import React, { useState, useRef } from 'react';

function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

export default function UploadForm() {
  const [step, setStep] = useState(1);
  const [sessionId, setSessionId] = useState('');
  const [doc, setDoc] = useState(null);
  const [selfie, setSelfie] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [jwt, setJwt] = useState('');
  const [showCamera, setShowCamera] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const callback = getQueryParam('callback');

  // Step 1: Start session
  React.useEffect(() => {
    if (!callback) {
      setError('Missing callback URL. Please access this page via the correct verification link.');
      return;
    }
    setLoading(true);
    fetch(`http://localhost:5000/start?callback=${encodeURIComponent(callback)}`)
      .then(res => res.json())
      .then(data => {
        if (data.session_id) {
          setSessionId(data.session_id);
        } else {
          setError(data.error || 'Failed to start session');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Network error');
        setLoading(false);
      });
    // eslint-disable-next-line
  }, []);

  // Step 2: Upload DigiLocker doc
  const handleDocSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('doc', doc);
    try {
      const res = await fetch('http://localhost:5000/upload-doc', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setStep(2);
      } else {
        setError(data.error || 'Document verification failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  // Step 3: Upload selfie
  const handleSelfieSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('selfie', selfie);
    try {
      const res = await fetch('http://localhost:5000/upload-selfie', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.ok && data.redirect_url) {
        setJwt(data.token);
        window.location.href = data.redirect_url;
      } else {
        setError(data.error || 'Selfie verification failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  // Camera logic
  const startCamera = async () => {
    setError('');
    setShowCamera(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
      }
    } catch (err) {
      setError('Unable to access camera');
      setShowCamera(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setCameraActive(false);
    setShowCamera(false);
  };

  const captureSelfie = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(blob => {
        setSelfie(blob);
        stopCamera();
      }, 'image/jpeg');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">ALTID Identity Verification</h2>
      {!callback && (
        <div className="mb-4 text-red-600 font-semibold">Missing callback URL. Please access this page via the correct verification link from the website you are verifying with.</div>
      )}
      {!sessionId && loading && <div>Starting session...</div>}
      {error && <div className="mt-4 text-red-600">{error}</div>}
      {callback && sessionId && step === 1 && !error && (
        <form onSubmit={handleDocSubmit} className="space-y-4">
          <div>
                            <label className="block mb-1 font-medium">Upload Aadhaar Paperless Offline e-KYC XML</label>
                <input type="file" accept=".xml" required onChange={e => setDoc(e.target.files[0])} className="block w-full" />
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700" disabled={loading}>
            {loading ? 'Uploading...' : 'Continue'}
          </button>
        </form>
      )}
      {callback && sessionId && step === 2 && !error && (
        <form onSubmit={handleSelfieSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium">Take/Upload a Live Selfie</label>
            <div className="flex flex-col gap-2">
              <button type="button" className="bg-green-600 text-white py-1 px-3 rounded" onClick={startCamera} disabled={showCamera || cameraActive}>
                Use Camera
              </button>
              <input type="file" accept="image/*" onChange={e => setSelfie(e.target.files[0])} className="block w-full" />
            </div>
            {showCamera && (
              <div className="mt-2 flex flex-col items-center">
                <video ref={videoRef} autoPlay playsInline className="w-48 h-48 rounded border mb-2" />
                <canvas ref={canvasRef} style={{ display: 'none' }} />
                <div className="flex gap-2">
                  <button type="button" className="bg-blue-600 text-white py-1 px-3 rounded" onClick={captureSelfie}>
                    Capture
                  </button>
                  <button type="button" className="bg-gray-400 text-white py-1 px-3 rounded" onClick={stopCamera}>
                    Cancel
                  </button>
                </div>
              </div>
            )}
            {selfie && !showCamera && (
              <div className="mt-2">
                <div className="font-medium mb-1">Selfie Preview:</div>
                <img src={URL.createObjectURL(selfie)} alt="Selfie preview" className="w-32 h-32 object-cover rounded border" />
              </div>
            )}
          </div>
          <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700" disabled={loading || !selfie}>
            {loading ? 'Verifying...' : 'Verify'}
          </button>
        </form>
      )}
      {jwt && (
        <div className="mt-4">
          <div className="font-semibold mb-1">JWT Token:</div>
          <textarea className="w-full h-32 p-2 border rounded" readOnly value={jwt} />
        </div>
      )}
    </div>
  );
} 