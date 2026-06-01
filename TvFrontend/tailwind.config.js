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
    },
  },
  plugins: [],
}
