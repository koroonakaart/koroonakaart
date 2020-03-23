var data = require("./src/dataConstants");

module.exports = {
  devServer: {
    before: function(app, server) {
      app.get("/api", function(req, res) {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(data));
      });
    }
  },

  pluginOptions: {
    i18n: {
      locale: "ee",
      fallbackLocale: "ee",
      localeDir: "locales",
      enableInSFC: true
    }
  }
};
