/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Palette dallo studio UX
        'deep-blue': '#1a1a2e',
        'gold': '#f0a500',
        'success': '#00c853',
        'warning': '#ffab00',
        'error': '#ff1744',
        'neutral': '#9e9e9e',
        'accent-purple': '#7c4dff',
        'accent-teal': '#00bcd4',
      },
      fontFamily: {
        sans: ['Inter', 'SF Pro', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
}
