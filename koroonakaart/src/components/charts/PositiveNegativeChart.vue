<template>
  <b-container fluid>
    <highcharts
      class="chart"
      :options="chartOptions"
      ref="thisChart"
    ></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "PositiveNegativeChart",

  props: {
    height: {
      default: null
    },
    width: {
      default: null
    }
  },

  data() {
    return {
      chartType: "percent",

      chartOptions: {
        title: {
          text: this.$t("positiveNegativeTitle"),
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
                const button = this.$children[0].chart.exportSVGElements[4];

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
            },

            customButton: {
              text: this.$t("abs"),
              onclick: () => {
                this.chartType = "absolute";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "normal";
                this.$refs.thisChart.options.yAxis.title.text = this.$t("abs");
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

        xAxis: {
          labels: {
            /* padding: "1px", */
            autoRotation: [-10, -20, -30, -40, -50, -60, -70, -80, -85, -90],
            style: {
              fontSize: "11px",
              fontWeight: "bold"
            }
          },

          categories: [
            this.$t("insufficientData"),
            "Harjumaa",
            "Hiiumaa",
            "Ida-Virumaa",
            "Jõgevamaa",
            "Järvamaa",
            "Läänemaa",
            "Lääne-Virumaa",
            "Põlvamaa",
            "Pärnumaa",
            "Raplamaa",
            "Saaremaa",
            "Tartumaa",
            "Valgamaa",
            "Viljandimaa",
            "Võrumaa"
          ]
        },

        yAxis: {
          title: {
            text: "%"
          }
        },

        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b> ({point.percentage:.0f}%)</td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true
        },

        plotOptions: {
          column: {
            stacking: "percent",
            enableMouseTracking: true
          }
        },

        series: [
          {
            name: this.$t("positive"),
            data: data.dataPositiveNegativeChart.positive,
            color: "#000000"
          },
          {
            name: this.$t("negative"),
            data: data.dataPositiveNegativeChart.negative
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
      this.chartOptions.title.text = this.$t("positiveNegativeTitle");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.series[1].name = this.$t("negative");
      this.chartOptions.xAxis.categories[0] = this.$t("insufficientData");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("abs");
      if (this.chartType === "absolute") {
        this.$refs.thisChart.options.yAxis.title.text = this.$t("abs");
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
