<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "ConfirmedCasesByCountiesChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("confirmedCasesByCounties"),
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
            "Võrumaa",
            this.$t("insufficientData")
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
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
            data: [123, 2, 6, 1, 1, 1, 2, 3, 22, 2, 94, 21, 1, 2, 34, 11]
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
      this.chartOptions.title.text = this.$t("confirmedCasesByCounties");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("numberOfCases");
      this.chartOptions.xAxis.categories[0] = this.$t("insufficientData");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
