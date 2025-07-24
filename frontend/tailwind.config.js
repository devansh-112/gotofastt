/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'brand-blue': '#2563eb', // blue-600
        'brand-red': '#ef4444', // red-500
      },
      backgroundImage: {
        'blue-red-gradient': 'linear-gradient(90deg, rgba(37,99,235,0.8) 0%, rgba(139,92,246,0.6) 50%, rgba(239,68,68,0.8) 100%)',
      },
    },
  },
  plugins: [],
} 