import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Search, X, SlidersHorizontal } from 'lucide-react';
import { Link } from 'react-router-dom';

const Movies = () => {
  const { t, i18n } = useTranslation();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeGenre, setActiveGenre] = useState('barchasi');
  const currentLang = i18n.language;
  
  const genres = [
    { id: 'barchasi', label: { uz: 'Barchasi', ru: 'Все' } },
    { id: 'boevik', label: { uz: 'Boevik', ru: 'Боевик' } },
    { id: 'drama', label: { uz: 'Drama', ru: 'Драма' } },
    { id: 'komediya', label: { uz: 'Komediya', ru: 'Комедия' } },
    { id: 'melodrama', label: { uz: 'Melodrama', ru: 'Мелодрама' } },
    { id: 'triller', label: { uz: 'Triller', ru: 'Триллер' } },
    { id: 'detektiv', label: { uz: 'Detektiv', ru: 'Детектив' } },
    { id: 'qorqinchli', label: { uz: "Qo'rqinchli", ru: 'Ужасы' } },
    { id: 'fantastika', label: { uz: 'Fantastika', ru: 'Фантастика' } },
    { id: 'fentezi', label: { uz: 'Fentezi', ru: 'Фэнтези' } },
    { id: 'sarguzasht', label: { uz: 'Sarguzasht', ru: 'Приключения' } },
    { id: 'kriminal', label: { uz: 'Kriminal', ru: 'Криминал' } },
    { id: 'biografiya', label: { uz: 'Biografiya', ru: 'Биография' } },
    { id: 'tarixiy', label: { uz: 'Tarixiy', ru: 'Исторический' } },
    { id: 'harbiy', label: { uz: 'Harbiy', ru: 'Военный' } },
    { id: 'hujjatli', label: { uz: 'Hujjatli', ru: 'Документальный' } },
    { id: 'oilaviy', label: { uz: 'Oilaviy', ru: 'Семейный' } },
    { id: 'multfilm', label: { uz: 'Multfilm', ru: 'Мультфильм' } },
    { id: 'anime', label: { uz: 'Anime', ru: 'Аниме' } },
    { id: 'musiqiy', label: { uz: 'Musiqiy', ru: 'Музыкальный' } },
    { id: 'sport', label: { uz: 'Sport', ru: 'Спортивный' } },
  ];
  
  const movies = [
    {
      id: 1,
      title: { uz: 'SHERIKLAR III', ru: 'ШЕРИКLAR III' },
      year: 2026,
      rating: 8.8,
      genre: 'komediya',
      country: { uz: 'Qyrgyzstan', ru: 'Кыргызстан' },
      age: '12+',
      image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop',
    },
    {
      id: 2,
      title: { uz: '34 yillik o\'rzu', ru: '34-летняя мечта' },
      year: 2024,
      rating: 7.5,
      genre: 'drama',
      country: { uz: 'O\'zbekiston', ru: 'Узбекистан' },
      age: '16+',
      image: 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop',
    },
    {
      id: 3,
      title: { uz: 'KRIK 7', ru: 'КРИК 7' },
      year: 2025,
      rating: 7.2,
      genre: 'qorqinchli',
      country: { uz: 'AQSH', ru: 'США' },
      age: '18+',
      image: 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=300&h=450&fit=crop',
    },
    {
      id: 4,
      title: { uz: 'Salom Yevropa!', ru: 'Привет Европа!' },
      year: 2024,
      rating: 8.1,
      genre: 'komediya',
      country: { uz: 'Rossiya', ru: 'Россия' },
      age: '12+',
      image: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop',
    },
    {
      id: 5,
      title: { uz: 'Jannat 2', ru: 'Джаннат 2' },
      year: 2024,
      rating: 8.5,
      genre: 'oilaviy',
      country: { uz: 'O\'zbekiston', ru: 'Узбекистан' },
      age: '12+',
      image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop',
    },
    {
      id: 6,
      title: { uz: 'Tez va g\'azabli 10', ru: 'Форсаж 10' },
      year: 2023,
      rating: 7.8,
      genre: 'boevik',
      country: { uz: 'AQSH', ru: 'США' },
      age: '16+',
      image: 'https://images.unsplash.com/photo-1542204165-65bf26472b9b?w=300&h=450&fit=crop',
    },
    {
      id: 7,
      title: { uz: 'Interstellar', ru: 'Интерстеллар' },
      year: 2014,
      rating: 9.1,
      genre: 'fantastika',
      country: { uz: 'AQSH', ru: 'США' },
      age: '12+',
      image: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=300&h=450&fit=crop',
    },
    {
      id: 8,
      title: { uz: 'Priguny', ru: 'Прыгуны' },
      year: 2024,
      rating: 7.6,
      genre: 'multfilm',
      country: { uz: 'Rossiya', ru: 'Россия' },
      age: '6+',
      image: 'https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=300&h=450&fit=crop',
    },
    {
      id: 9,
      title: { uz: 'Yolg\'izlar klubi', ru: 'Клуб одиночек' },
      year: 2023,
      rating: 7.9,
      genre: 'melodrama',
      country: { uz: 'Hindiston', ru: 'Индия' },
      age: '16+',
      image: 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=450&fit=crop',
    },
    {
      id: 10,
      title: { uz: 'Detektiv Shorlok', ru: 'Детектив Шерлок' },
      year: 2024,
      rating: 8.3,
      genre: 'detektiv',
      country: { uz: 'Buyuk Britaniya', ru: 'Великобритания' },
      age: '12+',
      image: 'https://images.unsplash.com/photo-1560169897-fc0cdbdfa4d5?w=300&h=450&fit=crop',
    },
    {
      id: 11,
      title: { uz: 'O\'rmondagi sarguzasht', ru: 'Приключения в лесу' },
      year: 2024,
      rating: 7.4,
      genre: 'sarguzasht',
      country: { uz: 'Kanada', ru: 'Канада' },
      age: '6+',
      image: 'https://images.unsplash.com/photo-1511884642898-4c92249e20b6?w=300&h=450&fit=crop',
    },
    {
      id: 12,
      title: { uz: 'Naruto: Film', ru: 'Наруто: Фильм' },
      year: 2023,
      rating: 8.7,
      genre: 'anime',
      country: { uz: 'Yaponiya', ru: 'Япония' },
      age: '12+',
      image: 'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=300&h=450&fit=crop',
    },
  ];
  
  const filteredMovies = movies.filter(movie => {
    const matchesSearch = movie.title[currentLang].toLowerCase().includes(searchQuery.toLowerCase());
    const matchesGenre = activeGenre === 'barchasi' || movie.genre === activeGenre;
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
            {currentLang === 'uz' ? 'Filmlar' : 'Фильмы'}
          </span>
        </div>
        
        {/* Page Title */}
        <h1 className="text-4xl font-bold mb-8">
          {currentLang === 'uz' ? 'Filmlar' : 'Фильмы'}
        </h1>
        
        {/* Search */}
        <div className="mb-8 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder={currentLang === 'uz' ? "Film nomini kiriting..." : "Введите название фильма..."}
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
        
        {/* Movies Count */}
        <div className="mb-6 flex items-center justify-between">
          <p className="text-gray-400">
            {currentLang === 'uz' ? 'Topildi' : 'Найдено'}: <span className="text-white font-semibold">{filteredMovies.length}</span> {currentLang === 'uz' ? 'ta film' : 'фильмов'}
          </p>
          
          <select className="bg-dark-card border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary">
            <option value="popular">{currentLang === 'uz' ? 'Mashhur' : 'Популярные'}</option>
            <option value="new">{currentLang === 'uz' ? 'Yangi' : 'Новые'}</option>
            <option value="rating">{currentLang === 'uz' ? 'Reyting' : 'Рейтинг'}</option>
            <option value="year">{currentLang === 'uz' ? 'Yil' : 'Год'}</option>
          </select>
        </div>
        
        {/* Movies Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          {filteredMovies.map((movie) => (
            <Link key={movie.id} to={`/movie/${movie.id}`} className="group cursor-pointer">
              <div className="relative aspect-[2/3] rounded-lg overflow-hidden mb-3">
                <img 
                  src={movie.image} 
                  alt={movie.title[currentLang]}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
                
                {/* Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="absolute bottom-0 left-0 right-0 p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="bg-primary text-black text-xs font-bold px-2 py-1 rounded">
                        {movie.rating}
                      </span>
                      <span className="bg-red-600 text-white text-xs font-bold px-2 py-1 rounded">
                        {movie.age}
                      </span>
                    </div>
                  </div>
                </div>
                
                {/* Top badges */}
                <div className="absolute top-2 right-2">
                  <span className="bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
                    {movie.year}
                  </span>
                </div>
              </div>
              
              <h3 className="font-semibold text-sm mb-1 line-clamp-2 group-hover:text-primary transition-colors">
                {movie.title[currentLang]}
              </h3>
              <p className="text-xs text-gray-400">
                {movie.country[currentLang]}
              </p>
            </Link>
          ))}
        </div>
        
        {/* No Results */}
        {filteredMovies.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg mb-4">
              {currentLang === 'uz' ? 'Filmlar topilmadi' : 'Фильмы не найдены'}
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
        {filteredMovies.length > 0 && (
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

export default Movies;
