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
      <ChannelsSection />

      {/* Filmlar va seriallar — tez kunda */}
      <section className="page-container py-12">
        <h2 className="section-title">
          <span className="gradient-text">{t('sections.comingSoonRow')}</span>
        </h2>
        <ComingSoon className="py-8" showBackButton={false} />
      </section>

      <CinemasSection />
    </div>
  );
};

export default Home;
