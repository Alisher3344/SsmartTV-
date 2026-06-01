import React from 'react';
import { useTranslation } from 'react-i18next';
import { Play } from 'lucide-react';
import { moviesData } from '../data/movies';

const FeaturedSection = () => {
  const { t, i18n } = useTranslation();
  const { featured } = moviesData;
  const currentLang = i18n.language;
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 relative z-10 mb-12">
      <h2 className="section-title mb-6 text-xl">
        {t('hero.more')}
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
          <path d="M4 2l4 4-4 4" stroke="currentColor" strokeWidth="2" fill="none"/>
        </svg>
      </h2>
      
      <div className="bg-dark-card rounded-xl overflow-hidden hover:scale-[1.02] transition-transform duration-300 cursor-pointer">
        <div className="flex flex-col sm:flex-row">
          <div className="sm:w-56 h-72 sm:h-auto relative group">
            <img 
              src={featured.image} 
              alt={featured.title[currentLang]}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
              <Play size={56} className="text-primary" fill="currentColor" />
            </div>
          </div>
          
          <div className="p-8 flex-1">
            <h3 className="text-2xl font-bold mb-3">{featured.title[currentLang]}</h3>
            <p className="text-gray-400 mb-4 text-lg">{featured.description[currentLang]}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeaturedSection;
