import React, { useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { moviesData } from '../data/movies';

const PremieresSection = () => {
  const { t, i18n } = useTranslation();
  const scrollRef = useRef(null);
  const currentLang = i18n.language;
  
  const scroll = (direction) => {
    if (scrollRef.current) {
      const scrollAmount = 400;
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-6">
        <h2 className="section-title">
          {t('sections.premieres')}
          <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
            <path d="M4 2l4 4-4 4" stroke="currentColor" strokeWidth="2" fill="none"/>
          </svg>
        </h2>
        
        <div className="flex gap-2">
          <button 
            onClick={() => scroll('left')}
            className="bg-dark-card hover:bg-gray-800 p-2 rounded-lg transition-colors"
          >
            <ChevronLeft size={20} />
          </button>
          <button 
            onClick={() => scroll('right')}
            className="bg-dark-card hover:bg-gray-800 p-2 rounded-lg transition-colors"
          >
            <ChevronRight size={20} />
          </button>
        </div>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex gap-4 overflow-x-auto scrollbar-hide scroll-smooth pb-4"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {moviesData.premieres.map((movie) => (
          <div 
            key={movie.id}
            className="flex-shrink-0 w-48 group cursor-pointer"
          >
            <div className="relative aspect-[2/3] rounded-lg overflow-hidden mb-3">
              <img 
                src={movie.image} 
                alt={movie.title[currentLang]}
                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              />
              {movie.age && (
                <div className="absolute top-2 right-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">
                  {movie.age}
                </div>
              )}
            </div>
            
            <h3 className="font-semibold text-sm mb-1 line-clamp-2">
              {movie.title[currentLang]}
            </h3>
            <p className="text-xs text-gray-400">
              {movie.genre[currentLang]}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PremieresSection;
