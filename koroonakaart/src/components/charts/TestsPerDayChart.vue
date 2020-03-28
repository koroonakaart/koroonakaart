<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "TestsPerDayChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("testsPerDay"),
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
          categories: data.dates2,
          crosshair: true,
          plotLines: [
            {
              color: "red", // Color value
              value: 18, // Value of where the line will appear
              width: 1,
              label: {
                text: this.$t("method"),
                align: "left"
              }
            },
            {
              color: "red", // Color value
              value: 28, // Value of where the line will appear
              width: 1,
              label: {
                text: this.$t("method"),
                align: "left",
                x: -20
              }
            }
          ]
        },

        yAxis: [
          {
            min: 0,
            title: {
              text: this.$t("numberOfTests")
            }
          },
          {
            max: 100,
            title: {
              text: this.$t("percentPositiveTests")
            },
            opposite: true
          }
        ],

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
            data: data.dataTestsPerDayChart.testsPerDay,
            type: "column",
            yAxis: 0
          },
          {
            name: this.$t("percentPositiveTests"),
            data: data.dataTestsPerDayChart.positiveTestsPercentage,
            type: "spline",
            yAxis: 1
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
      this.chartOptions.yAxis[0].title.text = this.$t("numberOfTests");
      this.chartOptions.yAxis[1].title.text = this.$t("percentPositiveTests");
      this.chartOptions.series[0].name = this.$t("testsPerDay");
      this.chartOptions.series[1].name = this.$t("percentPositiveTests");
      this.chartOptions.xAxis.plotLines[0].label.text = this.$t("method");
      this.chartOptions.xAxis.plotLines[1].label.text = this.$t("method");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
