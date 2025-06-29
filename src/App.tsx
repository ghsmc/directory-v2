import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Jobs } from './pages/Jobs';
import { Companies } from './pages/Companies';
import { Directory } from './pages/Directory';
import { Feed } from './pages/Feed';
import { Chat } from './pages/Chat';
import { Auth } from './pages/Auth';
import ProfilePage from './pages/Profile';

function App() {
  const [session, setSession] = useState<any>(null);

  const handleLogin = () => {
    // Demo login - just set a mock session
    setSession({ user: { id: '1', email: 'demo@example.com' } });
  };

  return (
    <Router>
      {!session ? (
        <Routes>
          <Route path="/auth" element={<Auth onLogin={handleLogin} />} />
          <Route path="*" element={<Navigate to="/auth" replace />} />
        </Routes>
      ) : (
        <Routes>
          <Route path="/" element={<Feed />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/companies" element={<Companies />} />
          <Route path="/people" element={<Directory />} />
          <Route path="/feed" element={<Feed />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      )}
    </Router>
  );
}

export default App;