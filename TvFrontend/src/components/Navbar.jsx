import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useStore } from '../store/useStore';
import { Search, Bell, User, Menu, X, Globe } from 'lucide-react';

const Navbar = () => {
  const { t, i18n } = useTranslation();
  const { language, setLanguage } = useStore();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
    setLanguage(lang);
  };

  const navItems = [
    { key: 'home', label: t('nav.home'), path: '/' },
    { key: 'tv', label: t('nav.tv'), path: '/channels' },
    { key: 'sport', label: t('nav.sport'), path: '/sport' },
    { key: 'films', label: t('nav.films'), path: '/movies' },
    { key: 'series', label: t('nav.series'), path: '/series' },
    { key: 'kids', label: t('nav.kids'), path: '/kids' },
  ];

  const isActive = (path) => (path === '/' ? pathname === '/' : pathname.startsWith(path));

  return (
    <nav className="bg-dark-lighter/80 border-b border-white/5 sticky top-0 z-50 backdrop-blur-xl">
      <div className="page-container">
        <div className="flex items-center justify-between h-16 sm:h-20 lg:h-24">
          {/* Logo */}
          <div className="flex items-center flex-shrink-0">
            <Link to="/" aria-label="Smart TV">
              <img
                src="/logo.png"
                alt="Smart TV"
                className="h-12 sm:h-16 lg:h-20 w-auto object-contain cursor-pointer transition-transform duration-300 hover:scale-105"
                style={{ filter: 'brightness(0) invert(1) drop-shadow(0 0 10px rgba(113, 0, 135, 0.5))' }}
              />
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center justify-center flex-1">
            <div className="flex items-center space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.key}
                  to={item.path}
                  className={`navbar-link text-base relative py-1 ${
                    isActive(item.path)
                      ? "text-primary after:absolute after:-bottom-0.5 after:left-0 after:right-0 after:h-0.5 after:rounded-full after:bg-primary after:shadow-glow-sm"
                      : ''
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>

          {/* Right Section */}
          <div className="flex items-center space-x-1.5 sm:space-x-3">
            {/* Search */}
            <button
              className="tap-target text-gray-300 hover:text-white transition-colors rounded-lg active:scale-95"
              aria-label="Qidirish"
            >
              <Search size={20} />
            </button>

            {/* Language Switcher */}
            <div className="flex items-center gap-1 bg-dark-card px-2 py-1 rounded-lg">
              <Globe size={16} className="hidden xs:block text-gray-400" />
              <button
                onClick={() => changeLanguage('uz')}
                className={`px-2 py-1 text-xs rounded transition-colors active:scale-95 ${
                  language === 'uz' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                UZ
              </button>
              <button
                onClick={() => changeLanguage('ru')}
                className={`px-2 py-1 text-xs rounded transition-colors active:scale-95 ${
                  language === 'ru' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                RU
              </button>
            </div>

            {/* Notifications */}
            <button
              className="tap-target text-gray-300 hover:text-white transition-colors rounded-lg active:scale-95 hidden sm:flex"
              aria-label="Bildirishnomalar"
            >
              <Bell size={20} />
            </button>

            {/* User / Admin panel */}
            <button
              onClick={() => navigate('/admin')}
              title="Admin panel"
              className="flex items-center gap-2 bg-dark-card px-3 py-2 rounded-lg hover:bg-gray-800 transition-colors active:scale-95 min-h-touch"
            >
              <User size={18} />
              <span className="text-sm hidden sm:inline">SS</span>
            </button>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="tap-target lg:hidden text-gray-300 hover:text-white rounded-lg active:scale-95"
              aria-label="Menyu"
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-dark-card border-t border-white/5 animate-fade-up">
          <div className="px-4 py-2">
            {navItems.map((item) => (
              <Link
                key={item.key}
                to={item.path}
                className={`flex items-center min-h-touch py-3 px-2 rounded-lg text-base font-medium transition-colors ${
                  isActive(item.path)
                    ? 'text-primary bg-primary/10'
                    : 'text-white hover:text-primary hover:bg-white/5'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
