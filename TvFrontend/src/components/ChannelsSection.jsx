import React, { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import apiClient, { absoluteUrl } from '../api/client';
import VideoPlayer from './VideoPlayer';

const ChannelsSection = () => {
  const { t } = useTranslation();
  const scrollRef = useRef(null);
  const [showPlayer, setShowPlayer] = useState(false);
  const [selectedChannel, setSelectedChannel] = useState(null);
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    let active = true;
    apiClient
      .get('/api/channels')
      .then(({ data }) => {
        if (!active) return;
        setChannels(
          data.map((c) => ({
            id: c.slug,
            name: c.name,
            logo: c.logo,
            videoUrl: c.stream_url ? absoluteUrl(c.stream_url) : null,
          }))
        );
      })
      .catch(() => active && setChannels([]));
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
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-6">
        <h2 className="section-title">
          {t('sections.channels')}
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
        className="flex gap-4 overflow-x-auto scrollbar-hide scroll-smooth"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {channels.map((channel) => (
          <div 
            key={channel.id}
            className="flex-shrink-0 w-32 h-20 bg-dark-card rounded-lg flex items-center justify-center hover:bg-gray-800 transition-colors cursor-pointer"
            onClick={() => {
              if (channel.videoUrl) {
                setSelectedChannel(channel);
                setShowPlayer(true);
              }
            }}
          >
            <img 
              src={channel.logo} 
              alt={channel.name}
              className="max-w-full max-h-full object-contain p-2"
            />
          </div>
        ))}
      </div>
      
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
