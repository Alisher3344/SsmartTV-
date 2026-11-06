import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import apiClient, { absoluteUrl } from '../api/client';
import VideoPlayer from './VideoPlayer';
import { RowSkeleton } from './Skeleton';

const ChannelsSection = () => {
  const { t, i18n } = useTranslation();
  const currentLang = i18n.language;
  const scrollRef = useRef(null);
  const [showPlayer, setShowPlayer] = useState(false);
  const [selectedChannel, setSelectedChannel] = useState(null);
  const [channels, setChannels] = useState([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let active = true;
    // Backend limiti 100 — barcha kanallarni sahifalab yuklaymiz.
    const fetchAll = async () => {
      const pageSize = 100;
      let offset = 0;
      let all = [];
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const { data } = await apiClient.get(
          `/api/v1/channels?limit=${pageSize}&offset=${offset}`
        );
        const items = Array.isArray(data) ? data : (data?.items ?? []);
        all = all.concat(items);
        const total = data?.total ?? all.length;
        if (items.length === 0 || all.length >= total) break;
        offset += pageSize;
      }
      return all;
    };

    fetchAll()
      .then((list) => {
        if (!active) return;
        setChannels(
          list.map((c) => ({
            id: c.slug,
            name: c.name,
            logo: c.logo,
            country: c.country, // {slug, name_uz, name_ru, ...}
            // Live kanal uchun backend proxy URL beradi (/api/v1/stream/{slug});
            // stream_url public javobda yashirilgan.
            videoUrl: c.playback_url ? absoluteUrl(c.playback_url) : null,
          }))
        );
      })
      .catch(() => active && setChannels([]))
      .finally(() => active && setLoaded(true));
    return () => {
      active = false;
    };
  }, []);

  const scroll = (direction) => {
    if (scrollRef.current) {
      const scrollAmount = 300;
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };
  
  // Yuklanib bo'lgach kanal bo'lmasa — "Tez kunda" placeholderini ko'rsatamiz
  if (loaded && channels.length === 0) {
    return (
      <div className="page-container py-16">
        <div className="flex items-end gap-4 mb-7">
          <span className="section-index hidden sm:block">01</span>
          <div>
            <p className="eyebrow">{t('sections.channelsKicker')}</p>
            <h2 className="section-title mb-0">{t('sections.channels')}</h2>
          </div>
        </div>
        <div className="rounded-2xl ring-1 ring-white/10 bg-white/5 py-14 px-6 text-center">
          <span className="inline-block px-3 py-1 mb-3 rounded-full bg-gold/20 text-gold text-xs font-semibold uppercase tracking-wider">
            {t('comingSoon.badge')}
          </span>
          <h3 className="text-2xl font-bold mb-2">{t('comingSoon.title')}</h3>
          <p className="text-white/60 max-w-md mx-auto">{t('comingSoon.subtitle')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container py-16">
      <div className="flex items-end justify-between mb-7">
        <div className="flex items-end gap-4">
          <span className="section-index hidden sm:block">01</span>
          <div>
            <p className="eyebrow">{t('sections.channelsKicker')}</p>
            <h2 className="section-title mb-0">{t('sections.channels')}</h2>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => scroll('left')}
            className="tap-target bg-white/5 ring-1 ring-white/10 hover:bg-gold hover:text-ink rounded-full transition-colors active:scale-95"
            aria-label="Chapga"
          >
            <ChevronLeft size={22} />
          </button>
          <button
            onClick={() => scroll('right')}
            className="tap-target bg-white/5 ring-1 ring-white/10 hover:bg-gold hover:text-ink rounded-full transition-colors active:scale-95"
            aria-label="O'ngga"
          >
            <ChevronRight size={22} />
          </button>
        </div>
      </div>

      {!loaded ? (
        <RowSkeleton count={8} itemClassName="w-32 h-20 flex-shrink-0" />
      ) : (
      <div
        ref={scrollRef}
        className="flex gap-3 sm:gap-4 overflow-x-auto scrollbar-hide scroll-smooth"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {channels.map((channel) => (
          <div
            key={channel.id}
            className="relative flex-shrink-0 w-32 h-20 bg-ink-700 ring-1 ring-white/5 rounded-xl flex items-center justify-center hover:ring-gold/40 hover:-translate-y-1 transition duration-300 cursor-pointer overflow-hidden"
            onClick={() => {
              if (channel.videoUrl) {
                setSelectedChannel(channel);
                setShowPlayer(true);
              }
            }}
          >
            {channel.country && (
              <span className="absolute top-1 left-1 px-1.5 py-0.5 rounded-full bg-ink/80 ring-1 ring-white/10 text-[9px] font-medium uppercase tracking-wider text-white/80">
                {currentLang === 'ru'
                  ? channel.country.name_ru
                  : channel.country.name_uz}
              </span>
            )}
            {channel.logo ? (
              <img
                src={channel.logo}
                alt={channel.name}
                className="max-w-full max-h-full object-contain p-2"
              />
            ) : (
              <span className="px-2 text-center text-sm font-medium text-white">
                {channel.name}
              </span>
            )}
          </div>
        ))}
      </div>
      )}

      {/* Video Player */}
      {showPlayer && selectedChannel && (
        <VideoPlayer 
          src={selectedChannel.videoUrl}
          poster={selectedChannel.logo}
          onClose={() => {
            setShowPlayer(false);
            setSelectedChannel(null);
          }}
        />
      )}
    </div>
  );
};

export default ChannelsSection;
