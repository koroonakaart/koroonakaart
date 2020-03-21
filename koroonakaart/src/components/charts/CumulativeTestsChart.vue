<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "CumulativeTestsChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("cumulativeTests"),
          align: "left"

        },

        exporting: {
          buttons: {
              customButton: {
                  text: this.$t("linear"),
                  onclick: function() {
                      this.yAxis[0].update({
                          type: 'linear'
                      });
                  }
              },
              customButton2: {
                  text: this.$t("logarithmic"),
                  onclick: function() {
                      this.yAxis[0].update({
                          type: 'logarithmic'
                      });
                  }
              }}},
        chart: {
          height: 470
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        legend: {
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom"
        },

        plotOptions: {
          series: {
            label: {
              connectorAllowed: false
            }
          }
        },

        xAxis: {
          categories: [
            "2020-02-26",
            "2020-02-27",
            "2020-02-28",
            "2020-02-29",
            "2020-03-01",
            "2020-03-02",
            "2020-03-03",
            "2020-03-04",
            "2020-03-05",
            "2020-03-06",
            "2020-03-07",
            "2020-03-08",
            "2020-03-09",
            "2020-03-10",
            "2020-03-11",
            "2020-03-12",
            "2020-03-13",
            "2020-03-14",
            "2020-03-15",
            "2020-03-16",
            "2020-03-17",
            "2020-03-18",
            "2020-03-19",
            "2020-03-20",
            "2020-03-21"
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfTests"),
          }
        },

        series: [
          {
            name: this.$t("testsAdministered"),
            data: [
              6,
              17,
              29,
              38,
              53,
              74,
              100,
              143,
              184,
              242,
              293,
              311,
              350,
              419,
              464,
              584,
              843,
              971,
              1133,
              1387,
              1625,
              2020,
              2259,
              2504,
              2812
            ]
          }
        ]
      }
    };
  },

  // Get current locale
  computed: {
    currentLocale: function() {
      return this.$i18n.locale;
    }
  },

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale() {
      this.chartOptions.title.text = this.$t("cumulativeTests");
      this.chartOptions.yAxis.title.text = this.$t("numberOfTests");
      this.chartOptions.series[0].name = this.$t("testsAdministered");
      this.expoting.buttons.customButton.text = this.$t("linear");
      this.expoting.buttons.customButton2.text = this.$t("logarithmic");

    }
  }
};
</script>

<style lang="scss" scoped>
</style>
