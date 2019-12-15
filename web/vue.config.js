module.exports = {
  publicPath: '/',
  devServer: {
    "host": "0.0.0.0",
    "port": 80,
  },
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "@/assets/scss/_variable.scss";` //新
        // data: `@import "~@/assets/scss/_veriable.scss"` 老
      }
    }
  }
};