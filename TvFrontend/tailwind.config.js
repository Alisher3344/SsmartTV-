/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#710087',
          dark: '#5a006b',
          light: '#a000c0',
        },
        secondary: {
          DEFAULT: '#ffcc00',
          dark: '#ff9900',
        },
        dark: {
          DEFAULT: '#0a0a0a',
          lighter: '#1a1a1a',
          card: '#141414',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      screens: {
        xs: '375px',
      },
      fontSize: {
        'fluid-hero': ['clamp(2rem, 6vw, 4rem)', { lineHeight: '1.05' }],
        'fluid-h1': ['clamp(1.75rem, 4vw + 0.5rem, 3rem)', { lineHeight: '1.1' }],
        'fluid-h2': ['clamp(1.25rem, 2vw + 0.5rem, 1.875rem)', { lineHeight: '1.2' }],
      },
      minHeight: {
        touch: '44px',
      },
      minWidth: {
        touch: '44px',
      },
      boxShadow: {
        glow: '0 0 24px rgba(113, 0, 135, 0.45)',
        'glow-sm': '0 0 12px rgba(113, 0, 135, 0.35)',
        card: '0 4px 24px rgba(0, 0, 0, 0.4)',
      },
      backgroundImage: {
        'brand-gradient': 'linear-gradient(135deg, #710087, #a000c0)',
        'radial-glow': 'radial-gradient(circle at center, rgba(113, 0, 135, 0.25), transparent 70%)',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
        fadeUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        float: 'float 4s ease-in-out infinite',
        shimmer: 'shimmer 1.6s infinite',
        'fade-up': 'fadeUp 0.6s ease-out',
      },
    },
  },
  plugins: [],
}
