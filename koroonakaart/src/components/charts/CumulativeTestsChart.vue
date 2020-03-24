<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "CumulativeTestsChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("cumulativeTests"),
          align: "left",
          y: 30
        },

        exporting: {
          buttons: {
            customButton: {
              text: this.$t("linear"),
              onclick: function() {
                this.yAxis[0].update({
                  type: "linear"
                });
              }
            },
            customButton2: {
              text: this.$t("logarithmic"),
              onclick: function() {
                this.yAxis[0].update({
                  type: "logarithmic"
                });
              }
            }
          }
        },
        chart: {
          height: 470
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },
        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15
          }
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
          categories: data.dates2
        },

        yAxis: {
          title: {
            text: this.$t("numberOfTests")
          }
        },

        series: [
          {
            name: this.$t("testsAdministered"),
            data: data.dataCumulativeTestsChart.testsAdministered
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
      this.chartOptions.exporting.buttons.customButton.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "logarithmic"
      );
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
