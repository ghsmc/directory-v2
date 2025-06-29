import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Jobs } from './pages/Jobs';
import { Companies } from './pages/Companies';
import { Directory } from './pages/Directory';
import { Feed } from './pages/Feed';
import { Chat } from './pages/Chat';
import { Auth } from './pages/Auth';
import ProfilePage from './pages/Profile';

function AppRoutes() {
  const [session, setSession] = useState<any>(null);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogin = () => {
    // Demo login - just set a mock session
    setSession({ user: { id: '1', email: 'demo@example.com' } });
    // Redirect to feed after login
    navigate('/');
  };

  return !session ? (
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
  );
}

function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

export default App;