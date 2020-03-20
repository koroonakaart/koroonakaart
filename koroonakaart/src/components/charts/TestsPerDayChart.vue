<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "TestsPerDayChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("testsPerDay")
        },

        chart: {
          type: "column",
          height: 470
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

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
            "2020-03-19"
          ],
          crosshair: true
        },

        yAxis: {
          min: 0,
          title: {
            text: this.$t("numberOfTests")
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
            borderWidth: 0
          }
        },

        series: [
          {
            name: this.$t("testsPerDay"),
            data: [
              6,
              11,
              12,
              9,
              15,
              21,
              26,
              43,
              41,
              58,
              51,
              18,
              39,
              69,
              45,
              120,
              259,
              128,
              162,
              254,
              238,
              395,
              239,
              245
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
      this.chartOptions.title.text = this.$t("testsPerDay");
      this.chartOptions.yAxis.title.text = this.$t("numberOfTests");
      this.chartOptions.series[0].name = this.$t("testsPerDay");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
