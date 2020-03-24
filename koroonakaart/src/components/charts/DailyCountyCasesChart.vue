<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import { countyByDay } from "../../dataConstants";

export default {
  name: "DailyCountyCasesChart",

  data() {
    return {
      countyByDay,

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
          categories: countyByDay.dates,
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


        series: [
          {
            name: "Harjumaa" ,
            data: countyByDay.harjumaa,
            color:"#2F7ED8"
          },
          {
            name: "Hiiumaa",
            data: countyByDay.hiiumaa,
            color: "#456990"
          },
          {
            name: "Ida-Virumaa",
            data: countyByDay.idavirumaa,
            color: "#49BEAA"
          },
          {
            name: "Jõgevamaa" ,
            data: countyByDay.jogevamaa,
            color: "#49DCB1"
          },
          {
            name: "Järvamaa",
            data: countyByDay.jarvemaa,
            color: "#EEB868"
          },
          {
            name: "Läänemaa" ,
            data: countyByDay.laanemaa
          },
          {
            name: "Lääne-Virumaa",
            data: countyByDay.laanevirumaa,
            color: "#6684A4"
          },
          {
            name: "Põlvamaa",
            data: countyByDay.polvamaa
          },
          {
            name: "Pärnumaa",
            data: countyByDay.parnumaa
          },
          {
            name: "Raplamaa" ,
            data: countyByDay.raplamaa
          },
          {
            name: "Saaremaa",
            data: countyByDay.saaremaa
          },
          {
            name: "Tartumaa",
            data: countyByDay.tartumaa
          },
          {
            name: "Valgamaa" ,
            data: countyByDay.valgamaa
          },
          {
            name: "Viljandimaa",
            data: countyByDay.viljandimaa
          },
          {
            name: "Võrumaa",
            data: countyByDay.vorumaa
          },
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
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
