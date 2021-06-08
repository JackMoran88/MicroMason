const webpack = require('webpack')
const path = require('path')
// const PrerenderSPAPlugin = require('prerender-spa-plugin')
// const Renderer = PrerenderSPAPlugin.PuppeteerRenderer


module.exports = {

  pwa: {
    name: 'MicroMason',
  },

  configureWebpack: {
    plugins: [
      new webpack.IgnorePlugin(/^\.\/esm\/icons$/, /bootstrap-vue$/),
      // new PrerenderSPAPlugin({
      //   // Required - The path to the webpack-outputted app to prerender.
      //   staticDir: path.join(__dirname, 'dist'),
      //   // Required - Routes to render.
      //   routes: ['/'],
      //
      //   minify: {
      //     collapseBooleanAttributes: true,
      //     collapseWhitespace: true,
      //     decodeEntities: true,
      //     keepClosingSlash: true,
      //     sortAttributes: true
      //   },
      //   renderer: new Renderer({
      //     renderAfterTime: 5000, // Wait 5 seconds.
      //     // headless: false // Display the browser window when rendering. Useful for debugging.
      //   })
      // })
    ],

  },


  css: {
    loaderOptions: {
      sass: {
        additionalData: `
          @import "@/assets/styles/mixins.scss";
        `
      }
    }
  },
  pluginOptions: {
    webpackBundleAnalyzer: {
      openAnalyzer: false
    }
  },

  runtimeCompiler: true,
  lintOnSave: false,


  chainWebpack: (config) => {

    /*
       Disable (or customize) prefetch, see:
       https://cli.vuejs.org/guide/html-and-static-assets.html#prefetch
    */
    config.plugins.delete('prefetch')

    /*
       Configure preload to load all chunks
       NOTE: use `allChunks` instead of `all` (deprecated)
    */
    config.plugin('preload').tap((options) => {
      options[0].include = 'allChunks'
      return options
    })
    config.plugin('html').tap(args => {
      args[0].title = "MicroMason";
      return args;
    })
  },
};



