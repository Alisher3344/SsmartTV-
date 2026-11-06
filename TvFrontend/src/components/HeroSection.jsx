import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Play } from 'lucide-react';
import apiClient from '../api/client';

const ROTATE_MS = 6000;

// Bosh sahifa karuseli — slaydlar super-admin tomonidan
// ssmart-dashboard.ssmart.uz/tv-admins dan boshqariladi (TV backend /api/v1/carousel).
// Faol slayd bo'lmasa — hech narsa ko'rsatilmaydi (bo'sh joy egallamaydi).
const HeroSection = () => {
  const { t, i18n } = useTranslation();
  const lang = i18n.language === 'ru' ? 'ru' : 'uz';

  const [slides, setSlides] = useState([]);
  const [idx, setIdx] = useState(0);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let active = true;
    apiClient
      .get('/api/v1/carousel')
      .then(({ data }) => {
        if (!active) return;
        setSlides(Array.isArray(data) ? data : data?.items ?? []);
      })
      .catch(() => active && setSlides([]))
      .finally(() => active && setLoaded(true));
    return () => {
      active = false;
    };
  }, []);

  // Avtomatik aylanish (bir nechta slayd bo'lsa)
  useEffect(() => {
    if (slides.length <= 1) return;
    const t = setInterval(() => setIdx((i) => (i + 1) % slides.length), ROTATE_MS);
    return () => clearInterval(t);
  }, [slides.length]);

  // Slayd o'chirilsa, indeksni chegarada ushlab turamiz
  useEffect(() => {
    if (idx >= slides.length) setIdx(0);
  }, [slides.length, idx]);

  // Yuklanmaguncha — skeleton; faol slayd bo'lmasa — hech narsa
  if (!loaded) {
    return <div className="skeleton h-[68vh] min-h-[440px] sm:h-[78vh] sm:min-h-[560px]" />;
  }
  if (slides.length === 0) return null;

  const slide = slides[Math.min(idx, slides.length - 1)];
  const title =
    (lang === 'ru' ? slide.title_ru : slide.title_uz) || slide.title_uz || slide.title_ru || '';

  return (
    <section className="relative h-[68vh] min-h-[440px] sm:h-[78vh] sm:min-h-[560px] overflow-hidden">
      {/* Fon — sekin ken-burns zoom (har slayd almashganda qayta ishga tushadi) */}
      <div
        key={slide.id}
        className="absolute inset-0 bg-cover bg-center animate-kenburns"
        style={{ backgroundImage: `url(${slide.image})` }}
      />

      {/* Asimmetrik chap-og'ir scrim (editorial matn o'qilishi uchun) + pastki fade */}
      <div className="absolute inset-0 bg-gradient-to-r from-ink/90 via-ink/35 to-transparent" />
      <div className="absolute inset-0 hero-gradient" />

      {/* Editorial kontent — chap ustun, pastga tayanadi */}
      <div className="relative page-container h-full flex items-end pb-12 sm:pb-20">
        <div className="max-w-2xl">
          <p className="eyebrow reveal reveal-1">{t('hero.live')}</p>

          {title && (
            <h1 className="font-display text-fluid-hero font-semibold text-white reveal reveal-2 drop-shadow-[0_2px_20px_rgba(0,0,0,0.6)]">
              {title}
            </h1>
          )}

          <div className="mt-7 flex flex-wrap items-center gap-3 reveal reveal-3">
            {slide.link_url ? (
              <a href={slide.link_url} className="btn-primary">
                <Play size={18} fill="currentColor" />
                {t('hero.watch')}
              </a>
            ) : (
              <span className="btn-primary">
                <Play size={18} fill="currentColor" />
                {t('hero.watch')}
              </span>
            )}
            {slide.link_url && (
              <a href={slide.link_url} className="btn-outline">
                {t('hero.more')}
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Slayd indikatorlari */}
      {slides.length > 1 && (
        <div className="absolute bottom-4 right-4 sm:right-8 flex gap-1">
          {slides.map((s, i) => (
            <button
              key={s.id}
              onClick={(e) => {
                e.preventDefault();
                setIdx(i);
              }}
              aria-label={`Slayd ${i + 1}`}
              className="flex h-6 items-center px-1"
            >
              <span
                className={`block h-1.5 rounded-full transition-all ${
                  i === idx ? 'w-7 bg-gold' : 'w-2 bg-white/30 hover:bg-white/60'
                }`}
              />
            </button>
          ))}
        </div>
      )}
    </section>
  );
};

export default HeroSection;
