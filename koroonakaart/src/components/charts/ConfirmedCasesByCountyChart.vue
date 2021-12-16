// "Cases by county" chart
<template>
  <b-container fluid>
    <highcharts v-if="chartOptions"
                class="chart"
                :options="chartOptions">
    </highcharts>
  </b-container>
</template>

<script>

export default {
  name: "ConfirmedCasesByCountyChart",

  props: {
    height: {
      default: null,
    },
    width: {
      default: null,
    },
  },

  data() {
    return {
      chartOptions: null
    };
  },

  // Get current locale
  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
    loaded () {
      return this.$store.state.loaded;
    },
    confirmedCasesByCounty () {
      return this.$store.getters.confirmedCasesByCounty;
    },
    countyByDayNew () {
      return this.$store.getters.countyByDayNew;
    },
  },

  methods: {
    getChartOptions() {
      this.chartOptions = {
        title: {
          text: this.$t("confirmedCasesByCounty"),
          align: "left",
          y: 5,
        },

        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15,
          },
        },

        chart: {
          type: "bar",
          height: this.height,
          width: this.width,
          marginTop: 40,
        },

        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "downloadPNG",
                "downloadSVG",
                "downloadCSV",
              ],
            },
          },

          chartOptions: {
            // specific options for the exported image
            plotOptions: {
              series: {
                dataLabels: {
                  enabled: true,
                },
              },
            },
          },
          fallbackToExportServer: false,
        },

        tooltip: {
          headerFormat: "<span>{point.key}</span><table>",
          pointFormat:
            '<tr><td><span style="color:{series.color}">●</span> {series.name}&nbsp;&nbsp;</td>' +
            '<td style="padding:0; text-align: right"><b>{point.y}</b></tr>',
          footerFormat: "</table>",
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true,
        },

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true,
        },

        xAxis: {
          labels: {
            style: {
              fontSize: "13px",
              fontWeight: "bold",
            },
          },
          categories: [
            "Harjumaa",
            "Hiiumaa",
            "Ida-Virumaa",
            "Jõgevamaa",
            "Järvamaa",
            "Läänemaa",
            "Lääne-Virumaa",
            "Põlvamaa",
            "Pärnumaa",
            "Raplamaa",
            "Saaremaa",
            "Tartumaa",
            "Valgamaa",
            "Viljandimaa",
            "Võrumaa",
            this.$t("insufficientData"),
          ],
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases"),
          },
        },

        plotOptions: {
          bar: {
            //            dataLabels: {
            //              enabled: true
            //            },
            enableMouseTracking: true,
          },
        },

        series: [
          {
            dataLabels: {
              enabled: true,
            },
            name: this.$t("numberOfCases"),
            data: this.confirmedCasesByCounty,
          },
          {
            name: this.$t("newPositive"),
            data: this.countyByDayNew,
          },
        ],
      };
    }
  },

  created: function () {
      if (this.loaded) {
        this.getChartOptions();
      }
  },

  watch: {
    loaded: function () {
      this.getChartOptions();
    },
    currentLocale() {
      this.chartOptions.title.text = this.$t("confirmedCasesByCounty");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("numberOfCases");
      this.chartOptions.series[1].name = this.$t("newPositive");
      this.chartOptions.xAxis.categories[15] = this.$t("insufficientData");
    },
  },
};
</script>

<style lang="scss" scoped></style>
