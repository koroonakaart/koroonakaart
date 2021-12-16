<template>
  <b-container fluid>
    <highcharts v-if="chartOptions"
                class="chart"
                :options="chartOptions">
    </highcharts>
  </b-container>
</template>

<script>
export default {
  name: "CumulativeTestsChart",

  props: {
    height: {
      default: null,
    },
    width: {
      default: null,
    },
  },

  data() {
    return {
      chartOptions: null
    };
  },

  // Get current locale
  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
    loaded () {
      return this.$store.state.loaded;
    },
    caseDates () {
      return this.$store.getters.caseDates;
    },
    dataCumulativeTestsChart () {
      return this.$store.getters.dataCumulativeTestsChart;
    },
  },

  methods: {
    getChartOptions() {
      this.chartOptions = {
        title: {
          text: this.$t("cumulativeTests"),
          align: "left",
          y: 5,
        },

        chartType: "linear",

        chart: {
          height: this.height,
          width: this.width,
          events: {
            load: function () {
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
            redraw: function () {
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
            },
          },
        },

        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "downloadPNG",
                "downloadSVG",
                "downloadCSV",
              ],
            },

            customButton2: {
              text: this.$t("logarithmic"),
              onclick: function () {
                this.options.chartType = "logarithmic";
                this.yAxis[0].update({
                  type: "logarithmic",
                });
              },
            },

            customButton: {
              text: this.$t("linear"),
              onclick: function () {
                this.options.chartType = "linear";
                this.yAxis[0].update({
                  type: "linear",
                });
              },
            },
          },
        },

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true,
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
                    textDecoration: "underline",
                  },
                },
              },
              style: {
                /* color: "#039", */
                /* fontWeight: "bold", */
                textDecoration: "none",
              },
            },
          },
        },

        legend: {
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
        },

        plotOptions: {
          line: {
            /* or spline, area, series, areaspline etc.*/
            marker: {
              enabled: false,
            },
          },
          series: {
            label: {
              connectorAllowed: false,
            },
          },
        },

        xAxis: {
          categories: this.caseDates,
          /* plotLines: [
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
          ] */
        },

        yAxis: {
          title: {
            text: this.$t("numberOfTests"),
          },
        },

        series: [
          {
            name: this.$t("testsAdministered"),
            data: this.dataCumulativeTestsChart.testsAdministered,
          },
        ],

        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 650,
              },

              chartOptions: {
                chart: { marginTop: 80 },
                navigation: {
                  buttonOptions: {
                    y: 20,
                    verticalAlign: "center",
                    theme: {
                      style: {
                        width: "70px",
                      },
                    },
                  },
                },
              },
            },
          ],
        },
      };
    }
  },

  created: function () {
      if (this.loaded) {
        this.getChartOptions();
      }
  },

  watch: {
    loaded: function () {
      this.getChartOptions();
    },
    currentLocale() {
      this.chartOptions.title.text = this.$t("cumulativeTests");
      this.chartOptions.yAxis.title.text = this.$t("numberOfTests");
      this.chartOptions.series[0].name = this.$t("testsAdministered");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "logarithmic"
      );
      /* this.chartOptions.xAxis.plotLines[0].label.text = this.$t("method");
      this.chartOptions.xAxis.plotLines[1].label.text = this.$t("method"); */
    },
  },
};
</script>

<style lang="scss" scoped></style>
