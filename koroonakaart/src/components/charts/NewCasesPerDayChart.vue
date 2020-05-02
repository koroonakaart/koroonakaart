<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "NewCasesPerDayChart",

  props: {
    height: {
      default: null
    },
    width: {
      default: null
    }
  },

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("newCasesPerDay"),
          align: "left",
          y: 5
        },

        chart: {
          type: "column",
          height: this.height,
          width: this.width
        },

        exporting: {
          menuItemDefinitions: {
            embed: {
              onclick: () => {
                this.$store.dispatch("setCurrentChartName", this.$options.name);
                this.$bvModal.show("embed-modal");
              },
              text: "Embed Graph"
            }
          },

          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "separator",
                "downloadPNG",
                "downloadJPEG",
                "downloadPDF",
                "downloadSVG",
                "downloadCSV",
                "downloadXLS",
                "separator",
                "embed"
              ]
            }
          }
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

        xAxis: {
          categories: data.dates2,
          crosshair: true
        },

        yAxis: {
          min: 0,
          title: {
            text: this.$t("numberOfCases")
          }
        },

        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true
        },

        plotOptions: {
          column: {
            pointWidth: 10,
            pointPadding: -0.2,
            borderWidth: 0
          }
        },

        series: [
          {
            name: this.$t("confirmedCases"),
            color: "#7cb5ec",
            data: data.dataNewCasesPerDayChart.confirmedCases
          },
         {
            name: this.$t("recovered"),
            color: "#90ed7d",
            data: data.dataNewCasesPerDayChart.recovered
          },
          {
            name: this.$t("deceased"),
            color: "#434348",
            data: data.dataNewCasesPerDayChart.deceased
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
      this.chartOptions.title.text = this.$t("newCasesPerDay");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("confirmedCases");
      this.chartOptions.series[1].name = this.$t("recovered");
      this.chartOptions.series[2].name = this.$t("deceased");
    }
  }
};
</script>

<style lang="scss" scoped></style>
