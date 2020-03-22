<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import { dataNewCasesPerDayChart } from "../../dataConstants";

export default {
  name: "NewCasesPerDayChart",

  data() {
    return {
      dataNewCasesPerDayChart,

      chartOptions: {
        title: {
          text: this.$t("newCasesPerDay"),
          align: "left",
          y: 30
        },

        chart: {
          type: "column",
          height: 470
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
          categories: dataNewCasesPerDayChart.date,
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
            pointPadding: 0.2,
            borderWidth: 0,
            stacking: "normal"
          }
        },

        series: [
          {
            name: this.$t("confirmedCases"),
            color: "#7cb5ec",
            data: dataNewCasesPerDayChart.confirmedCases
          },
          {
            name: this.$t("recovered"),
            color: "#90ed7d",
            data: dataNewCasesPerDayChart.recovered
          },
          {
            name: this.$t("deceased"),
            color: "#434348",
            data: dataNewCasesPerDayChart.deceased
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

<style lang="scss" scoped>
</style>
