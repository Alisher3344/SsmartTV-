import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Search, X, SlidersHorizontal, Play } from 'lucide-react';

const Series = () => {
  const { t, i18n } = useTranslation();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeGenre, setActiveGenre] = useState('barchasi');
  const currentLang = i18n.language;
  
  const genres = [
    { id: 'barchasi', label: { uz: 'Barchasi', ru: 'Все' } },
    { id: 'drama', label: { uz: 'Drama', ru: 'Драма' } },
    { id: 'komediya', label: { uz: 'Komediya', ru: 'Комедия' } },
    { id: 'triller', label: { uz: 'Triller', ru: 'Триллер' } },
    { id: 'detektiv', label: { uz: 'Detektiv', ru: 'Детектив' } },
    { id: 'kriminal', label: { uz: 'Kriminal', ru: 'Криминал' } },
    { id: 'melodrama', label: { uz: 'Melodrama', ru: 'Мелодрама' } },
    { id: 'fantastika', label: { uz: 'Fantastika', ru: 'Фантастика' } },
    { id: 'fentezi', label: { uz: 'Fentezi', ru: 'Фэнтези' } },
    { id: 'sarguzasht', label: { uz: 'Sarguzasht', ru: 'Приключения' } },
    { id: 'tarixiy', label: { uz: 'Tarixiy', ru: 'Исторический' } },
    { id: 'harbiy', label: { uz: 'Harbiy', ru: 'Военный' } },
    { id: 'oilaviy', label: { uz: 'Oilaviy', ru: 'Семейный' } },
    { id: 'yoshlar', label: { uz: 'Yoshlar', ru: 'Молодёжный' } },
    { id: 'koreys', label: { uz: 'Koreys Doramalari', ru: 'Корейские дорамы' } },
    { id: 'turk', label: { uz: 'Turk Seriallari', ru: 'Турецкие сериалы' } },
  ];
  
  const series = [
    {
      id: 1,
      title: { uz: 'Qalb izlari', ru: 'Следы сердца' },
      year: 2024,
      rating: 8.5,
      genre: 'drama',
      seasons: 2,
      episodes: 45,
      country: { uz: "O'zbekiston", ru: 'Узбекистан' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=450&fit=crop',
    },
    {
      id: 2,
      title: { uz: 'Muhabbat va jazo', ru: 'Любовь и наказание' },
      year: 2023,
      rating: 8.8,
      genre: 'turk',
      seasons: 3,
      episodes: 120,
      country: { uz: 'Turkiya', ru: 'Турция' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop',
    },
    {
      id: 3,
      title: { uz: 'Squid Game', ru: 'Игра в кальмара' },
      year: 2021,
      rating: 9.2,
      genre: 'koreys',
      seasons: 2,
      episodes: 17,
      country: { uz: 'Janubiy Koreya', ru: 'Южная Корея' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=300&h=450&fit=crop',
    },
    {
      id: 4,
      title: { uz: 'Sherlock', ru: 'Шерлок' },
      year: 2010,
      rating: 9.1,
      genre: 'detektiv',
      seasons: 4,
      episodes: 13,
      country: { uz: 'Buyuk Britaniya', ru: 'Великобритания' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1560169897-fc0cdbdfa4d5?w=300&h=450&fit=crop',
    },
    {
      id: 5,
      title: { uz: 'Breaking Bad', ru: 'Во все тяжкие' },
      year: 2008,
      rating: 9.5,
      genre: 'kriminal',
      seasons: 5,
      episodes: 62,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop',
    },
    {
      id: 6,
      title: { uz: 'Game of Thrones', ru: 'Игра престолов' },
      year: 2011,
      rating: 9.3,
      genre: 'fentezi',
      seasons: 8,
      episodes: 73,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=450&fit=crop',
    },
    {
      id: 7,
      title: { uz: 'Stranger Things', ru: 'Очень странные дела' },
      year: 2016,
      rating: 8.7,
      genre: 'fantastika',
      seasons: 4,
      episodes: 34,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=300&h=450&fit=crop',
    },
    {
      id: 8,
      title: { uz: 'Friends', ru: 'Друзья' },
      year: 1994,
      rating: 8.9,
      genre: 'komediya',
      seasons: 10,
      episodes: 236,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=300&h=450&fit=crop',
    },
    {
      id: 9,
      title: { uz: 'Chernobyl', ru: 'Чернобыль' },
      year: 2019,
      rating: 9.4,
      genre: 'tarixiy',
      seasons: 1,
      episodes: 5,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1542204165-65bf26472b9b?w=300&h=450&fit=crop',
    },
    {
      id: 10,
      title: { uz: 'Band of Brothers', ru: 'Братья по оружию' },
      year: 2001,
      rating: 9.4,
      genre: 'harbiy',
      seasons: 1,
      episodes: 10,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=300&h=450&fit=crop',
    },
    {
      id: 11,
      title: { uz: 'Oilaviy qadriyatlar', ru: 'Семейные ценности' },
      year: 2023,
      rating: 7.8,
      genre: 'oilaviy',
      seasons: 1,
      episodes: 24,
      country: { uz: "O'zbekiston", ru: 'Узбекистан' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=300&h=450&fit=crop',
    },
    {
      id: 12,
      title: { uz: 'Yosh yuraklar', ru: 'Молодые сердца' },
      year: 2024,
      rating: 7.5,
      genre: 'yoshlar',
      seasons: 1,
      episodes: 16,
      country: { uz: "O'zbekiston", ru: 'Узбекистан' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=300&h=450&fit=crop',
    },
    {
      id: 13,
      title: { uz: 'Sirli qishloq', ru: 'Таинственная деревня' },
      year: 2024,
      rating: 8.2,
      genre: 'triller',
      seasons: 1,
      episodes: 20,
      country: { uz: 'Rossiya', ru: 'Россия' },
      status: { uz: 'Tugallangan', ru: 'Завершён' },
      image: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop',
    },
    {
      id: 14,
      title: { uz: "Ishq va intiqom", ru: 'Любовь и месть' },
      year: 2023,
      rating: 8.6,
      genre: 'melodrama',
      seasons: 2,
      episodes: 80,
      country: { uz: 'Turkiya', ru: 'Турция' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=450&fit=crop',
    },
    {
      id: 15,
      title: { uz: 'Sarguzashtlar dunyosi', ru: 'Мир приключений' },
      year: 2024,
      rating: 7.9,
      genre: 'sarguzasht',
      seasons: 1,
      episodes: 12,
      country: { uz: 'AQSH', ru: 'США' },
      status: { uz: 'Davom etmoqda', ru: 'Продолжается' },
      image: 'https://images.unsplash.com/photo-1511884642898-4c92249e20b6?w=300&h=450&fit=crop',
    },
  ];
  
  const filteredSeries = series.filter(item => {
    const matchesSearch = item.title[currentLang].toLowerCase().includes(searchQuery.toLowerCase());
    const matchesGenre = activeGenre === 'barchasi' || item.genre === activeGenre;
    return matchesSearch && matchesGenre;
  });
  
  return (
    <div className="min-h-screen bg-dark text-white pt-8 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <div className="mb-6 flex items-center gap-2 text-sm">
          <a href="/" className="text-gray-400 hover:text-white transition-colors">
            {currentLang === 'uz' ? 'Bosh sahifa' : 'Главная'}
          </a>
          <span className="text-gray-600">/</span>
          <span className="text-white font-medium">
            {currentLang === 'uz' ? 'Seriallar' : 'Сериалы'}
          </span>
        </div>
        
        {/* Page Title */}
        <h1 className="text-4xl font-bold mb-8">
          {currentLang === 'uz' ? 'Seriallar' : 'Сериалы'}
        </h1>
        
        {/* Search */}
        <div className="mb-8 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder={currentLang === 'uz' ? "Serial nomini kiriting..." : "Введите название сериала..."}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-dark-card border border-gray-700 rounded-lg pl-12 pr-10 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-primary transition-colors"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
              >
                <X size={20} />
              </button>
            )}
          </div>
          
          <button className="flex items-center gap-2 bg-dark-card hover:bg-gray-800 px-4 py-3 rounded-lg transition-colors">
            <SlidersHorizontal size={20} />
            <span>{currentLang === 'uz' ? 'Filtrlar' : 'Фильтры'}</span>
          </button>
        </div>
        
        {/* Genre Filters */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">
            {currentLang === 'uz' ? 'Janr' : 'Жанр'}
          </h2>
          <div className="flex flex-wrap gap-3">
            {genres.map((genre) => (
              <button
                key={genre.id}
                onClick={() => setActiveGenre(genre.id)}
                className={`px-5 py-2 rounded-full font-medium transition-all duration-300 ${
                  activeGenre === genre.id
                    ? 'bg-primary text-black'
                    : 'bg-dark-card text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                {genre.label[currentLang]}
              </button>
            ))}
          </div>
        </div>
        
        {/* Series Count */}
        <div className="mb-6 flex items-center justify-between">
          <p className="text-gray-400">
            {currentLang === 'uz' ? 'Topildi' : 'Найдено'}: <span className="text-white font-semibold">{filteredSeries.length}</span> {currentLang === 'uz' ? 'ta serial' : 'сериалов'}
          </p>
          
          <select className="bg-dark-card border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary">
            <option value="popular">{currentLang === 'uz' ? 'Mashhur' : 'Популярные'}</option>
            <option value="new">{currentLang === 'uz' ? 'Yangi' : 'Новые'}</option>
            <option value="rating">{currentLang === 'uz' ? 'Reyting' : 'Рейтинг'}</option>
            <option value="year">{currentLang === 'uz' ? 'Yil' : 'Год'}</option>
          </select>
        </div>
        
        {/* Series Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {filteredSeries.map((item) => (
            <div key={item.id} className="group cursor-pointer">
              <div className="relative aspect-[2/3] rounded-lg overflow-hidden mb-3">
                <img 
                  src={item.image} 
                  alt={item.title[currentLang]}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
                
                {/* Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Play size={48} className="text-primary" fill="currentColor" />
                  </div>
                  <div className="absolute bottom-0 left-0 right-0 p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="bg-primary text-black text-xs font-bold px-2 py-1 rounded">
                        {item.rating}
                      </span>
                      <span className="bg-dark text-white text-xs px-2 py-1 rounded">
                        {item.seasons} {currentLang === 'uz' ? 'fasl' : 'сезона'}
                      </span>
                    </div>
                  </div>
                </div>
                
                {/* Top badges */}
                <div className="absolute top-2 right-2 flex flex-col gap-1">
                  <span className="bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
                    {item.year}
                  </span>
                  <span className={`text-white text-xs px-2 py-1 rounded ${
                    item.status[currentLang].includes('Davom') || item.status[currentLang].includes('Продолжается')
                      ? 'bg-green-600'
                      : 'bg-gray-600'
                  }`}>
                    {item.status[currentLang].includes('Davom') || item.status[currentLang].includes('Продолжается')
                      ? (currentLang === 'uz' ? 'Davom' : 'Идёт')
                      : (currentLang === 'uz' ? 'Tugagan' : 'Завершён')
                    }
                  </span>
                </div>
              </div>
              
              <h3 className="font-semibold text-sm mb-1 line-clamp-2 group-hover:text-primary transition-colors">
                {item.title[currentLang]}
              </h3>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <span>{item.country[currentLang]}</span>
                <span>•</span>
                <span>{item.episodes} {currentLang === 'uz' ? 'qism' : 'серий'}</span>
              </div>
            </div>
          ))}
        </div>
        
        {/* No Results */}
        {filteredSeries.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg mb-4">
              {currentLang === 'uz' ? 'Seriallar topilmadi' : 'Сериалы не найдены'}
            </p>
            <button 
              onClick={() => {
                setSearchQuery('');
                setActiveGenre('barchasi');
              }}
              className="btn-primary"
            >
              {currentLang === 'uz' ? 'Filtrlarni tozalash' : 'Очистить фильтры'}
            </button>
          </div>
        )}
        
        {/* Load More */}
        {filteredSeries.length > 0 && (
          <div className="mt-12 text-center">
            <button className="btn-primary px-12 py-3">
              {currentLang === 'uz' ? 'Ko\'proq yuklash' : 'Загрузить еще'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Series;
