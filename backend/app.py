from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import tempfile
from verification.ocr import extract_text
from verification.face_match import match_faces
from utils.jwt_utils import issue_token

app = Flask(__name__)
CORS(app)

@app.route('/verify', methods=['POST'])
def verify():
    if 'id_image' not in request.files or 'selfie' not in request.files:
        return jsonify({'error': 'Missing files'}), 400
    id_file = request.files['id_image']
    selfie_file = request.files['selfie']
    with tempfile.TemporaryDirectory(dir='backend/temp') as temp_dir:
        id_path = os.path.join(temp_dir, secure_filename(id_file.filename))
        selfie_path = os.path.join(temp_dir, secure_filename(selfie_file.filename))
        id_file.save(id_path)
        selfie_file.save(selfie_path)
        # OCR
        text = extract_text(id_path)
        # Simple parsing (for demo)
        name = 'Unknown'
        dob = 'Unknown'
        nationality = 'Unknown'
        for line in text.split('\n'):
            if 'Name' in line:
                name = line.split(':')[-1].strip()
            if 'DOB' in line or 'Birth' in line:
                dob = line.split(':')[-1].strip()
            if 'Nationality' in line:
                nationality = line.split(':')[-1].strip()
        # Face match
        if not match_faces(id_path, selfie_path):
            return jsonify({'error': 'Face match failed'}), 401
        # Issue JWT
        payload = {
            'sub': 'user123',
            'name': name,
            'dob': dob,
            'nationality': nationality
        }
        token = issue_token(payload)
        return jsonify({'token': token})

@app.route('/public-key', methods=['GET'])
def public_key():
    # Placeholder for serving public key
    key_path = os.path.join('static', 'keys', 'public.pem')
    if os.path.exists(key_path):
        return send_file(key_path)
    return jsonify({'error': 'Public key not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 