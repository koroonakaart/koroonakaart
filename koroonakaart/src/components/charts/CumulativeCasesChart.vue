<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "CumulativeCasesChart",

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
          text: this.$t("cumulativeCases"),
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
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true
        },

        series: [
          {
            name: this.$t("confirmedCases"),
            color: "#2f7ed8",
            data: data.dataCumulativeCasesChart.cases
          },
          {
            name: this.$t("recovered"),
            color: "#90ed7d",
            data: data.dataCumulativeCasesChart.recovered
          },
          {
            name: this.$t("active"),
            color: "#f28f43",
            data: data.dataCumulativeCasesChart.active
          },
          {
            name: this.$t("deceased"),
            color: "#0d233a",
            data: data.dataCumulativeCasesChart.deceased
          },
          {
            name: this.$t("hospitalised"),
            data: data.dataCumulativeCasesChart.haiglas
          },
          {
            name: this.$t("intensive"),
            data: data.dataCumulativeCasesChart.intensive,
            color: "#c42525"
          }
        ],

        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 350
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
      this.chartOptions.title.text = this.$t("cumulativeCases");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("confirmedCases");
      this.chartOptions.series[1].name = this.$t("recovered");
      this.chartOptions.series[2].name = this.$t("active");
      this.chartOptions.series[3].name = this.$t("deceased");
      this.chartOptions.series[4].name = this.$t("hospitalised");
      this.chartOptions.series[5].name = this.$t("intensive");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "logarithmic"
      );
    }
  }
};
</script>

<style lang="scss" scoped></style>
