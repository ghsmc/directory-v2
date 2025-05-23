import React from 'react';

export function DotPattern() {
  return (
    <div className="absolute inset-0 -z-10 overflow-hidden">
      <div 
        className="absolute inset-0 bg-[radial-gradient(#80808012_1px,transparent_1px)] [background-size:24px_24px]"
      />
      
      {/* Subtle gradient overlays */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-white/50 to-white" />
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-white" />
    </div>
  );
}