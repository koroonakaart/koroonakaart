<template>
  <b-container>
    <highcharts
      class="chart"
      :options="chartOptions"
    ></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";
// import Highcharts from "highcharts";

export default {
  name: "TestsAgeSexRelationalDistributionChart",

  data () {
    const categories = [
      "0 - 4",
      "5 - 9",
      "10 - 14",
      "15 - 19",
      "20 - 24",
      "25 - 29",
      "30 - 34",
      "35 - 39",
      "40 - 44",
      "45 - 49",
      "50 - 54",
      "55 - 59",
      "60 - 64",
      "65+"
    ];

    return {
      chartOptions: {
        title: {
          text: this.$t("relationalDistributionOfAgeSexTests"), //TRANSLATE
          align: "left",
          y: 30
        },

        chart: {
          absolute: true,
          type: "bar",
          height: 470
        },

        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15
          }
        },

        credits: {
          enabled: false
        },

        xAxis: [
          {
            categories,
            reversed: false,
            labels: {
              step: 1
            },
          },
          {
            opposite: true,
            reversed: false,
            categories,
            linkedTo: 0,
            labels: {
              step: 1
            }
          }
        ],

        yAxis: {
          title: {
            text: this.$t("numberOfTests")
          },
          max: 100,
          tickInterval: 25,
          labels: {
            formatter: function () {
              const absoluteValue = Math.abs(this.value);
              if (absoluteValue > 100) return "";
              return absoluteValue + "%";
            }
          }
        },
        plotOptions: {
          bar: {
            stacking: "normal",
            enableMouseTracking: true
          }
        },

        tooltip: {
          formatter: function () {
            let value = Math.abs(this.point.y);
            return (
              "<b>" +
              this.series.name +
              "  " +
              this.point.category +
              "</b><br/>" +
              + value + "%"
            );
          }
        },

        series: [
          {
            name: this.$t("maleNegative"),
            data: data.dataPositiveTestsByAgeChart.maleNegative.map((val, index) => {
              const total = data.dataPositiveTestsByAgeChart.maleNegative[index] + data.dataPositiveTestsByAgeChart.malePositive[index];
              let pcnt = (val * 100) / total;
              pcnt = Math.round(Math.abs(pcnt));
              return pcnt * -1;
            }),
            color: "#97beeb"
          },
          {
            name: this.$t("malePositive"),
            data: data.dataPositiveTestsByAgeChart.malePositive.map((val, index) => {
              const total = data.dataPositiveTestsByAgeChart.maleNegative[index] + data.dataPositiveTestsByAgeChart.malePositive[index];
              let pcnt = (val * 100) / total;
              pcnt = Math.round(Math.abs(pcnt));
              return pcnt * -1;
            }),
            color: "#2f7ed8"
          },
          {
            name: this.$t("femaleNegative"),
            data: data.dataPositiveTestsByAgeChart.femaleNegative.map((val, index) => {
              const total = data.dataPositiveTestsByAgeChart.femaleNegative[index] + data.dataPositiveTestsByAgeChart.femalePositive[index];
              let pcnt = (val * 100) / total;
              pcnt = Math.round(Math.abs(pcnt));
              return pcnt;
            }),
            color: "#917ea9"
          },
          {
            name: this.$t("femalePositive"),
            data: data.dataPositiveTestsByAgeChart.femalePositive.map((val, index) => {
              const total = data.dataPositiveTestsByAgeChart.femaleNegative[index] + data.dataPositiveTestsByAgeChart.femalePositive[index];
              let pcnt = (val * 100) / total;
              pcnt = Math.round(Math.abs(pcnt));
              return pcnt;
            }),
            color: "#492970"
          }
        ]
      }
    };
  },

  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    }
  },

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale () {
      this.chartOptions.title.text = this.$t("relationalDistributionOfAgeSexTests");
      this.chartOptions.yAxis.title.text = this.$t("percentTests");
      this.chartOptions.series[0].name = this.$t("maleNegative");
      this.chartOptions.series[1].name = this.$t("malePositive");
      this.chartOptions.series[2].name = this.$t("femaleNegative");
      this.chartOptions.series[3].name = this.$t("femalePositive");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
