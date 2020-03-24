<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "CumulativeCasesChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("cumulativeCases"),
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
        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15
          }
        },
        xAxis: {
          categories: data.dates2
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
          }
        },

        series: [
          {
            name: this.$t("confirmedCases"),
            color: "#2f7ed8",
            data: data.dataCumulativeCasesChart.cases
          },
          {
            name: this.$t("recovered"),
            color: "#90ed7d",
            data: data.dataCumulativeCasesChart.recovered
          },
          {
            name: this.$t("active"),
            color: "#f28f43",
            data: data.dataCumulativeCasesChart.active
          },
          {
            name: this.$t("deceased"),
            color: "#0d233a",
            data: data.dataCumulativeCasesChart.deceased
          },
          {
            name: this.$t("hospitalised"),
            data: data.dataCumulativeCasesChart.haiglas
          },
          {
            name: this.$t("intensive"),
            data: data.dataCumulativeCasesChart.intensive,
            color: "#c42525"
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
      this.chartOptions.title.text = this.$t("cumulativeCases");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("confirmedCases");
      this.chartOptions.series[1].name = this.$t("recovered");
      this.chartOptions.series[2].name = this.$t("active");
      this.chartOptions.series[3].name = this.$t("deceased");
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
