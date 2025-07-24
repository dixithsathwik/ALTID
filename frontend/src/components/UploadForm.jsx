import React, { useState } from 'react';

export default function UploadForm() {
  const [idImage, setIdImage] = useState(null);
  const [selfie, setSelfie] = useState(null);
  const [jwt, setJwt] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setJwt('');
    setLoading(true);
    const formData = new FormData();
    formData.append('id_image', idImage);
    formData.append('selfie', selfie);
    try {
      const res = await fetch('http://localhost:5000/verify', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setJwt(data.token);
      } else {
        setError(data.error || 'Verification failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">ALTID Identity Verification</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Upload ID Image</label>
          <input type="file" accept="image/*" required onChange={e => setIdImage(e.target.files[0])} className="block w-full" />
        </div>
        <div>
          <label className="block mb-1 font-medium">Upload Selfie</label>
          <input type="file" accept="image/*" required onChange={e => setSelfie(e.target.files[0])} className="block w-full" />
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700" disabled={loading}>
          {loading ? 'Verifying...' : 'Verify'}
        </button>
      </form>
      {error && <div className="mt-4 text-red-600">{error}</div>}
      {jwt && (
        <div className="mt-4">
          <div className="font-semibold mb-1">JWT Token:</div>
          <textarea className="w-full h-32 p-2 border rounded" readOnly value={jwt} />
        </div>
      )}
    </div>
  );
} 