/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  theme: {
    extend: {
      fontFamily: {
        acumin: ['Acumin Regular'],
        acuminBold: ['Acumin Bold']
      },
      colors: {
        textAreaGray: '#E8E8E8',
        placeHolderGray: '#D9D9D9',
        textGray: '#636363',
        buttonGreen: '#299E00',
        buttonBlue: '#00C2FF',
      }
    },
  },
  plugins: [
    require('tw-elements/dist/plugin')
  ],
}
