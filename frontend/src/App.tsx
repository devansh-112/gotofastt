import React from 'react';

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-red-gradient">
      {/* Brand Logo Placeholder */}
      <div className="mt-8 mb-4">
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="40" r="38" stroke="#2563eb" strokeWidth="4" fill="#fff" />
          <text x="50%" y="54%" textAnchor="middle" fill="#2563eb" fontSize="32" fontWeight="bold" fontFamily="Arial" dy=".3em">GF</text>
        </svg>
      </div>
      {/* Brand Name */}
      <h1 className="text-4xl font-extrabold text-white drop-shadow-lg mb-2 tracking-wide">GotoFast</h1>
      <p className="text-lg text-white/80 mb-8 max-w-xl text-center">
        Fast, reliable, and modern logistics for businesses and consumers. Book, track, and manage your deliveries with ease.
      </p>
      <div className="flex gap-4">
        <button className="px-6 py-3 rounded-lg bg-white/90 text-brand-blue font-semibold shadow hover:bg-white transition">Book a Delivery</button>
        <button className="px-6 py-3 rounded-lg bg-white/20 text-white font-semibold border border-white/40 hover:bg-white/30 transition">Track Package</button>
      </div>
    </div>
  );
}

export default App; 