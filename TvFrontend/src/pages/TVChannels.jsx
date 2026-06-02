import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Search, List, Radio as RadioIcon, PlaySquare, X } from 'lucide-react';
import VideoPlayer from '../components/VideoPlayer';
import apiClient, { absoluteUrl } from '../api/client';

const TVChannels = () => {
  const { t, i18n } = useTranslation();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCountry, setActiveCountry] = useState('ozbekiston'); // asosiy: davlat
  const [activeGenre, setActiveGenre] = useState('barcasi'); // sub: janr
  const [showPlayer, setShowPlayer] = useState(false);
  const [selectedChannel, setSelectedChannel] = useState(null);
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  // TV pulti uslubidagi navigatsiya holati
  const [focusIndex, setFocusIndex] = useState(0);
  const [showMenuBar, setShowMenuBar] = useState(false);
  const cardRefs = useRef([]);
  const currentLang = i18n.language;

  useEffect(() => {
    let active = true;
    // Backend limiti 100 — barcha kanallarni olish uchun sahifalab yuklaymiz
    // (davlatlar ko'paygani sayin jami 100 dan oshadi).
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
        // Backend maydonlarini komponent kutgan shaklga moslash
        setChannels(
          list.map((c) => ({
            id: c.slug,
            name: c.name,
            logo: c.logo,
            currentShow: c.current_show,
            time: c.time,
            description: { uz: c.description_uz, ru: c.description_ru },
            image: c.image,
            // Backend country/genre obyekt sifatida qaytaradi (slug bo'yicha filter)
            category: c.country?.slug, // davlat: ozbekiston/rossiya/usa/turkiya/...
            subcategory: c.genre?.slug, // janr
            country: c.country, // {slug, name_uz, name_ru, ...} — kartochkada ko'rsatish uchun
            genre: c.genre, // {slug, name_uz, name_ru, ...}
            // Live kanal uchun backend proxy URL beradi: /api/v1/stream/{slug}.
            // stream_url public javobda yashirilgan, shuning uchun playback_url'dan olamiz.
            videoUrl: c.playback_url ? absoluteUrl(c.playback_url) : null,
          }))
        );
      })
      .catch(() => active && setChannels([]))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);
  
  // Asosiy filtr — davlat (kanal.category). "Barchasi" yo'q: standart O'zbekiston.
  const countries = [
    { id: 'ozbekiston', label: { uz: "O'zbekiston", ru: 'Узбекистан' } },
    { id: 'rossiya', label: { uz: 'Rossiya', ru: 'Россия' } },
    { id: 'usa', label: { uz: 'AQSH', ru: 'США' } },
    { id: 'turkiya', label: { uz: 'Turkiya', ru: 'Турция' } },
    { id: 'qozogiston', label: { uz: "Qozog'iston", ru: 'Казахстан' } },
    { id: 'belarus', label: { uz: 'Belarus', ru: 'Беларусь' } },
  ];

  // Sub filtr — janr (kanal.subcategory)
  const genres = [
    { id: 'barcasi', label: { uz: 'Barchasi', ru: 'Все' } },
    { id: 'yangiliklar', label: { uz: 'Yangiliklar', ru: 'Новости' } },
    { id: 'sport', label: { uz: 'Sport', ru: 'Спорт' } },
    { id: 'kino', label: { uz: 'Kino', ru: 'Кино' } },
    { id: 'seriallar', label: { uz: 'Seriallar', ru: 'Сериалы' } },
    { id: 'musiqiy', label: { uz: 'Musiqiy', ru: 'Музыкальные' } },
    { id: 'bolalar', label: { uz: 'Bolalar', ru: 'Детские' } },
    { id: 'hujjatli', label: { uz: 'Hujjatli', ru: 'Документальные' } },
    { id: 'kongilochar', label: { uz: "Ko'ngilochar", ru: 'Развлекательные' } },
    { id: 'talimiy', label: { uz: "Ta'limiy", ru: 'Образовательные' } },
    { id: 'madaniyat', label: { uz: 'Madaniyat', ru: 'Культура' } },
    { id: 'sayohat', label: { uz: 'Sayohat', ru: 'Путешествия' } },
    { id: 'anime', label: { uz: 'Anime', ru: 'Аниме' } },
    { id: 'multfilm', label: { uz: 'Multfilm', ru: 'Мультфильмы' } },
    { id: 'jonli', label: { uz: 'Jonli Efir', ru: 'Прямой эфир' } },
    { id: 'oilaviy', label: { uz: 'Oilaviy', ru: 'Семейные' } },
  ];

  const filteredChannels = useMemo(
    () =>
      channels.filter((channel) => {
        const matchesSearch = channel.name
          .toLowerCase()
          .includes(searchQuery.toLowerCase());
        const matchesCountry = channel.category === activeCountry;
        const matchesGenre =
          activeGenre === 'barcasi' || channel.subcategory === activeGenre;
        return matchesSearch && matchesCountry && matchesGenre;
      }),
    [channels, searchQuery, activeCountry, activeGenre]
  );

  const openChannel = (channel) => {
    if (channel?.videoUrl) {
      setSelectedChannel(channel);
      setShowPlayer(true);
      setShowMenuBar(false);
    }
  };

  // TV pulti / klaviatura navigatsiyasi:
  //  ↑ / ↓  — kanallar ro'yxati bo'yicha fokusni siljitish
  //  ← / →  — davlat (asosiy kategoriya) bo'yicha oldingi/keyingisiga o'tish
  //  Enter  — fokusdagi kanalni ochish
  //  Space  — davlatlar, janrlar va qolgan kanallar menyusini ochish/yopish
  useEffect(() => {
    const onKey = (e) => {
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA') return; // matn yozayotganda aralashmaymiz
      if (showPlayer) return; // pleyer ochiq bo'lsa, u o'zi boshqaradi

      const cIndex = countries.findIndex((c) => c.id === activeCountry);
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setFocusIndex((i) => Math.min(i + 1, filteredChannels.length - 1));
          break;
        case 'ArrowUp':
          e.preventDefault();
          setFocusIndex((i) => Math.max(i - 1, 0));
          break;
        case 'ArrowRight':
          e.preventDefault();
          setActiveCountry(countries[(cIndex + 1) % countries.length].id);
          setActiveGenre('barcasi');
          setFocusIndex(0);
          break;
        case 'ArrowLeft':
          e.preventDefault();
          setActiveCountry(
            countries[(cIndex - 1 + countries.length) % countries.length].id
          );
          setActiveGenre('barcasi');
          setFocusIndex(0);
          break;
        case 'Enter':
          e.preventDefault();
          openChannel(filteredChannels[focusIndex]);
          break;
        case ' ':
        case 'Spacebar':
          e.preventDefault();
          setShowMenuBar((v) => !v);
          break;
        default:
          break;
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filteredChannels, activeCountry, focusIndex, showPlayer]);

  // Fokusdagi kanal ko'rinish maydoniga avtomatik suriladi
  useEffect(() => {
    const el = cardRefs.current[focusIndex];
    if (el) el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }, [focusIndex]);

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
            {currentLang === 'uz' ? 'Telekanallar' : 'Телеканалы'}
          </span>
        </div>
        
        {/* Page Title */}
        <h1 className="text-4xl font-bold mb-2">
          {currentLang === 'uz' ? 'Telekanallar' : 'Телеканалы'}
        </h1>
        {/* Klaviatura / pult boshqaruvi haqida eslatma */}
        <p className="mb-8 text-xs text-gray-500">
          {currentLang === 'uz'
            ? '↑ ↓ kanal · ← → davlat · Enter ochish · Space menyu'
            : '↑ ↓ канал · ← → страна · Enter открыть · Space меню'}
        </p>
        
        {/* Search and View Options */}
        <div className="mb-8 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder={currentLang === 'uz' ? "TV kanal nomini kiriting..." : "Введите название канала..."}
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setFocusIndex(0);
              }}
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
          
          {/* View Options */}
          <div className="flex items-center gap-2 bg-dark-card rounded-lg p-1">
            <button className="flex items-center gap-2 px-4 py-2 rounded-md bg-primary text-black font-medium">
              <List size={18} />
              <span className="hidden sm:inline">{currentLang === 'uz' ? "Kanal ro'yxati" : 'Список каналов'}</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded-md text-gray-400 hover:text-white transition-colors">
              <RadioIcon size={18} />
              <span className="hidden sm:inline">Radio</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded-md text-gray-400 hover:text-white transition-colors">
              <PlaySquare size={18} />
              <span className="hidden sm:inline">{currentLang === 'uz' ? "Pleylistni yuklab olish" : 'Скачать плейлист'}</span>
            </button>
          </div>
        </div>
        
        {/* Asosiy filtr — Davlat */}
        <div className="mb-4 flex flex-wrap gap-3">
          {countries.map((country) => (
            <button
              key={country.id}
              onClick={() => {
                setActiveCountry(country.id);
                setActiveGenre('barcasi');
                setFocusIndex(0);
              }}
              className={`px-6 py-2 rounded-full font-medium transition-all duration-300 ${
                activeCountry === country.id
                  ? 'bg-primary text-black'
                  : 'bg-dark-card text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              {country.label[currentLang]}
            </button>
          ))}
        </div>

        {/* Sub filtr — Janr */}
        <div className="mb-8 flex flex-wrap gap-2">
          {genres.map((genre) => (
            <button
              key={genre.id}
              onClick={() => {
                setActiveGenre(genre.id);
                setFocusIndex(0);
              }}
              className={`px-4 py-1.5 rounded-full text-sm transition-all duration-300 ${
                activeGenre === genre.id
                  ? 'bg-secondary text-black'
                  : 'bg-dark-card text-gray-500 hover:text-white hover:bg-gray-800'
              }`}
            >
              {genre.label[currentLang]}
            </button>
          ))}
        </div>

        {/* Channels Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredChannels.map((channel, index) => (
            <div
              key={channel.id}
              ref={(el) => (cardRefs.current[index] = el)}
              className={`group cursor-pointer rounded-xl p-1 transition-all duration-200 ${
                index === focusIndex
                  ? 'ring-2 ring-primary ring-offset-2 ring-offset-dark'
                  : 'ring-0'
              }`}
              onClick={() => {
                setFocusIndex(index);
                openChannel(channel);
              }}
            >
              {/* Channel card: logo (yoki nom) + jonli efir belgisi */}
              <div className="bg-dark-card rounded-lg group-hover:bg-gray-800 transition-colors overflow-hidden">
                <div className="relative h-32 flex items-center justify-center p-4">
                  {channel.country && (
                    <span className="absolute top-2 left-2 px-2 py-0.5 rounded-full bg-black/60 text-[11px] font-medium text-gray-200">
                      {currentLang === 'ru'
                        ? channel.country.name_ru
                        : channel.country.name_uz}
                    </span>
                  )}
                  {channel.logo ? (
                    <img
                      src={channel.logo}
                      alt={channel.name}
                      className="max-h-full max-w-full object-contain"
                    />
                  ) : (
                    <span className="text-center text-lg font-bold text-white">
                      {channel.name}
                    </span>
                  )}
                </div>
                <div className="flex items-center justify-between px-4 py-3 border-t border-gray-800">
                  <h3 className="font-semibold truncate">{channel.name}</h3>
                  {channel.videoUrl && (
                    <span className="ml-2 flex-shrink-0 flex items-center gap-1 text-xs text-primary">
                      <span className="w-2 h-2 bg-primary rounded-full animate-pulse"></span>
                      {currentLang === 'uz' ? 'Jonli' : 'Эфир'}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Loading / No Results */}
        {loading && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">
              {currentLang === 'uz' ? 'Yuklanmoqda...' : 'Загрузка...'}
            </p>
          </div>
        )}
        {!loading && filteredChannels.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">
              {currentLang === 'uz' ? 'Kanallar topilmadi' : 'Каналы не найдены'}
            </p>
          </div>
        )}
      </div>
      
      {/* Space bilan ochiladigan menyu paneli: kategoriyalar + qolgan kanallar */}
      {showMenuBar && (
        <div
          className="fixed inset-0 z-40 bg-black/50"
          onClick={() => setShowMenuBar(false)}
        >
          <div
            className="absolute left-0 top-0 bottom-0 w-80 max-w-[85vw] bg-dark-lighter border-r border-gray-800 p-4 overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-lg">
                {currentLang === 'uz' ? 'Menyu' : 'Меню'}
              </h3>
              <button
                onClick={() => setShowMenuBar(false)}
                className="text-gray-400 hover:text-white"
              >
                <X size={20} />
              </button>
            </div>

            {/* Davlatlar (asosiy) */}
            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
              {currentLang === 'uz' ? 'Davlatlar' : 'Страны'}
            </p>
            <div className="flex flex-wrap gap-2 mb-5">
              {countries.map((country) => (
                <button
                  key={country.id}
                  onClick={() => {
                    setActiveCountry(country.id);
                    setActiveGenre('barcasi');
                    setFocusIndex(0);
                  }}
                  className={`px-3 py-1 rounded-full text-sm transition-colors ${
                    activeCountry === country.id
                      ? 'bg-primary text-black'
                      : 'bg-dark-card text-gray-400 hover:text-white'
                  }`}
                >
                  {country.label[currentLang]}
                </button>
              ))}
            </div>

            {/* Janrlar (sub) */}
            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
              {currentLang === 'uz' ? 'Janrlar' : 'Жанры'}
            </p>
            <div className="flex flex-wrap gap-2 mb-6">
              {genres.map((genre) => (
                <button
                  key={genre.id}
                  onClick={() => {
                    setActiveGenre(genre.id);
                    setFocusIndex(0);
                  }}
                  className={`px-3 py-1 rounded-full text-sm transition-colors ${
                    activeGenre === genre.id
                      ? 'bg-secondary text-black'
                      : 'bg-dark-card text-gray-500 hover:text-white'
                  }`}
                >
                  {genre.label[currentLang]}
                </button>
              ))}
            </div>

            {/* Qolgan kanallar */}
            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
              {currentLang === 'uz' ? 'Kanallar' : 'Каналы'} (
              {filteredChannels.length})
            </p>
            <div className="space-y-1">
              {filteredChannels.map((channel, index) => (
                <button
                  key={channel.id}
                  onClick={() => {
                    setFocusIndex(index);
                    openChannel(channel);
                    setShowMenuBar(false);
                  }}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    index === focusIndex ? 'bg-gray-800' : 'hover:bg-dark-card'
                  }`}
                >
                  <img
                    src={channel.logo}
                    alt={channel.name}
                    className="w-8 h-6 object-contain flex-shrink-0"
                  />
                  <span className="text-sm truncate">{channel.name}</span>
                  {channel.videoUrl && (
                    <span className="ml-auto text-[10px] text-primary">●</span>
                  )}
                </button>
              ))}
              {filteredChannels.length === 0 && (
                <p className="text-sm text-gray-500 px-3 py-2">
                  {currentLang === 'uz' ? 'Kanallar topilmadi' : 'Каналы не найдены'}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Video Player */}
      {showPlayer && selectedChannel && (
        <VideoPlayer 
          src={selectedChannel.videoUrl}
          poster={selectedChannel.image}
          onClose={() => {
            setShowPlayer(false);
            setSelectedChannel(null);
          }}
        />
      )}
    </div>
  );
};

export default TVChannels;
