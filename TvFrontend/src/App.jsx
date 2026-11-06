import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import MastersFab from './components/MastersFab';
import Home from './pages/Home';
import TVChannels from './pages/TVChannels';
import Movies from './pages/Movies';
import Series from './pages/Series';
import Kids from './pages/Kids';
import Agreement from './pages/Agreement';
import Privacy from './pages/Privacy';
import MovieDetail from './pages/MovieDetail';
import AdminPanel from './pages/AdminPanel';
import ComingSoon from './components/ComingSoon';
import { useStore } from './store/useStore';
import './i18n/config';

function App() {
  const { i18n } = useTranslation();
  const fetchMe = useStore((s) => s.fetchMe);

  useEffect(() => {
    // Tilni localStorage dan yuklash
    const savedLanguage = localStorage.getItem('language') || 'uz';
    i18n.changeLanguage(savedLanguage);
  }, [i18n]);

  useEffect(() => {
    // Joriy sessiyani backend cookie orqali tekshirish
    fetchMe();
  }, [fetchMe]);
  
  return (
    <Router>
      <div className="relative z-10 min-h-screen bg-dark text-white">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          {/* --- VAQTINCHA: Tez kunda (asl sahifalar commentga olindi; qaytarish uchun commentni oching) --- */}
          <Route path="/channels" element={<ComingSoon />} />
          {/* <Route path="/channels" element={<TVChannels />} /> */}
          <Route path="/sport" element={<ComingSoon />} />
          {/* <Route path="/sport" element={<TVChannels />} /> */}
          <Route path="/movies" element={<ComingSoon />} />
          {/* <Route path="/movies" element={<Movies />} /> */}
          {/* --- VAQTINCHA tugadi --- */}
          <Route path="/movie/:id" element={<MovieDetail />} />
          <Route path="/series" element={<Series />} />
          <Route path="/kids" element={<Kids />} />
          <Route path="/agreement" element={<Agreement />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
        <Footer />
        <MastersFab />
      </div>
    </Router>
  );
}

export default App;
