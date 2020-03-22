<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "CumulativeCasesChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("cumulativeCases"),
          align: "left"
        },

  exporting: {
    buttons: {
        customButton: {
            text: this.$t("linear"),
            onclick: function() {
                this.yAxis[0].update({
                    type: 'linear'
                });
            }
        },
        customButton2: {
            text: this.$t("logarithmic"),
            onclick: function() {
                this.yAxis[0].update({
                    type: 'logarithmic'
                });
            }
        }}},

        chart: {
          height: 470
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        legend: {
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom"
        },

        plotOptions: {
          series: {
            label: {
              connectorAllowed: false
            }
          }
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
            "2020-03-19",
            "2020-03-20",
            "2020-03-21",
            "2020-03-22"
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
          }
        },

        series: [
          {
            name: this.$t("confirmedCases"),
            color: "#2f7ed8",
            data: [
              0,
              1,
              1,
              1,
              1,
              1,
              2,
              2,
              5,
              10,
              10,
              10,
              10,
              13,
              17,
              41,
              109,
              135,
              171,
              205,
              225,
              258,
              267,
              283,
              306,
              326
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
              1,
              1,
              1,
              1,
              1,
              1,
              2,
              2,
              4
            ]
          },
          {
            name: this.$t("active"),
            color: "#f28f43",
            data: [
              0,
              1,
              1,
              1,
              1,
              1,
              2,
              2,
              5,
              10,
              10,
              10,
              10,
              13,
              17,
              41,
              109,
              134,
              170,
              204,
              224,
              257,
              266,
              281,
              304,
              324
            ]
          },
          {
            name: this.$t("deceased"),
            color: "#0d233a",
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
      this.chartOptions.title.text = this.$t("cumulativeCases");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("confirmedCases");
      this.chartOptions.series[1].name = this.$t("recovered");
      this.chartOptions.series[2].name = this.$t("active");
      this.chartOptions.series[3].name = this.$t("deceased");
      this.expoting.buttons.customButton.text = this.$t("linear");
      this.expoting.buttons.customButton2.text = this.$t("logarithmic");

    }
  }
};
</script>

<style lang="scss" scoped>
</style>
