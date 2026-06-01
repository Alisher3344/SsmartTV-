import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Search, X, Star, Play } from 'lucide-react';

const Kids = () => {
  const { t, i18n } = useTranslation();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('barchasi');
  const currentLang = i18n.language;
  
  const categories = [
    { id: 'barchasi', label: { uz: 'Barchasi', ru: 'Все' } },
    { id: 'multfilm', label: { uz: 'Multfilmlar', ru: 'Мультфильмы' } },
    { id: 'ertaklar', label: { uz: 'Ertaklar', ru: 'Сказки' } },
    { id: 'talimiy', label: { uz: "Ta'limiy videolar", ru: 'Образовательные' } },
    { id: 'oyinlar', label: { uz: "O'yinlar", ru: 'Игры' } },
    { id: 'qoshiqlar', label: { uz: "Qo'shiqlar", ru: 'Песни' } },
    { id: 'serial', label: { uz: 'Animatsiya seriallar', ru: 'Анимационные сериалы' } },
    { id: 'rang', label: { uz: "Rang berish", ru: 'Раскраски' } },
    { id: 'test', label: { uz: 'Qiziqarli testlar', ru: 'Интересные тесты' } },
    { id: 'interaktiv', label: { uz: 'Interaktiv darslar', ru: 'Интерактивные уроки' } },
    { id: 'film', label: { uz: 'Bolalar filmlari', ru: 'Детские фильмы' } },
    { id: 'yangi', label: { uz: 'Yangi multfilmlar', ru: 'Новые мультфильмы' } },
    { id: 'qahramon', label: { uz: 'Mashhur qahramonlar', ru: 'Популярные герои' } },
    { id: 'hayvon', label: { uz: 'Hayvonlar olami', ru: 'Мир животных' } },
    { id: 'alifbo', label: { uz: "ABC o'rganish", ru: 'Изучение азбуки' } },
    { id: 'raqam', label: { uz: 'Raqamlar va matematika', ru: 'Цифры и математика' } },
  ];
  
  const content = [
    // Multfilmlar
    {
      id: 1,
      title: { uz: 'Paw Patrol', ru: 'Щенячий патруль' },
      category: 'multfilm',
      age: '3+',
      rating: 4.8,
      duration: '22 daqiqa',
      episodes: 250,
      image: 'https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=300&h=450&fit=crop',
      popular: true,
    },
    {
      id: 2,
      title: { uz: 'Frozen', ru: 'Холодное сердце' },
      category: 'film',
      age: '6+',
      rating: 4.9,
      duration: '102 daqiqa',
      image: 'https://images.unsplash.com/photo-1551269901-5c5e14c25df7?w=300&h=450&fit=crop',
      popular: true,
    },
    {
      id: 3,
      title: { uz: 'Mickey Mouse Clubhouse', ru: 'Клуб Микки Мауса' },
      category: 'serial',
      age: '2+',
      rating: 4.7,
      duration: '24 daqiqa',
      episodes: 125,
      image: 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=300&h=450&fit=crop',
      popular: true,
    },
    
    // Ertaklar
    {
      id: 4,
      title: { uz: 'Uch ayiq', ru: 'Три медведя' },
      category: 'ertaklar',
      age: '3+',
      rating: 4.6,
      duration: '15 daqiqa',
      image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=450&fit=crop',
    },
    {
      id: 5,
      title: { uz: 'Toshbaqa va quyon', ru: 'Черепаха и заяц' },
      category: 'ertaklar',
      age: '3+',
      rating: 4.5,
      duration: '12 daqiqa',
      image: 'https://images.unsplash.com/photo-1516192518150-0d8fee5425e3?w=300&h=450&fit=crop',
    },
    
    // Ta'limiy
    {
      id: 6,
      title: { uz: 'ABC bilan tanishing', ru: 'Знакомство с азбукой' },
      category: 'alifbo',
      age: '3+',
      rating: 4.8,
      duration: '30 daqiqa',
      image: 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=300&h=450&fit=crop',
    },
    {
      id: 7,
      title: { uz: 'Raqamlarni o\'rganamiz', ru: 'Учим цифры' },
      category: 'raqam',
      age: '3+',
      rating: 4.7,
      duration: '25 daqiqa',
      image: 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300&h=450&fit=crop',
    },
    {
      id: 8,
      title: { uz: 'Ingliz tili bolalar uchun', ru: 'Английский для детей' },
      category: 'talimiy',
      age: '5+',
      rating: 4.6,
      duration: '20 daqiqa',
      episodes: 50,
      image: 'https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=300&h=450&fit=crop',
    },
    
    // O'yinlar va Qo'shiqlar
    {
      id: 9,
      title: { uz: 'Rang topish o\'yini', ru: 'Игра угадай цвет' },
      category: 'oyinlar',
      age: '3+',
      rating: 4.5,
      duration: 'Interaktiv',
      image: 'https://images.unsplash.com/photo-1596464716127-f2a82984de30?w=300&h=450&fit=crop',
    },
    {
      id: 10,
      title: { uz: 'Bolalar qo\'shiqlari', ru: 'Детские песенки' },
      category: 'qoshiqlar',
      age: '2+',
      rating: 4.9,
      duration: '3-5 daqiqa',
      episodes: 100,
      image: 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=300&h=450&fit=crop',
    },
    
    // Rang berish
    {
      id: 11,
      title: { uz: 'Hayvonlarni bo\'yash', ru: 'Раскрась животных' },
      category: 'rang',
      age: '3+',
      rating: 4.4,
      duration: 'Interaktiv',
      image: 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=300&h=450&fit=crop',
    },
    
    // Testlar
    {
      id: 12,
      title: { uz: 'Hayvonlarni tanish', ru: 'Угадай животное' },
      category: 'test',
      age: '4+',
      rating: 4.6,
      duration: '15 daqiqa',
      image: 'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=300&h=450&fit=crop',
    },
    
    // Interaktiv darslar
    {
      id: 13,
      title: { uz: 'Matematik sarguzashtlar', ru: 'Математические приключения' },
      category: 'interaktiv',
      age: '5+',
      rating: 4.7,
      duration: '30 daqiqa',
      image: 'https://images.unsplash.com/photo-1596464716127-f2a82984de30?w=300&h=450&fit=crop',
    },
    
    // Yangi multfilmlar
    {
      id: 14,
      title: { uz: 'Sonic 2', ru: 'Соник 2' },
      category: 'yangi',
      age: '6+',
      rating: 4.8,
      duration: '122 daqiqa',
      image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop',
      popular: true,
    },
    {
      id: 15,
      title: { uz: 'Encanto', ru: 'Энканто' },
      category: 'yangi',
      age: '6+',
      rating: 4.9,
      duration: '102 daqiqa',
      image: 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop',
      popular: true,
    },
    
    // Mashhur qahramonlar
    {
      id: 16,
      title: { uz: 'Spider-Man (bolalar)', ru: 'Человек-паук (детский)' },
      category: 'qahramon',
      age: '6+',
      rating: 4.7,
      duration: '22 daqiqa',
      episodes: 50,
      image: 'https://images.unsplash.com/photo-1635805737707-575885ab0820?w=300&h=450&fit=crop',
    },
    
    // Hayvonlar olami
    {
      id: 17,
      title: { uz: 'Hayvonlar dunyosi', ru: 'Мир животных' },
      category: 'hayvon',
      age: '4+',
      rating: 4.8,
      duration: '25 daqiqa',
      episodes: 30,
      image: 'https://images.unsplash.com/photo-1516728043615-f1e7e02e3c42?w=300&h=450&fit=crop',
    },
    {
      id: 18,
      title: { uz: 'Okean sirlari', ru: 'Тайны океана' },
      category: 'hayvon',
      age: '5+',
      rating: 4.7,
      duration: '30 daqiqa',
      image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=300&h=450&fit=crop',
    },
  ];
  
  const filteredContent = content.filter(item => {
    const matchesSearch = item.title[currentLang].toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeCategory === 'barchasi' || item.category === activeCategory;
    return matchesSearch && matchesCategory;
  });
  
  const popularContent = content.filter(item => item.popular);
  
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
            {currentLang === 'uz' ? 'Bolalar uchun' : 'Детям'}
          </span>
        </div>
        
        {/* Page Title with emoji */}
        <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
          <span>🎈</span>
          {currentLang === 'uz' ? 'Bolalar uchun' : 'Детям'}
        </h1>
        <p className="text-gray-400 mb-8">
          {currentLang === 'uz' ? 'Xavfsiz va qiziqarli kontent bolalar uchun' : 'Безопасный и интересный контент для детей'}
        </p>
        
        {/* Search */}
        <div className="mb-8">
          <div className="relative max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder={currentLang === 'uz' ? "Qidirish..." : "Поиск..."}
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
        </div>
        
        {/* Popular Section */}
        {activeCategory === 'barchasi' && !searchQuery && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <Star className="text-yellow-400" fill="currentColor" size={24} />
              {currentLang === 'uz' ? 'Mashhur' : 'Популярные'}
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {popularContent.map((item) => (
                <div key={item.id} className="group cursor-pointer">
                  <div className="relative aspect-[2/3] rounded-xl overflow-hidden mb-3 border-4 border-transparent group-hover:border-primary transition-all duration-300">
                    <img 
                      src={item.image} 
                      alt={item.title[currentLang]}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <Play size={48} className="text-white" fill="currentColor" />
                      </div>
                    </div>
                    <div className="absolute top-2 left-2">
                      <span className="bg-yellow-400 text-black text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
                        <Star size={12} fill="currentColor" />
                        {item.rating}
                      </span>
                    </div>
                    <div className="absolute top-2 right-2">
                      <span className="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                        {item.age}
                      </span>
                    </div>
                  </div>
                  <h3 className="font-semibold text-sm mb-1 line-clamp-2">
                    {item.title[currentLang]}
                  </h3>
                  <p className="text-xs text-gray-400">{item.duration}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Category Filters */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <span>🎯</span>
            {currentLang === 'uz' ? 'Kategoriyalar' : 'Категории'}
          </h2>
          <div className="flex flex-wrap gap-3">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`px-5 py-2 rounded-full font-medium transition-all duration-300 ${
                  activeCategory === category.id
                    ? 'bg-primary text-black'
                    : 'bg-dark-card text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                {category.label[currentLang]}
              </button>
            ))}
          </div>
        </div>
        
        {/* Content Grid */}
        {filteredContent.length > 0 && (
          <>
            <div className="mb-6">
              <p className="text-gray-400">
                {currentLang === 'uz' ? 'Topildi' : 'Найдено'}: <span className="text-white font-semibold">{filteredContent.length}</span> {currentLang === 'uz' ? 'ta kontent' : 'контента'}
              </p>
            </div>
            
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
              {filteredContent.map((item) => (
                <div key={item.id} className="group cursor-pointer">
                  <div className="relative aspect-[2/3] rounded-xl overflow-hidden mb-3 border-2 border-transparent group-hover:border-primary transition-all duration-300">
                    <img 
                      src={item.image} 
                      alt={item.title[currentLang]}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <div className="absolute inset-0 flex items-center justify-center">
                        <Play size={40} className="text-white" fill="currentColor" />
                      </div>
                      {item.rating && (
                        <div className="absolute bottom-3 left-3">
                          <span className="bg-yellow-400 text-black text-xs font-bold px-2 py-1 rounded-full flex items-center gap-1">
                            <Star size={12} fill="currentColor" />
                            {item.rating}
                          </span>
                        </div>
                      )}
                    </div>
                    <div className="absolute top-2 right-2">
                      <span className="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                        {item.age}
                      </span>
                    </div>
                  </div>
                  <h3 className="font-semibold text-sm mb-1 line-clamp-2 group-hover:text-primary transition-colors">
                    {item.title[currentLang]}
                  </h3>
                  <p className="text-xs text-gray-400">{item.duration}</p>
                  {item.episodes && (
                    <p className="text-xs text-gray-500">{item.episodes} {currentLang === 'uz' ? 'qism' : 'серий'}</p>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
        
        {/* No Results */}
        {filteredContent.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">😢</div>
            <p className="text-gray-400 text-lg mb-4">
              {currentLang === 'uz' ? 'Hech narsa topilmadi' : 'Ничего не найдено'}
            </p>
            <button 
              onClick={() => {
                setSearchQuery('');
                setActiveCategory('barchasi');
              }}
              className="btn-primary"
            >
              {currentLang === 'uz' ? 'Barchasini ko\'rish' : 'Показать все'}
            </button>
          </div>
        )}
        
        {/* Load More */}
        {filteredContent.length > 0 && (
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

export default Kids;
