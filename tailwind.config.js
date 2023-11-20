/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./static/**/**/*.{css,js}",
    "./templates/**/**/*.{html,js}",
    "./templates/**/*.{html,js}",
    "./templates/*.{html,js}",
  ],
  theme: {
    extend: {},
    screens: {
      "sm": {min: "360px", max: "719px"},
      "md": "720px"
    }
  },
  plugins: [],
}

