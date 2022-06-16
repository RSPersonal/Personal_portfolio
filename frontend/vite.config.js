const { resolve } = require('path');

module.exports = {
  plugins: [],
  root: resolve('./core/static/src'),
  base: '/core/static/',
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.js', '.json'],
  },
  build: {
    outDir: resolve('core/static/dist'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: {
        main: resolve('core/static/src/js/main.js'),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
};
