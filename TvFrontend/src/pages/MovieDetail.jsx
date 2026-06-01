import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams, useNavigate } from 'react-router-dom';
import { Play, Share2, Star, ChevronLeft, ChevronRight, User, Film, MessageCircle, Image as ImageIcon } from 'lucide-react';
import VideoPlayer from '../components/VideoPlayer';

const MovieDetail = () => {
  const { i18n } = useTranslation();
  const { id } = useParams();
  const navigate = useNavigate();
  const currentLang = i18n.language;
  const [showPlayer, setShowPlayer] = useState(false);
  
  // Mock movie data
  const movie = {
    id: 1,
    title: { uz: 'SHERIKLAR III', ru: 'ПАРТНЁРЫ III', en: 'PARTNERS III' },
    background: 'https://images.unsplash.com/photo-1595769816263-9b910be24d5f?w=1920&h=600&fit=crop',
    poster: 'https://images.unsplash.com/photo-1595769816263-9b910be24d5f?w=300&h=450&fit=crop',
    videoUrl: 'https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8',
    year: 2026,
    genre: { uz: 'Komediya', ru: 'Комедия', en: 'Comedy' },
    country: { uz: 'Qirg\'iziston', ru: 'Кыргызстан', en: 'Kyrgyzstan' },
    age: '12+',
    duration: '124 daqiqa',
    imdb: 8.8,
    kp: 8.8,
    mtv: 8.8,
    description: {
      uz: 'Uchta do\'st yana yangi sarguzashtga kirishadilar. Bu safar ular biznes olamida o\'z o\'rnini topishga harakat qilishadi.',
      ru: 'Три друга снова отправляются в новое приключение. На этот раз они пытаются найти свое место в мире бизнеса.',
      en: 'Three friends embark on a new adventure again. This time they try to find their place in the business world.'
    }
  };
  
  // Oxshash filmlar
  const similarMovies = [
    { id: 2, title: { uz: 'Do\'stlar', ru: 'Друзья', en: 'Friends' }, poster: 'https://images.unsplash.com/photo-1574267432644-f610f5ac0b45?w=300&h=450&fit=crop', rating: 8.5, year: 2025 },
    { id: 3, title: { uz: 'Kulgu', ru: 'Смех', en: 'Laughter' }, poster: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop', rating: 8.2, year: 2024 },
    { id: 4, title: { uz: 'Biznesmen', ru: 'Бизнесмен', en: 'Businessman' }, poster: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop', rating: 7.9, year: 2025 },
    { id: 5, title: { uz: 'Uch do\'st', ru: 'Три друга', en: 'Three friends' }, poster: 'https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=300&h=450&fit=crop', rating: 8.1, year: 2024 },
    { id: 6, title: { uz: 'Komediya', ru: 'Комедия', en: 'Comedy' }, poster: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop', rating: 7.8, year: 2026 }
  ];
  
  // Aktyorlar
  const actors = [
    { id: 1, name: 'Aziz Muradillayev', role: { uz: 'Bosh rol', ru: 'Главная роль', en: 'Main role' }, photo: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop' },
    { id: 2, name: 'Sardor Rahimov', role: { uz: 'Ikkinchi rol', ru: 'Вторая роль', en: 'Second role' }, photo: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop' },
    { id: 3, name: 'Jasur Hamroyev', role: { uz: 'Yordamchi', ru: 'Помощник', en: 'Helper' }, photo: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200&h=200&fit=crop' },
    { id: 4, name: 'Madina Karimova', role: { uz: 'Ayol bosh rol', ru: 'Главная роль', en: 'Female lead' }, photo: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop' },
    { id: 5, name: 'Dilnoza Kubayeva', role: { uz: 'Yordamchi', ru: 'Помощник', en: 'Helper' }, photo: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop' }
  ];
  
  // Treylerlar
  const trailers = [
    { id: 1, title: { uz: 'Rasmiy treyder', ru: 'Трейлер', en: 'Trailer' }, thumbnail: 'https://images.unsplash.com/photo-1574267432644-f610f5ac0b45?w=400&h=225&fit=crop', duration: '2:34' },
    { id: 2, title: { uz: 'Sahna ortida', ru: 'За кадром', en: 'Behind scenes' }, thumbnail: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&h=225&fit=crop', duration: '5:12' },
    { id: 3, title: { uz: 'Intervyu', ru: 'Интервью', en: 'Interview' }, thumbnail: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400&h=225&fit=crop', duration: '8:45' }
  ];
  
  // Sharhlar
  const reviews = [
    { id: 1, user: 'Alisher', rating: 9, text: { uz: 'Ajoyib film!', ru: 'Отличный фильм!', en: 'Great movie!' }, date: '2026-05-15' },
    { id: 2, user: 'Malika', rating: 8, text: { uz: 'Hammaga yoqdi!', ru: 'Всем понравилось!', en: 'Everyone loved it!' }, date: '2026-05-14' },
    { id: 3, user: 'Sardor', rating: 10, text: { uz: 'Eng yaxshi!', ru: 'Лучший!', en: 'The best!' }, date: '2026-05-13' }
  ];
  
  // Tavsiya
  const recommended = [
    { id: 7, title: { uz: 'Kulgi', ru: 'Смех', en: 'Laugh' }, poster: 'https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=300&h=450&fit=crop', rating: 8.3 },
    { id: 8, title: { uz: 'Do\'stlik', ru: 'Дружба', en: 'Friend' }, poster: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop', rating: 8.6 },
    { id: 9, title: { uz: 'Sarguzasht', ru: 'Приключение', en: 'Adventure' }, poster: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop', rating: 8.4 },
    { id: 10, title: { uz: 'Hayot', ru: 'Жизнь', en: 'Life' }, poster: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop', rating: 8.7 }
  ];
  
  // Fotogalereya
  const gallery = [
    { id: 1, url: 'https://images.unsplash.com/photo-1574267432644-f610f5ac0b45?w=600&h=400&fit=crop' },
    { id: 2, url: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&h=400&fit=crop' },
    { id: 3, url: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=600&h=400&fit=crop' },
    { id: 4, url: 'https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=600&h=400&fit=crop' },
    { id: 5, url: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&h=400&fit=crop' }
  ];
  
  const Carousel = ({ children, title }) => {
    const containerRef = React.useRef(null);
    
    const scroll = (direction) => {
      const container = containerRef.current;
      if (container) {
        const scrollAmount = direction === 'left' ? -500 : 500;
        container.scrollBy({ 
          left: scrollAmount, 
          behavior: 'smooth' 
        });
      }
    };
    
    return (
      <div className="mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">{title}</h2>
          <div className="flex gap-2">
            <button 
              onClick={() => scroll('left')} 
              className="p-3 bg-gray-800 hover:bg-primary rounded-lg transition-all hover:scale-110 active:scale-95"
              aria-label="Scroll left"
            >
              <ChevronLeft className="text-white" size={24} />
            </button>
            <button 
              onClick={() => scroll('right')} 
              className="p-3 bg-gray-800 hover:bg-primary rounded-lg transition-all hover:scale-110 active:scale-95"
              aria-label="Scroll right"
            >
              <ChevronRight className="text-white" size={24} />
            </button>
          </div>
        </div>
        <div 
          ref={containerRef} 
          className="flex gap-4 overflow-x-scroll scrollbar-hide"
          style={{ 
            scrollBehavior: 'smooth',
            WebkitOverflowScrolling: 'touch'
          }}
        >
          {children}
        </div>
      </div>
    );
  };
  
  return (
    <div className="min-h-screen bg-dark text-white">
      {/* Hero */}
      <div className="relative h-[600px] bg-cover bg-center mt-24" style={{ backgroundImage: `url(${movie.background})` }}>
        <div className="absolute inset-0 bg-gradient-to-t from-dark via-dark/80 to-transparent" />
        <div className="relative max-w-7xl mx-auto px-4 h-full flex items-end pb-16">
          <div className="flex gap-8 w-full">
            <img src={movie.poster} alt={movie.title[currentLang]} className="hidden md:block w-[240px] h-[360px] rounded-xl shadow-2xl" />
            <div className="flex-1">
              <h1 className="text-5xl font-bold mb-4">{movie.title[currentLang]}</h1>
              <div className="flex gap-4 mb-4">
                <div className="bg-yellow-600 px-3 py-2 rounded flex items-center gap-2">
                  <span className="font-bold text-sm">IMDb</span>
                  <span className="text-xl font-bold">{movie.imdb}</span>
                </div>
                <div className="bg-orange-600 px-3 py-2 rounded flex items-center gap-2">
                  <span className="font-bold text-sm">КГ</span>
                  <span className="text-xl font-bold">{movie.kp}</span>
                </div>
                <div className="bg-purple-600 px-3 py-2 rounded flex items-center gap-2">
                  <span className="font-bold text-sm">MTV</span>
                  <span className="text-xl font-bold">{movie.mtv}</span>
                </div>
              </div>
              <p className="text-gray-300 text-lg mb-6">{movie.genre[currentLang]}, {movie.year}, {movie.age}, {movie.country[currentLang]}</p>
              <div className="flex gap-4">
                <button 
                  onClick={() => setShowPlayer(true)}
                  className="btn-primary flex items-center gap-3 px-8 py-4 text-lg"
                >
                  <Play size={24} fill="currentColor" />
                  {currentLang === 'uz' ? 'Ko\'rish' : currentLang === 'ru' ? 'Смотреть' : 'Watch'}
                </button>
                <button className="bg-gray-700 hover:bg-gray-600 px-8 py-4 rounded-lg flex items-center gap-3 text-lg transition-colors">
                  <Share2 size={24} />
                  {currentLang === 'uz' ? 'Ulashish' : currentLang === 'ru' ? 'Поделиться' : 'Share'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-4">{currentLang === 'uz' ? 'Tavsif' : currentLang === 'ru' ? 'Описание' : 'Description'}</h2>
          <p className="text-gray-300 text-lg leading-relaxed">{movie.description[currentLang]}</p>
        </div>
        
        {/* Aktyorlar */}
        <Carousel title={currentLang === 'uz' ? 'Aktyorlar' : currentLang === 'ru' ? 'Актёры' : 'Cast'}>
          {actors.map((actor) => (
            <div key={actor.id} className="flex-shrink-0 w-[180px]">
              <div className="relative group cursor-pointer mb-3">
                <img 
                  src={actor.photo} 
                  alt={actor.name} 
                  className="w-[180px] h-[180px] object-cover rounded-lg"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 rounded-lg transition-all flex items-center justify-center">
                  <User className="text-white opacity-0 group-hover:opacity-100 transition-opacity" size={48} />
                </div>
              </div>
              <h3 className="font-semibold text-white mb-1">{actor.name}</h3>
              <p className="text-sm text-gray-400">{actor.role[currentLang]}</p>
            </div>
          ))}
        </Carousel>
        
        {/* Treylerlar */}
        <Carousel title={currentLang === 'uz' ? 'Treylerlar' : currentLang === 'ru' ? 'Трейлеры' : 'Trailers'}>
          {trailers.map((t) => (
            <div key={t.id} className="flex-shrink-0 w-[400px] cursor-pointer group">
              <div className="relative aspect-video rounded-lg overflow-hidden mb-3">
                <img 
                  src={t.thumbnail} 
                  alt={t.title[currentLang]} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                />
                <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
                  <Play size={64} className="text-white" fill="currentColor" />
                </div>
                <div className="absolute bottom-3 right-3 bg-black bg-opacity-75 px-3 py-1 rounded text-sm font-bold">
                  {t.duration}
                </div>
              </div>
              <h3 className="font-semibold text-white">{t.title[currentLang]}</h3>
            </div>
          ))}
        </Carousel>
        
        {/* Sharhlar */}
        <Carousel title={currentLang === 'uz' ? 'Sharhlar' : currentLang === 'ru' ? 'Отзывы' : 'Reviews'}>
          {reviews.map((r) => (
            <div key={r.id} className="flex-shrink-0 w-[400px]">
              <div className="bg-dark-card p-6 rounded-lg h-full">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-black font-bold text-lg">
                      {r.user[0]}
                    </div>
                    <div>
                      <h3 className="font-semibold text-white">{r.user}</h3>
                      <p className="text-sm text-gray-400">{r.date}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1 bg-yellow-600 px-3 py-1 rounded">
                    <Star size={16} fill="currentColor" />
                    <span className="font-bold">{r.rating}</span>
                  </div>
                </div>
                <p className="text-gray-300 leading-relaxed">{r.text[currentLang]}</p>
              </div>
            </div>
          ))}
        </Carousel>
        
        {/* Oxshash */}
        <Carousel title={currentLang === 'uz' ? 'Oxshash filmlar' : currentLang === 'ru' ? 'Похожие' : 'Similar'}>
          {similarMovies.map((m) => (
            <div key={m.id} className="flex-shrink-0 w-[180px] cursor-pointer group">
              <div className="relative aspect-[2/3] rounded-lg overflow-hidden">
                <img src={m.poster} alt={m.title[currentLang]} className="w-full h-full object-cover group-hover:scale-105 transition" />
                <div className="absolute top-2 right-2 bg-yellow-600 px-2 py-1 rounded text-xs font-bold flex items-center gap-1">
                  <Star size={12} fill="currentColor" />{m.rating}
                </div>
              </div>
              <h3 className="mt-2 text-sm font-semibold line-clamp-2">{m.title[currentLang]}</h3>
              <p className="text-xs text-gray-400">{m.year}</p>
            </div>
          ))}
        </Carousel>
        
        {/* Tavsiya */}
        <Carousel title={currentLang === 'uz' ? 'Tavsiya etamiz' : currentLang === 'ru' ? 'Рекомендуем' : 'Recommended'}>
          {recommended.map((m) => (
            <div key={m.id} className="flex-shrink-0 w-[180px] cursor-pointer group">
              <div className="relative aspect-[2/3] rounded-lg overflow-hidden">
                <img src={m.poster} alt={m.title[currentLang]} className="w-full h-full object-cover group-hover:scale-105 transition" />
                <div className="absolute top-2 right-2 bg-primary px-2 py-1 rounded text-xs font-bold text-black">{m.rating}</div>
              </div>
              <h3 className="mt-2 text-sm font-semibold">{m.title[currentLang]}</h3>
            </div>
          ))}
        </Carousel>
        
        {/* Fotogalereya */}
        <Carousel title={currentLang === 'uz' ? 'Fotogalereya' : currentLang === 'ru' ? 'Фото' : 'Gallery'}>
          {gallery.map((p) => (
            <div key={p.id} className="flex-shrink-0 w-[350px] cursor-pointer group">
              <div className="aspect-video rounded-lg overflow-hidden">
                <img src={p.url} alt="Gallery" className="w-full h-full object-cover group-hover:scale-110 transition" />
              </div>
            </div>
          ))}
        </Carousel>
      </div>
      
      {/* Video Player */}
      {showPlayer && (
        <VideoPlayer 
          src={movie.videoUrl}
          poster={movie.poster}
          onClose={() => setShowPlayer(false)}
        />
      )}
    </div>
  );
};

export default MovieDetail;
