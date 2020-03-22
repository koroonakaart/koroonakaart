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
          text: this.$t("confirmedCasesByCounties")
        },

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
            this.$t("insufficientData"),
            "Lääne-Virumaa",
            "Valgamaa",
            "Jõgevamaa",
            "Järvamaa",
            "Läänemaa",
            "Hiiumaa",
            "Viljandimaa",
            "Raplamaa",
            "Põlvamaa",
            "Ida-Virumaa",
            "Tartumaa",
            "Pärnumaa",
            "Võrumaa",
            "Saaremaa",
            "Harjumaa"
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
            data: [11, 1, 1, 1, 1, 2, 2, 2, 2, 3, 6, 21, 22, 34, 94, 123]
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
