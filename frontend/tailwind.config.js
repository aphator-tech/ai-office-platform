/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: {
          dark: '#0D1117',
          card: '#161B22',
          elevated: '#21262D',
        },
        primary: {
          DEFAULT: '#58A6FF',
          light: '#79B8FF',
          dark: '#388BFD',
        },
        secondary: {
          DEFAULT: '#A371F7',
          light: '#BC8CFF',
          dark: '#8957E5',
        },
        accent: {
          DEFAULT: '#3FB950',
          light: '#56D364',
          dark: '#238636',
        },
        warning: '#D29922',
        error: '#F85149',
        text: {
          primary: '#F0F6FC',
          secondary: '#8B949E',
        },
        border: '#30363D',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'monospace'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 300ms ease-out',
        'slide-up': 'slideUp 300ms ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
