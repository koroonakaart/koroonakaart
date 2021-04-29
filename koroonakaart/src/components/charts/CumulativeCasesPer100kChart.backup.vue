<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";
import { formatTooltip } from "../../utilities/formatTooltip";

export default {
  name: "CumulativeCasesPer100kChart",

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
      chartOptions: {
        chartType: "linear",

        chart: {
          height: this.height,
          width: this.width,
          events: {
            load: function() {
              // Buttons have indexes go in even numbers (button1 [0], button2 [2])
              // Odd indexes are button symbols
              if (!this.exportSVGElements) return;

              const button = this.exportSVGElements[4];

              // States:
              // 0 - normal
              // 1 - hover
              // 2 - selected
              // 3 - disabled
              button.setState(2);
            },
            redraw: function() {
              // Redraw seems to be async so setTimeout for the button to update state
              setTimeout(() => {
                if (!this.exportSVGElements) return;

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

        title: {
          text: this.$t("cumulativeCasesPer100k"),
          align: "left",
          y: 5
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

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true
        },

        legend: {
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom"
        },

        plotOptions: {
          line: {
            /* or spline, area, series, areaspline etc.*/
            marker: {
              enabled: false
            }
          },
          series: {
            label: {
              connectorAllowed: false
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

        xAxis: {
          categories: data.dates2
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
          }
        },

        tooltip: {
          formatter: (context) => {
              return formatTooltip(context, this.chartOptions.series, this.currentLocale, 1);
          },
          // headerFormat:
          //   '<span>{point.key}</span><table>',
          // pointFormat:
          //   '<tr><td><span style="color:{series.color}">●</span> {series.name}&nbsp;&nbsp;</td>' +
          //   '<td><b>{point.y}</b></td></tr>',
          // footerFormat: "</table>",
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true,
          valueDecimals: 1
        },

        series: [
          {
            name: this.$t("active100k"),
            color: "#2f7ed8",
            data: data.dataCumulativeCasesChart.active100k
          }
        ],

        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 670
              },

              chartOptions: {
                chart: { marginTop: 70 },
                navigation: {
                  buttonOptions: {
                    y: 10,
                    verticalAlign: "center",
                    theme: {
                      style: {
                        width: "70px"
                      }
                    }
                  }
                }
              }
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
      this.chartOptions.title.text = this.$t("cumulativeCasesPer100k");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("active100k");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "logarithmic"
      );
    }
  }
};
</script>

<style lang="scss" scoped></style>
