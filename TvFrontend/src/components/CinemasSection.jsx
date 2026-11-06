import { useTranslation } from 'react-i18next';
import { moviesData } from '../data/movies';

const CinemasSection = () => {
  const { t } = useTranslation();
  
  return (
    <div className="page-container py-16">
      <div className="flex items-end gap-4 mb-7">
        <span className="section-index hidden sm:block">02</span>
        <div>
          <p className="eyebrow">{t('sections.cinemasKicker')}</p>
          <h2 className="section-title mb-0">{t('sections.cinemas')}</h2>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 sm:gap-5">
        {moviesData.cinemas.map((cinema) => (
          <div
            key={cinema.id}
            className="aspect-[3/2] min-w-0 rounded-xl overflow-hidden ring-1 ring-white/5 hover:ring-gold/40 hover:-translate-y-1 transition duration-300 cursor-pointer"
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
