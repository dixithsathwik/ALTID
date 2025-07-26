from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import tempfile
from verification.ocr import extract_text
from verification.face_match import match_faces
from verification.extract_photo import extract_photo_from_xml, extract_photo_from_pdf
from verification.signature_validation import validate_xml_signature, validate_pdf_signature
from utils.jwt_utils import issue_token
from utils.logging_utils import log_failure
from config import JWT_CLAIMS, JWT_EXPIRATION_MINUTES, JWT_ISSUER

app = Flask(__name__)
CORS(app)

sessions = {}  # In-memory session store for demo

@app.route('/start', methods=['GET'])
def start_verification():
    callback_url = request.args.get('callback')
    if not callback_url:
        return jsonify({'error': 'Missing callback URL'}), 400
    # Generate a session token (for demo, use a simple counter)
    session_id = str(len(sessions) + 1)
    sessions[session_id] = {'callback_url': callback_url}
    return jsonify({'session_id': session_id})

@app.route('/upload-doc', methods=['POST'])
def upload_doc():
    session_id = request.form.get('session_id')
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    if 'doc' not in request.files:
        return jsonify({'error': 'Missing document'}), 400
    doc_file = request.files['doc']
    filename = secure_filename(doc_file.filename)
    ext = os.path.splitext(filename)[1].lower()
    with tempfile.TemporaryDirectory(dir='backend/temp') as temp_dir:
        doc_path = os.path.join(temp_dir, filename)
        doc_file.save(doc_path)
        if ext == '.xml':
            if not validate_xml_signature(doc_path):
                log_failure('Invalid XML signature', {'session_id': session_id})
                return jsonify({'error': 'Invalid XML signature'}), 400
            photo = extract_photo_from_xml(doc_path)
        elif ext == '.pdf':
            if not validate_pdf_signature(doc_path):
                log_failure('Invalid PDF signature', {'session_id': session_id})
                return jsonify({'error': 'Invalid PDF signature'}), 400
            photo = extract_photo_from_pdf(doc_path)
        else:
            log_failure('Unsupported document type', {'session_id': session_id})
            return jsonify({'error': 'Only Aadhaar Paperless Offline e-KYC XML files are accepted'}), 400
        if photo is None:
            log_failure('Photo extraction failed', {'session_id': session_id})
            return jsonify({'error': 'Photo extraction failed'}), 400
        # Save photo for next step
        photo_path = os.path.join(temp_dir, 'doc_photo.jpg')
        photo.save(photo_path)
        # For demo, store photo bytes in session (not for production)
        with open(photo_path, 'rb') as f:
            sessions[session_id]['doc_photo'] = f.read()
        return jsonify({'success': True})

@app.route('/upload-selfie', methods=['POST'])
def upload_selfie():
    session_id = request.form.get('session_id')
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    if 'selfie' not in request.files:
        return jsonify({'error': 'Missing selfie'}), 400
    selfie_file = request.files['selfie']
    with tempfile.TemporaryDirectory(dir='backend/temp') as temp_dir:
        selfie_path = os.path.join(temp_dir, secure_filename(selfie_file.filename))
        selfie_file.save(selfie_path)
        # Save doc photo to temp file
        doc_photo_path = os.path.join(temp_dir, 'doc_photo.jpg')
        with open(doc_photo_path, 'wb') as f:
            f.write(sessions[session_id]['doc_photo'])
        # Face match
        if not match_faces(doc_photo_path, selfie_path):
            log_failure('Face match failed', {'session_id': session_id})
            return jsonify({'error': 'Face match failed'}), 401
        # Issue JWT
        payload = {
            'sub': session_id,
            'iss': JWT_ISSUER,
            **JWT_CLAIMS
        }
        token = issue_token(payload)
        callback_url = sessions[session_id]['callback_url']
        # Redirect with JWT as query param
        redirect_url = f"{callback_url}?token={token}"
        return jsonify({'redirect_url': redirect_url, 'token': token})

@app.route('/public-key', methods=['GET'])
def public_key():
    key_path = os.path.join('static', 'keys', 'public.pem')
    if os.path.exists(key_path):
        return send_file(key_path)
    return jsonify({'error': 'Public key not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 