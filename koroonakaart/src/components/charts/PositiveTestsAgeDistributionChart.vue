<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions" ref="thisChart"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "PositiveTestsAgeDistributionChart",

  data() {
    return {
      chartType: "absolute",

      props: {
        height: {
          default: null
        },
        width: {
          default: null
        }
      },

      chartOptions: {
        title: {
          text: this.$t("distributionOfPositiveTests"),
          align: "left",
          y: 25
        },

        chart: {
          type: "column",
          height: this.height,
          width: this.width,
          events: {
            // Use lambda to get the component context
            load: () => {
              // setTimeout to be able to access this.$children[0].chart.exportSVGElements
              setTimeout(() => {
                if (!this.$children[0].chart.exportSVGElements) return;

                // Buttons have indexes go in even numbers (button1 [0], button2 [2])
                // Odd indexes are button symbols
                const button = this.$children[0].chart.exportSVGElements[2];

                // States:
                // 0 - normal
                // 1 - hover
                // 2 - selected
                // 3 - disabled
                button.setState(2);
              }, 50);
            },

            redraw: () => {
              // Redraw seems to be async aswell so setTimeout for the button to update state
              setTimeout(() => {
                if (!this.$children[0].chart.exportSVGElements) return;

                this.$children[0].chart.exportSVGElements[4].setState(
                  this.chartType === "percent" ? 2 : 0
                );

                this.$children[0].chart.exportSVGElements[2].setState(
                  this.chartType === "absolute" ? 2 : 0
                );
              }, 50);
            }
          }
        },

        exporting: {
          menuItemDefinitions: {
            embed: {
              onclick: () => {
                this.$store.dispatch("setCurrentChartName", this.$options.name);
                this.$bvModal.show("embed-modal");
              },
              text: "Embed chart"
            }
          },

          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "separator",
                "downloadPNG",
                "downloadSVG",
                "downloadCSV",
                "separator",
                "embed"
              ]
            },

            customButton: {
              text: this.$t("abs"),
              onclick: () => {
                this.chartType = "absolute";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "normal";
                this.$refs.thisChart.options.yAxis.title.text = this.$t(
                  "numberOfTests"
                );
              }
            },

            customButton2: {
              text: "%",
              onclick: () => {
                this.chartType = "percent";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "percent";
                this.$refs.thisChart.options.yAxis.title.text = "%";
              }
            }
          }
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

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true
        },

        xAxis: {
          title: {
            text: this.$t("age")
          },
          labels: {
            /* padding: "1px", */
            autoRotation: [
              -10,
              -20,
              -30,
              -40,
              -50,
              -60,
              -70,
              -80,
              -85,
              -88,
              -90
            ],
            style: {
              fontSize: "10px",
              fontWeight: "bold"
            }
          },

          categories: [
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
            "65 - 69",
            "70 - 74",
            "75 - 79",
            "80 - 85",
            "85+",
            this.$t("unknown")
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfTests")
          }
        },
        plotOptions: {
          column: {
            stacking: "normal",
            enableMouseTracking: true
          }
        },
        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b> ({point.percentage:.1f}%)</td></tr>',
          footerFormat: "</table>",
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true
        },
        series: [
          {
            name: this.$t("positive"),
            data: data.dataPositiveTestsByAgeChart.positive,
            color: "#000000"
          },
          {
            name: this.$t("negative"),
            data: data.dataPositiveTestsByAgeChart.negative
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
      this.chartOptions.title.text = this.$t("distributionOfPositiveTests");
      this.chartOptions.xAxis.title.text = this.$t("age");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.series[1].name = this.$t("negative");
      this.chartOptions.xAxis.categories[
        this.chartOptions.xAxis.categories.length - 1
      ] = this.$t("unknown");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("abs");
      if (this.chartType === "absolute") {
        this.chartOptions.yAxis.title.text = this.$t("numberOfTests");
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
