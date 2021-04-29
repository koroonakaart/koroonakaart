<template>
  <b-container fluid>
    <highcharts :constructor-type="'stockChart'" class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";
import { formatTooltip } from "../../utilities/formatTooltip";

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
              text: "Embed chart"
            }
          },

          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "separator",
                "downloadPNG",
                "downloadSVG",
                "downloadCSV",
                "separator",
                "embed"
              ]
            }
          }
        },

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true
        },

        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15
          }
        },

        xAxis: {
          type: "datetime",
          dateTimeLabelFormats: {
            day: "%Y<br>%m-%d",
            week: "%Y<br>%m-%d",
            month: "%Y-%m",
            year: "%Y"
          },
          labels: {
            style: {
              fontSize: "11px"
            }
          }
        },

        yAxis: {
//          min: 0,
          title: {
            text: this.$t("numberOfCases")
          }
        },

       tooltip: {
          formatter: (context) => {
              return formatTooltip(context, this.chartOptions.series, this.currentLocale, 0, true);
          },
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          split: false,
          useHTML: true,
          distance: 20
        },
        legend: {
          enabled: true,
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
          y: 0
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
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            data: data.dataNewCasesPerDayChart.confirmedCases
          },
         {
            name: this.$t("recovered"),
            color: "#90ed7d",
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            data: data.dataNewCasesPerDayChart.recovered
          },
          {
            name: this.$t("deceased"),
            color: "#434348",
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
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
