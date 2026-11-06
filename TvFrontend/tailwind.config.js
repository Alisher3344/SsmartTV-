/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Binafsha — brend langari (logo). Endi kam, strukturaviy ishlatiladi.
        primary: {
          DEFAULT: '#710087',
          dark: '#54006a',
          light: '#9a1cb8',
        },
        // Yangi keskin editorial aksent — issiq oltin/amber
        gold: {
          DEFAULT: '#E8B23A',
          light: '#F5D27A',
          deep: '#B8862A',
          50: '#FBF3DD',
        },
        // Qatlamli kino-qora (tekis emas)
        ink: {
          DEFAULT: '#08080A',
          900: '#0B0B0F',
          800: '#111016',
          700: '#17161E',
          600: '#211F2A',
        },
        // Eski klasslar buzilmasligi uchun aliaslar (yangi ranglarga ko'rsatadi)
        secondary: {
          DEFAULT: '#E8B23A',
          dark: '#B8862A',
        },
        dark: {
          DEFAULT: '#08080A',
          lighter: '#111016',
          card: '#17161E',
        },
      },
      fontFamily: {
        sans: ['Manrope', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Fraunces', 'Playfair Display', 'Georgia', 'serif'],
      },
      screens: {
        xs: '375px',
      },
      fontSize: {
        'fluid-hero': ['clamp(2.5rem, 8vw, 6rem)', { lineHeight: '0.98', letterSpacing: '-0.02em' }],
        'fluid-display': ['clamp(2rem, 6vw + 0.5rem, 5rem)', { lineHeight: '1.0', letterSpacing: '-0.015em' }],
        'fluid-h1': ['clamp(1.75rem, 4vw + 0.5rem, 3rem)', { lineHeight: '1.05' }],
        'fluid-h2': ['clamp(1.5rem, 2.5vw + 0.5rem, 2.5rem)', { lineHeight: '1.1', letterSpacing: '-0.01em' }],
        eyebrow: ['0.6875rem', { lineHeight: '1', letterSpacing: '0.22em' }],
      },
      minHeight: {
        touch: '44px',
      },
      minWidth: {
        touch: '44px',
      },
      boxShadow: {
        // Eski glow keylari — endi nafis elevation soyalar (binafsha glow yo'qoladi)
        glow: '0 18px 50px -12px rgba(0,0,0,0.7)',
        'glow-sm': '0 8px 24px -8px rgba(0,0,0,0.6)',
        card: '0 16px 40px -16px rgba(0,0,0,0.75)',
        edge: 'inset 0 0 0 1px rgba(255,255,255,0.06)',
        'edge-gold': 'inset 0 0 0 1px rgba(232,178,58,0.45)',
        lift: '0 24px 60px -20px rgba(0,0,0,0.85)',
      },
      backgroundImage: {
        // Binafsha → oltin nozik chiziq (Footer aksenti)
        'brand-gradient': 'linear-gradient(90deg, transparent, #710087 30%, #E8B23A 70%, transparent)',
        // Neytrallashtirilgan (eski binafsha radial glow)
        'radial-glow': 'radial-gradient(circle at center, rgba(232,178,58,0.06), transparent 70%)',
        'film-grain':
          "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E\")",
        vignette: 'radial-gradient(120% 90% at 50% 0%, transparent 55%, rgba(0,0,0,0.55) 100%)',
        'editorial-fade': 'linear-gradient(to top, #08080A 4%, rgba(8,8,10,0.4) 40%, transparent 75%)',
        'gold-hairline': 'linear-gradient(90deg, transparent, rgba(232,178,58,0.5), transparent)',
      },
      keyframes: {
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
        fadeUp: {
          from: { opacity: '0', transform: 'translateY(24px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        kenburns: {
          '0%': { transform: 'scale(1.06)' },
          '100%': { transform: 'scale(1)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
      },
      animation: {
        shimmer: 'shimmer 1.6s infinite',
        'fade-up': 'fadeUp 0.7s cubic-bezier(0.22,1,0.36,1) both',
        kenburns: 'kenburns 12s ease-out both',
        float: 'float 4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
