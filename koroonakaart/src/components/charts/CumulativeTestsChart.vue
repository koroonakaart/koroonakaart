<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
/* import data from "../../data.json"; */
import tests from "../../data2.json";

import {
  collateDates,
  accumulatedTests
} from "../../utilities/dataCalculations";

export default {
  name: "CumulativeTestsChart",

  mounted() {
    // Update charts when data has been loaded
    this.chartOptions.xAxis.categories = this.cumulativeTests.map(
      item => item.ResultTime
    );
    this.chartOptions.series[0].data = this.cumulativeTests?.map(
      item => item.n
    );
  },

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("cumulativeTests"),
          align: "left",
          y: 30
        },

        chartType: "linear",

        chart: {
          height: 470,
          events: {
            load: function() {
              if (!this.exportSVGElements) return;
              // Buttons have indexes go in even numbers (button1 [0], button2 [2])
              // Odd indexes are button symbols
              const button = this.exportSVGElements[4];

              // States:
              // 0 - normal
              // 1 - hover
              // 2 - selected
              // 3 - disabled
              button.setState(2);
            },
            redraw: function() {
              if (!this.exportSVGElements) return;
              // Redraw seems to be async so setTimeout for the button to update state
              setTimeout(() => {
                this.exportSVGElements[4].setState(
                  this.options.chartType === "linear" ? 2 : 0
                );
                this.exportSVGElements[2].setState(
                  this.options.chartType === "logarithmic" ? 2 : 0
                );
              }, 100);
            }
          }
        },

        exporting: {
          buttons: {
            customButton2: {
              text: this.$t("logarithmic"),
              onclick: function() {
                this.options.chartType = "logarithmic";

                this.yAxis[0].update({
                  type: "logarithmic"
                });
              }
            },
            customButton: {
              text: this.$t("linear"),
              onclick: function() {
                this.options.chartType = "linear";

                this.yAxis[0].update({
                  type: "linear"
                });
              }
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
            y: -15,
            theme: {
              fill: "none",
              stroke: "none",
              "stroke-width": 0,
              r: 4,

              states: {
                hover: {
                  /* fill: "#f5f5f5" */
                },
                select: {
                  fill: "none",
                  style: {
                    fontWeight: "bold",
                    textDecoration: "underline"
                  }
                }
              },
              style: {
                /* color: "#039", */
                /* fontWeight: "bold", */
                textDecoration: "none"
              }
            }
          }
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
          categories: [],
                },

        yAxis: {
          title: {
            text: this.$t("numberOfTests")
          }
        },

        series: [
          {
            name: this.$t("testsAdministered"),
            data: []
          }
        ]
      }
    };
  },

  // Get current locale
  computed: {
    currentLocale: function() {
      return this.$i18n.locale;
    },
    collatedDates: function() {
      return collateDates(tests.tests_by_day);
    },
    cumulativeTests: function() {
      return accumulatedTests(this.collatedDates);
    }
  },

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale() {
      this.chartOptions.title.text = this.$t("cumulativeTests");
      this.chartOptions.yAxis.title.text = this.$t("numberOfTests");
      this.chartOptions.series[0].name = this.$t("testsAdministered");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "logarithmic"
      );
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
