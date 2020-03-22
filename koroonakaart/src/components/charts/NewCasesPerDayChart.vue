<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "NewCasesPerDayChart",

  data() {
    return {
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
            verticalAlign: 'top',
            y: -15,

        }},
        xAxis: {
          categories: [
            "2020-02-26",
            "2020-02-27",
            "2020-02-28",
            "2020-02-29",
            "2020-03-01",
            "2020-03-02",
            "2020-03-03",
            "2020-03-04",
            "2020-03-05",
            "2020-03-06",
            "2020-03-07",
            "2020-03-08",
            "2020-03-09",
            "2020-03-10",
            "2020-03-11",
            "2020-03-12",
            "2020-03-13",
            "2020-03-14",
            "2020-03-15",
            "2020-03-16",
            "2020-03-17",
            "2020-03-18",
            "2020-03-19",
            "2020-03-20",
            "2020-03-21",
            "2020-03-22"
          ],
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
            data: [
              0,
              1,
              0,
              0,
              0,
              0,
              1,
              0,
              3,
              5,
              0,
              0,
              0,
              3,
              4,
              24,
              68,
              26,
              36,
              34,
              20,
              33,
              9,
              16,
              23,
              20
            ]
          },
          {
            name: this.$t("recovered"),
            color: "#90ed7d",
            data: [
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              1,
              0,
              0,
              0,
              0,
              1,
              0,
              2
            ]
          },
          {
            name: this.$t("deceased"),
            color: "#434348",
            data: [
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0,
              0
            ]
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
