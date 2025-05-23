import React from 'react';
import { ChatInterface } from '../components/ChatInterface';
import { Navbar } from '../components/Navbar';

export function Chat() {
  return (
    <div className="h-screen flex">
      <Navbar />
      <div className="flex-1 md:pl-[72px]">
        <ChatInterface />
      </div>
    </div>
  );
}