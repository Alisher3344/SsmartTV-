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
  
  // Yuklanib bo'lgach kanal bo'lmasa — bo'limni ko'rsatmaymiz
  if (loaded && channels.length === 0) return null;

  return (
    <div className="page-container py-12">
      <div className="flex items-center justify-between mb-6">
        <h2 className="section-title">
          <span className="gradient-text">{t('sections.channels')}</span>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor" className="text-primary">
            <path d="M4 2l4 4-4 4" stroke="currentColor" strokeWidth="2" fill="none"/>
          </svg>
        </h2>

        <div className="flex gap-2">
          <button
            onClick={() => scroll('left')}
            className="tap-target bg-dark-card hover:bg-primary rounded-lg transition-colors active:scale-95"
            aria-label="Chapga"
          >
            <ChevronLeft size={22} />
          </button>
          <button
            onClick={() => scroll('right')}
            className="tap-target bg-dark-card hover:bg-primary rounded-lg transition-colors active:scale-95"
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
            className="relative flex-shrink-0 w-32 h-20 bg-dark-card rounded-lg flex items-center justify-center glow-hover hover:bg-gray-800 cursor-pointer overflow-hidden"
            onClick={() => {
              if (channel.videoUrl) {
                setSelectedChannel(channel);
                setShowPlayer(true);
              }
            }}
          >
            {channel.country && (
              <span className="absolute top-1 left-1 px-1.5 py-0.5 rounded-full bg-black/60 text-[9px] font-medium text-gray-200">
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
