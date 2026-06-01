import React from 'react';
import { useTranslation } from 'react-i18next';
import HeroSection from '../components/HeroSection';
import FeaturedSection from '../components/FeaturedSection';
import ChannelsSection from '../components/ChannelsSection';
import CinemasSection from '../components/CinemasSection';
import PremieresSection from '../components/PremieresSection';

const Home = () => {
  const { i18n } = useTranslation();
  
  return (
    <div>
      <HeroSection />
      <FeaturedSection />
      <ChannelsSection />
      <CinemasSection />
      <PremieresSection />
      
      {/* O'zbek dublyajidagi seriallar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="section-title mb-6">
          {i18n.language === 'uz' ? "O'zbek dublyajidagi seriallar" : "Сериалы с узбекским дубляжом"}
          <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
            <path d="M4 2l4 4-4 4" stroke="currentColor" strokeWidth="2" fill="none"/>
          </svg>
        </h2>
        
        <div className="text-center py-12">
          <p className="text-gray-400 mb-4">
            {i18n.language === 'uz' ? "Ko'proq ko'rsatish" : "Показать больше"}
          </p>
          <button className="btn-primary">
            {i18n.language === 'uz' ? "Barcha seriallarni ko'rish" : "Посмотреть все сериалы"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
