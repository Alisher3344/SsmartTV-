import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import apiClient from '../api/client';

const ROTATE_MS = 6000;

// Bosh sahifa karuseli — slaydlar super-admin tomonidan
// ssmart-dashboard.ssmart.uz/tv-admins dan boshqariladi (TV backend /api/v1/carousel).
// Faol slayd bo'lmasa — hech narsa ko'rsatilmaydi (bo'sh joy egallamaydi).
const HeroSection = () => {
  const { i18n } = useTranslation();
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
    return <div className="skeleton h-[56vh] min-h-[360px] sm:h-[60vh] sm:min-h-[440px]" />;
  }
  if (slides.length === 0) return null;

  const slide = slides[Math.min(idx, slides.length - 1)];
  const title =
    (lang === 'ru' ? slide.title_ru : slide.title_uz) || slide.title_uz || slide.title_ru || '';

  const body = (
    <div
      className="relative h-[56vh] min-h-[360px] sm:h-[60vh] sm:min-h-[440px] bg-cover bg-center"
      style={{ backgroundImage: `url(${slide.image})` }}
    >
      <div className="absolute inset-0 hero-gradient"></div>

      {title && (
        <div className="relative page-container h-full flex items-end pb-12 sm:pb-16">
          <h1 className="text-fluid-hero font-bold text-white max-w-2xl tracking-wide animate-fade-up drop-shadow-lg">
            {title}
          </h1>
        </div>
      )}

      {/* Slayd indikatorlari */}
      {slides.length > 1 && (
        <div className="absolute bottom-3 right-4 sm:right-8 flex gap-1">
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
                className={`block h-2 rounded-full transition-all ${
                  i === idx ? 'w-6 bg-primary' : 'w-2 bg-gray-500 hover:bg-gray-300'
                }`}
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );

  return slide.link_url ? (
    <a href={slide.link_url} className="block">
      {body}
    </a>
  ) : (
    body
  );
};

export default HeroSection;
