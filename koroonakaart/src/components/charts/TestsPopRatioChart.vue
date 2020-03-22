<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "TestsPopRatioChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("testsPer10000"),
          align: "left",
          y: 30
        },
        navigation: {
        buttonOptions: {
            verticalAlign: 'top',
            y: -15,

        }},
        chart: {
          type: "bar",
          height: 470
        },

        exporting: {
          chartOptions: {
            // specific options for the exported image
            plotOptions: {
              series: {
                dataLabels: {
                  enabled: true
                }
              }
            }
          },
          fallbackToExportServer: false
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        xAxis: {
          labels: {
            style: {
              fontSize: "13px",
              fontWeight: "bold"
            }
          },
          categories: [
          "Harjumaa",
          "Hiiumaa",
          "Ida-Virumaa",
          "Jõgevamaa",
          "Järvamaa",
          "Lääne-Virumaa",
          "Läänemaa",
          "Põlvamaa",
          "Pärnumaa",
          "Raplamaa",
          "Saaremaa",
          "Tartumaa",
          "Valgamaa",
          "Viljandimaa",
          "Võrumaa"

          ]
        },

        yAxis: {
          title: {
            text: this.$t("testsPer10000Axis")
          }
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true
            },
            enableMouseTracking: true
          }
        },

        series: [
          {
            name: this.$t("numberOfCases"),
            data: [2.06,
2.13,
0.44,
0.35,
0.33,
0.17,
0.98,
1.20,
2.56,
0.60,
28.39,
1.37,
0.35,
0.43,
9.50],
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
      this.chartOptions.title.text = this.$t("testsPer10000");
      this.chartOptions.yAxis.title.text = this.$t("testsPer10000Axis");
      this.chartOptions.series[0].name = this.$t("numberOfCases");
      this.chartOptions.xAxis.categories[0] = this.$t("insufficientData");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
