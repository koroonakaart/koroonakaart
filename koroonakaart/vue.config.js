module.exports = {
  pluginOptions: {
    i18n: {
      locale: "et",
      fallbackLocale: "et",
      localeDir: "locales",
      enableInSFC: true,
    },
    "style-resources-loader": {
      preProcessor: "sass",
      patterns: [],
    },
    webpackBundleAnalyzer: {
      // Relative to dist
      reportFilename: "../report.html",
      openAnalyzer: false,
    },
  },
};
