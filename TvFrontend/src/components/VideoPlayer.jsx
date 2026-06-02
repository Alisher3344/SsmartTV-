import React, { useEffect, useRef } from 'react';
import Hls from 'hls.js';
import { useStore } from '../store/useStore';

const VideoPlayer = ({ src, poster, onClose }) => {
  const videoRef = useRef(null);
  const hlsRef = useRef(null);
  const setPlayerOpen = useStore((s) => s.setPlayerOpen);

  // Player ochiq bo'lganda suzuvchi tugmalarni (MastersFab) yashiramiz,
  // yopilganda yana ko'rsatamiz.
  useEffect(() => {
    setPlayerOpen(true);
    return () => setPlayerOpen(false);
  }, [setPlayerOpen]);

  useEffect(() => {
    console.log('VideoPlayer mounted, src:', src);
    const video = videoRef.current;
    if (!video) {
      console.error('Video element not found');
      return;
    }

    // HLS stream uchun HLS.js ishlatish. Backend proxy URL'i (/api/v1/stream/{slug})
    // .m3u8 kengaytmasiz keladi, shuning uchun /stream/ ni ham HLS deb hisoblaymiz.
    const isHls = src.includes('.m3u8') || src.includes('/stream/');
    if (isHls) {
      console.log('HLS stream detected, using HLS.js');
      if (Hls.isSupported()) {
        console.log('HLS.js is supported');
        const hls = new Hls({
          enableWorker: true,
          lowLatencyMode: true,
          backBufferLength: 90,
          xhrSetup: function(xhr, url) {
            // CORS uchun credentials
            xhr.withCredentials = false;
          }
        });
        
        hlsRef.current = hls;
        hls.loadSource(src);
        hls.attachMedia(video);
        
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          console.log('Manifest parsed, starting playback');
          video.play().catch(err => console.error('Play error:', err));
        });

        hls.on(Hls.Events.ERROR, (event, data) => {
          console.error('HLS error:', data);
          if (data.fatal) {
            switch (data.type) {
              case Hls.ErrorTypes.NETWORK_ERROR:
                console.error('Network error encountered, trying to recover');
                hls.startLoad();
                break;
              case Hls.ErrorTypes.MEDIA_ERROR:
                console.error('Media error encountered, trying to recover');
                hls.recoverMediaError();
                break;
              default:
                console.error('Fatal error, cannot recover');
                hls.destroy();
                break;
            }
          }
        });
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // Safari uchun native HLS qo'llab-quvvatlash
        console.log('Using native HLS for Safari');
        video.src = src;
        video.addEventListener('loadedmetadata', () => {
          console.log('Metadata loaded, starting playback');
          video.play().catch(err => console.error('Play error:', err));
        });
      } else {
        console.error('HLS not supported in this browser');
      }
    } else {
      // Oddiy video fayl
      console.log('Regular video file');
      video.src = src;
      video.play().catch(err => console.error('Play error:', err));
    }

    return () => {
      console.log('VideoPlayer unmounting');
      if (hlsRef.current) {
        hlsRef.current.destroy();
      }
    };
  }, [src]);

  return (
    <div className="fixed inset-0 bg-black z-50 flex items-center justify-center">
      {/* Close button */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 z-50 bg-black bg-opacity-70 hover:bg-opacity-90 text-white p-3 rounded-full transition-all"
      >
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      {/* Video Player */}
      <video
        ref={videoRef}
        className="w-full h-full"
        controls
        autoPlay
        poster={poster}
      />
    </div>
  );
};

export default VideoPlayer;
