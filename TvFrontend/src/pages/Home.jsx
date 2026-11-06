import { useTranslation } from 'react-i18next';
import HeroSection from '../components/HeroSection';
import ChannelsSection from '../components/ChannelsSection';
import CinemasSection from '../components/CinemasSection';
import ComingSoon from '../components/ComingSoon';

const Home = () => {
  const { t } = useTranslation();

  return (
    <div>
      <HeroSection />

      <div className="reveal reveal-1">
        <ChannelsSection />
      </div>

      {/* Filmlar va seriallar — tez kunda */}
      <section className="page-container py-16 reveal reveal-2">
        <div className="flex items-end gap-4 mb-7">
          <span className="section-index hidden sm:block">03</span>
          <h2 className="section-title mb-0">{t('sections.comingSoonRow')}</h2>
        </div>
        <ComingSoon className="py-8" showBackButton={false} />
      </section>

      <div className="reveal reveal-3">
        <CinemasSection />
      </div>
    </div>
  );
};

export default Home;
