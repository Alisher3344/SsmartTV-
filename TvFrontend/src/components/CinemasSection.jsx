import { useTranslation } from 'react-i18next';
import { moviesData } from '../data/movies';

const CinemasSection = () => {
  const { t } = useTranslation();
  
  return (
    <div className="page-container py-12">
      <h2 className="section-title">
        <span className="gradient-text">{t('sections.cinemas')}</span>
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor" className="text-primary">
          <path d="M4 2l4 4-4 4" stroke="currentColor" strokeWidth="2" fill="none"/>
        </svg>
      </h2>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
        {moviesData.cinemas.map((cinema) => (
          <div
            key={cinema.id}
            className="aspect-[3/2] min-w-0 rounded-xl overflow-hidden glow-hover sm:hover:scale-105 cursor-pointer"
            style={{ backgroundColor: cinema.color }}
          >
            <div className="w-full h-full flex items-center justify-center p-4">
              <img 
                src={cinema.logo} 
                alt={cinema.name}
                className="max-w-full max-h-full object-contain"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CinemasSection;
