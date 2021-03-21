module.exports = {
  devServer: {
    // host: '192.168.1.243',
    // proxy: 'http://192.168.1.243:8080',
    port: 8080,
  },

  css: {
    loaderOptions: {
      scss: {
        additionalData: `
                @import "~@/assets/styles/colors.scss";
                @import "~@/assets/styles/components.scss";
                @import "~@/assets/styles/animations.scss";
                @import "~@/assets/styles/fonts.scss";
                @import "~@/assets/styles/scss.scss";
                `,
      },
    },
  },

  runtimeCompiler: true,
  lintOnSave: false,
};
