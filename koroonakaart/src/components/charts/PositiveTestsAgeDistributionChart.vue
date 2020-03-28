<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "PositiveTestsAgeDistributionChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("distributionOfPositiveTests"),
          align: "left",
          y: 30
        },
        exporting: {
          buttons: {
            customButton: {
              text: "Abs",
              onclick: function() {
                this.update({
                  plotOptions: {
                    column: {
                      stacking: "normal"
                    }
                  },
                  yAxis: {
                    title: {
                      text: "Abs"
                    }
                  }
                });
              }
            },
            customButton2: {
              text: "%",
              onclick: function() {
                this.update({
                  plotOptions: {
                    column: {
                      stacking: "percent"
                    }
                  },
                  yAxis: {
                    title: {
                      text: "%"
                    }
                  }
                });
              }
            }
          }
        },
        chart: {
          type: "column",
          height: 470
        },
        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15
          }
        },
        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        xAxis: {
          title: {
            text: this.$t("age")
          },
          categories: [
            "0 - 4",
            "5 - 9",
            "10 - 14",
            "15 - 19",
            "20 - 24",
            "25 - 29",
            "30 - 34",
            "35 - 39",
            "40 - 44",
            "45 - 49",
            "50 - 54",
            "55 - 59",
            "60 - 64",
            "65+",
            this.$t("unknown")
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
          }
        },
        plotOptions: {
          column: {
            stacking: "normal",
            enableMouseTracking: true
          }
        },
        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b> ({point.percentage:.0f}%)</td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true
        },
        series: [
          {
            name: this.$t("positive"),
            data: data.dataPositiveTestsByAgeChart.positive,
          },
          {
            name: this.$t("negative"),
            data: data.dataPositiveTestsByAgeChart.negative,
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
      this.chartOptions.title.text = this.$t("distributionOfPositiveTests");
      this.chartOptions.xAxis.title.text = this.$t("age");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.series[1].name = this.$t("negative");
      this.chartOptions.xAxis.categories[
        this.chartOptions.xAxis.categories.length - 1
      ] = this.$t("unknown");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
