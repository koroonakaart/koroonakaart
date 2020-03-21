<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "PositiveNegativeChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("positiveNegativeTitle")
        },

        chart: {
          type: "column",
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
            text: "%",
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
        plotOptions: {
          column: {
          stacking: "percent",
          enableMouseTracking: true
          }
        },

        series: [
          {
            name: this.$t("negative"),
            data: [155, 36, 14, 17, 15, 17, 16, 34, 63, 13, 35, 166, 176, 51, 333, 1365],
            color: "#90ed7d"
          },
          {
            name: this.$t("positive"),
            data: [10, 1, 1, 1, 1, 2, 2, 2, 2, 3, 6, 17, 22, 30, 92, 114],
            color: "#910000"
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
      this.chartOptions.title.text = this.$t("positiveNegativeTitle");
    //  this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("negative");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.xAxis.categories[0] = this.$t("insufficientData");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
