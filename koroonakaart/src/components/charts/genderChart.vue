<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions" ref="thisChart"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";
import Highcharts from "highcharts";
import drilldown from "highcharts/modules/drilldown";
import dataModule from "highcharts/modules/data";

dataModule(Highcharts);
drilldown(Highcharts);

export default {
  name: "GenderChart",
  props: {
    height: {
      default: null
    },
    width: {
      default: null
    }
  },

  mounted() {
    /* console.log(this.chartOptions.yAxis.title.text); */
    console.log(data.dataPositiveTestsByAgeChart.maleNegative);
    console.log(this.chartOptions);
  },

  data() {
    return {
      chartType: "pie",
      chartOptions: {
        title: {
          text: this.$t("genderChart"),
          align: "left",
          y: 25
        },

        chart: {
          type: "pie",
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
        tooltip: {
          pointFormat:
            '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
        },

        series: [
          {
            name: this.$t("genderChart"),
            colorByPoint: true,
            data: [
              {
                name: this.$t("male"),
                y: data.dataPositiveTestsByAgeChart.maleTotal,
                drilldown: "MALE"
              },
              {
                name: this.$t("female"),
                y: data.dataPositiveTestsByAgeChart.femaleTotal,
                drilldown: "FEMALE"
              }
            ]
          }
        ],
        drilldown: {
          series: [
            {
              name: this.$t("male"),
              id: "MALE",
              tooltip: {
                pointFormat:
                  '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> cases<br/>'
              },
              data: [
                [
                  this.$t("maleNegative"),
                  data.dataPositiveTestsByAgeChart.maleNegative.reduce(
                    (a, b) => a + b,
                    0
                  )
                ],
                [
                  this.$t("malePositive"),
                  data.dataPositiveTestsByAgeChart.malePositive.reduce(
                    (a, b) => a + b,
                    0
                  )
                ]
              ]
            },
            {
              name: this.$t("female"),
              id: "FEMALE",
              tooltip: {
                pointFormat:
                  '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
              },
              data: [
                [
                  this.$t("femaleNegative"),
                  data.dataPositiveTestsByAgeChart.femaleNegative.reduce(
                    (a, b) => a + b,
                    0
                  )
                ],
                [
                  this.$t("femalePositive"),
                  data.dataPositiveTestsByAgeChart.femalePositive.reduce(
                    (a, b) => a + b,
                    0
                  )
                ]
              ]
            }
          ]
        }
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
    console.log(this.chartOptions);
      this.chartOptions.title.text = this.$t("genderChart");
      this.chartOptions.series[0].name = this.$t("genderChart");
      this.chartOptions.series[0].data[0].name = this.$t("male");
      this.chartOptions.series[0].data[1].name = this.$t("female");
      this.chartOptions.drilldown.series[0].data[0][0] = this.$t("maleNegative");
      this.chartOptions.drilldown.series[0].data[1][0] = this.$t("malePositive");
      this.chartOptions.drilldown.series[1].data[0][0] = this.$t("femaleNegative");
      this.chartOptions.drilldown.series[1].data[1][0] = this.$t("femalePositive");

    }
  }
};

// Fire when currentLocale computed property changes
</script>

<style lang="scss" scoped>
</style>
