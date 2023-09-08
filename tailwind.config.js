/** @type {import('tailwindcss').Config} */
module.exports = {

	content: ['./index.html', './src/**/*.{html,js,ts,jsx,tsx,vue}'],

	theme: {
		extend: {},
	},
	plugins: [],
	corePlugins: {
		// ...
		float: false, // Disable float utilities to avoid conflicts
	  },
}
