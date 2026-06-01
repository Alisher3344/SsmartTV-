import React from 'react';
import { useTranslation } from 'react-i18next';
import { Play, Share2 } from 'lucide-react';
import { moviesData } from '../data/movies';

const HeroSection = () => {
  const { t, i18n } = useTranslation();
  const { hero } = moviesData;
  const currentLang = i18n.language;
  
  return (
    <div className="relative h-[70vh] min-h-[500px] bg-cover bg-center" 
         style={{ backgroundImage: `url(${hero.image})` }}>
      <div className="absolute inset-0 hero-gradient"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-end pb-12">
        <div className="max-w-2xl animate-slide-in">
          <h1 className="text-5xl sm:text-6xl font-bold mb-6 text-white tracking-wider">
            {hero.title[currentLang]}
          </h1>
          
          <div className="flex items-center gap-6 mb-6 text-sm">
            <span className="flex items-center gap-2">
              <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" 
                   alt="IMDb" className="h-6" />
              <span className="text-white font-semibold text-base">{hero.rating.imdb}</span>
            </span>
            <span className="text-gray-400">--</span>
            <span className="flex items-center gap-2">
              <span className="text-white font-semibold text-base">КГ</span>
            </span>
            <span className="text-gray-400">--</span>
            <span className="flex items-center gap-2">
              <span className="text-primary font-bold text-base">nTV</span>
              <span className="text-white font-semibold text-base">{hero.rating.ntv}</span>
            </span>
          </div>
          
          <p className="text-gray-300 mb-8 text-lg leading-relaxed">
            {hero.description[currentLang]}
          </p>
          
          <div className="flex flex-wrap gap-6">
            <button className="btn-primary flex items-center gap-3 px-10 py-3 text-base">
              <Play size={22} fill="currentColor" />
              {t('hero.watch')}
            </button>
            <button className="bg-dark-card hover:bg-gray-800 text-white font-semibold px-8 py-3 rounded-lg transition-all duration-300 flex items-center gap-3 text-base">
              <Share2 size={20} />
              {t('hero.share')}
            </button>
          </div>
        </div>
      </div>
      
      {/* Progress Indicators */}
      <div className="absolute bottom-4 right-8 flex gap-2">
        <div className="w-2 h-2 bg-primary rounded-full"></div>
        <div className="w-2 h-2 bg-gray-600 rounded-full"></div>
        <div className="w-2 h-2 bg-gray-600 rounded-full"></div>
      </div>
    </div>
  );
};

export default HeroSection;
