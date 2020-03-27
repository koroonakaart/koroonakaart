<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "DailyCountyCasesChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("confirmedCasesByCounties"),
          align: "left",
          y: 30
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
          categories: data.dates1,
          crosshair: true,
          plotLines: [{
              color: 'red', // Color value
              value: 9, // Value of where the line will appear
              width: 2,
              label: {
              text: this.$t("method"),
              align: "left",
              rotation: 360
              }
            }]
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

        series: [
          {
            name: "Harjumaa",
            data: data.countyByDay.Harjumaa,
            color: "#2F7ED8"
          },
          {
            name: "Hiiumaa",
            data: data.countyByDay.Hiiumaa,
            color: "#456990"
          },
          {
            name: "Ida-Virumaa",
            data: data.countyByDay.IdaVirumaa,
            color: "#49BEAA"
          },
          {
            name: "Jõgevamaa",
            data: data.countyByDay.Jõgevamaa,
            color: "#49DCB1"
          },
          {
            name: "Järvamaa",
            data: data.countyByDay.Järvemaa,
            color: "#EEB868"
          },
          {
            name: "Läänemaa",
            data: data.countyByDay.Läänemaa
          },
          {
            name: "Lääne-Virumaa",
            data: data.countyByDay.LääneVirumaa,
            color: "#6684A4"
          },
          {
            name: "Põlvamaa",
            data: data.countyByDay.Põlvamaa
          },
          {
            name: "Pärnumaa",
            data: data.countyByDay.Pärnumaa
          },
          {
            name: "Raplamaa",
            data: data.countyByDay.Raplamaa
          },
          {
            name: "Saaremaa",
            data: data.countyByDay.Saaremaa
          },
          {
            name: "Tartumaa",
            data: data.countyByDay.Tartumaa
          },
          {
            name: "Valgamaa",
            data: data.countyByDay.Valgamaa
          },
          {
            name: "Viljandimaa",
            data: data.countyByDay.Viljandimaa
          },
          {
            name: "Võrumaa",
            data: data.countyByDay.Võrumaa
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
      this.chartOptions.xAxis.plotLines[0].label.text = this.$t("method");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
