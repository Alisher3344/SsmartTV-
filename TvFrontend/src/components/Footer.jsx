import { MessageCircle, Phone, Mail } from 'lucide-react';

const Footer = () => {

  return (
    <footer className="bg-ink-900 border-t border-white/10 mt-20">
      {/* Brand accent chizig'i (binafsha → oltin) */}
      <div className="h-px w-full bg-brand-gradient" />
      <div className="page-container py-14">
        {/* Logo + serif wordmark — chapga tekislangan */}
        <div className="mb-10 flex items-center gap-4">
          <img
            src="/logo.png"
            alt="SSMART TV"
            className="h-14 sm:h-16 w-auto object-contain"
            style={{ filter: 'brightness(0) invert(1) drop-shadow(0 2px 10px rgba(0, 0, 0, 0.6))' }}
          />
          <span className="font-display text-2xl sm:text-3xl font-semibold tracking-tight text-white/90">
            SSMART<span className="text-gold">.</span>TV
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          {/* Bo'limlar */}
          <div>
            <h3 className="font-sans text-eyebrow uppercase tracking-[0.18em] text-gold/80 mb-4">Bo'limlar</h3>
            <ul className="space-y-2 text-sm text-white/55">
              <li><a href="/" className="hover:text-gold transition-colors">Bosh sahifa</a></li>
              <li><a href="/channels" className="hover:text-gold transition-colors">TV-kanallar</a></li>
              <li><a href="/sport" className="hover:text-gold transition-colors">Sport</a></li>
              <li><a href="/movies" className="hover:text-gold transition-colors">Filmlar</a></li>
              <li><a href="/series" className="hover:text-gold transition-colors">Seriallar</a></li>
              <li><a href="/kids" className="hover:text-gold transition-colors">Bolalar uchun</a></li>
            </ul>
          </div>

          {/* Ma'lumot */}
          <div>
            <h3 className="font-sans text-eyebrow uppercase tracking-[0.18em] text-gold/80 mb-4">Ma'lumot</h3>
            <ul className="space-y-2 text-sm text-white/55">
              <li><a href="/promo" className="hover:text-gold transition-colors">Promo-kodni kiritish</a></li>
              <li><a href="/smarttv" className="hover:text-gold transition-colors">Televizorga o'rnatish</a></li>
              <li><a href="/agreement" className="hover:text-gold transition-colors">Foydalanuvchi shartnomasi</a></li>
              <li><a href="/privacy" className="hover:text-gold transition-colors">Maxfiylik siyosati</a></li>
            </ul>
          </div>

          {/* Yordam */}
          <div>
            <h3 className="font-sans text-eyebrow uppercase tracking-[0.18em] text-gold/80 mb-4">Yordam</h3>
            <div className="space-y-3">
              <a href="mailto:info@smarttv.uz" className="flex items-center gap-2 text-sm text-white/55 hover:text-gold transition-colors">
                <Mail size={18} className="text-gold" />
                info@smarttv.uz
              </a>
              <a href="tel:+998555162111" className="flex items-center gap-2 text-sm text-white/55 hover:text-gold transition-colors">
                <Phone size={18} className="text-gold" />
                +998 55 516 2111
              </a>
              <a href="https://t.me/smarttv_support" className="flex items-center gap-2 text-sm text-white/55 hover:text-gold transition-colors">
                <MessageCircle size={18} className="text-gold" />
                Telegram yordam
              </a>
            </div>
          </div>

          {/* Ilovalar */}
          <div>
            <h3 className="font-sans text-eyebrow uppercase tracking-[0.18em] text-gold/80 mb-4">Ilovalar</h3>
            <div className="grid grid-cols-2 gap-3">
              <a href="https://apps.apple.com" target="_blank" rel="noopener noreferrer" className="hover:opacity-80 transition-opacity">
                <div className="bg-white/5 ring-1 ring-white/10 rounded-lg p-3 flex items-center justify-center h-12">
                  <span className="text-xs text-white/60">App Store</span>
                </div>
              </a>
              <a href="https://play.google.com" target="_blank" rel="noopener noreferrer" className="hover:opacity-80 transition-opacity">
                <div className="bg-white/5 ring-1 ring-white/10 rounded-lg p-3 flex items-center justify-center h-12">
                  <span className="text-xs text-white/60">Google Play</span>
                </div>
              </a>
              <a href="#" className="hover:opacity-80 transition-opacity">
                <div className="bg-white/5 ring-1 ring-white/10 rounded-lg p-3 flex items-center justify-center h-12">
                  <span className="text-xs text-white/60">Galaxy Store</span>
                </div>
              </a>
              <a href="#" className="hover:opacity-80 transition-opacity">
                <div className="bg-white/5 ring-1 ring-white/10 rounded-lg p-3 flex items-center justify-center h-12">
                  <span className="text-xs text-white/60">Smart TV</span>
                </div>
              </a>
              <a href="#" className="hover:opacity-80 transition-opacity">
                <div className="bg-white/5 ring-1 ring-white/10 rounded-lg p-3 flex items-center justify-center h-12">
                  <span className="text-xs text-white/60">App Gallery</span>
                </div>
              </a>
            </div>
          </div>
        </div>
        
        {/* Ijtimoiy tarmoqlar */}
        <div className="border-t border-white/10 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-3">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="tap-target bg-white/5 ring-1 ring-white/10 hover:bg-gold hover:text-ink rounded-full transition-colors active:scale-95">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
              <a href="https://youtube.com" target="_blank" rel="noopener noreferrer" className="tap-target bg-white/5 ring-1 ring-white/10 hover:bg-gold hover:text-ink rounded-full transition-colors active:scale-95">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </a>
              <a href="https://t.me/smarttv" target="_blank" rel="noopener noreferrer" className="tap-target bg-white/5 ring-1 ring-white/10 hover:bg-gold hover:text-ink rounded-full transition-colors active:scale-95">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.654-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.941z"/>
                </svg>
              </a>
            </div>

            <div className="text-sm text-white/45 text-center md:text-left">
              <p>© 2015 - 2026 SSMART TV. Barcha huquqlar himoyalangan.</p>
            </div>
          </div>

          <div className="mt-4 text-center">
            <div className="flex flex-wrap justify-center gap-4 text-xs text-white/40">
              <a href="/agreement" className="hover:text-gold transition-colors">Foydalanuvchi shartnomasi</a>
              <span>•</span>
              <a href="/privacy" className="hover:text-gold transition-colors">Maxfiylik siyosati</a>
              <span>•</span>
              <a href="/terms" className="hover:text-gold transition-colors">Foydalanish shartlari</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
