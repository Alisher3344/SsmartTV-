import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useStore } from '../store/useStore';
import { Search, Bell, User, Menu, X, Globe } from 'lucide-react';

const Navbar = () => {
  const { t, i18n } = useTranslation();
  const { language, setLanguage } = useStore();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  
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
  
  return (
    <nav className="bg-dark-lighter border-b border-gray-800 sticky top-0 z-50 backdrop-blur-md bg-opacity-90">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-24">
          {/* Logo - Chap tomonda */}
          <div className="flex items-center flex-shrink-0">
            <Link to="/">
              <img 
                src="/logo.png" 
                alt="Smart TV" 
                className="h-20 w-auto object-contain cursor-pointer"
                style={{ filter: 'drop-shadow(0 0 10px rgba(113, 0, 135, 0.5))' }}
              />
            </Link>
          </div>
          
          {/* Desktop Navigation - O'rtada */}
          <div className="hidden lg:flex items-center justify-center flex-1">
            <div className="flex items-center space-x-8">
              {navItems.map((item) => (
                <Link key={item.key} to={item.path} className="navbar-link text-base">
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
          
          {/* Right Section - O'ng tomonda */}
          <div className="flex items-center space-x-4">
            {/* Search Icon */}
            <button className="text-gray-300 hover:text-white transition-colors">
              <Search size={20} />
            </button>
            
            {/* Language Switcher */}
            <div className="flex items-center gap-1 bg-dark-card px-2 py-1 rounded-lg">
              <Globe size={16} className="text-gray-400" />
              <button
                onClick={() => changeLanguage('uz')}
                className={`px-2 py-1 text-xs rounded transition-colors ${
                  language === 'uz' ? 'bg-primary text-black' : 'text-gray-400 hover:text-white'
                }`}
              >
                UZ
              </button>
              <button
                onClick={() => changeLanguage('ru')}
                className={`px-2 py-1 text-xs rounded transition-colors ${
                  language === 'ru' ? 'bg-primary text-black' : 'text-gray-400 hover:text-white'
                }`}
              >
                RU
              </button>
            </div>
            
            {/* Notifications */}
            <button className="text-gray-300 hover:text-white transition-colors hidden sm:block">
              <Bell size={20} />
            </button>
            
            {/* User / Admin panel */}
            <button
              onClick={() => navigate('/admin')}
              title="Admin panel"
              className="flex items-center gap-2 bg-dark-card px-3 py-2 rounded-lg hover:bg-gray-800 transition-colors"
            >
              <User size={18} />
              <span className="text-sm hidden sm:inline">SS</span>
            </button>
            
            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden text-gray-300 hover:text-white"
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-dark-card border-t border-gray-800">
          <div className="px-4 py-4 space-y-3">
            {navItems.map((item) => (
              <Link
                key={item.key}
                to={item.path}
                className="block navbar-link py-2 text-base"
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
