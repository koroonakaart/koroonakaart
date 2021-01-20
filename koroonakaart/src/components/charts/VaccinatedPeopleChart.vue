<template>
  <b-container fluid>
    <highcharts :constructor-type="'stockChart'" class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "VaccinatedPeopleChart",

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
        chartFirstDate: Date.UTC(2020, 12, 26),

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

        rangeSelector: {
          selected: 5
        },

        title: {
          text: this.$t("vaccination"),
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
          enabled: true
        },

        legend: {
          enabled: true,
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
          y: 0
        },

        plotOptions: {
          line: {
            /* or spline, area, series, areaspline etc.*/
            marker: {
              enabled: false
            }
          },
          series: {
            showInNavigator: true,
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
          type: "datetime",
          dateTimeLabelFormats: {
            day: "%Y<br/>%m-%d",
            week: "%Y<br/>%m-%d",
            month: "%Y-%m",
            year: "%Y"
          },
          labels: {
            style: {
              fontSize: "11px"
            }
          }
        },

        yAxis: {
          title: {
            text: this.$t("vaccination")
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
            name: this.$t("allVaccinated"),
            color: "#2f7ed8",
            pointStart: Date.parse(data.dates3[0]),
            pointInterval: 24 * 3600 * 1000, // one day
            data: data.dataVaccinatedPeopleChart.vaccinesAll
          },
          {
            name: this.$t("vaccinationNumber"),
            color: "#90ed7d",
            pointStart: Date.parse(data.dates3[0]),
            pointInterval: 24 * 3600 * 1000, // one day
            data: data.dataVaccinatedPeopleChart.vaccinesProgress
          },
          {
            name: this.$t("completedVaccinationNumber"),
            color: "#f28f43",
            pointStart: Date.parse(data.dates3[0]),
            pointInterval: 24 * 3600 * 1000, // one day
            data: data.dataVaccinatedPeopleChart.vaccinesCompleted
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
            },
            {
              condition: {
                maxWidth: 575
              },

              chartOptions: {
                legend: {
                  enabled: true
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

  /* mounted() {
    this.chartOptions.
  }, */

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale() {
      this.chartOptions.title.text = this.$t("vaccination");
      this.chartOptions.yAxis.title.text = this.$t("vaccination");
      this.chartOptions.series[0].name = this.$t("allVaccinated");
      this.chartOptions.series[1].name = this.$t("vaccinationNumber");
      this.chartOptions.series[2].name = this.$t("completedVaccinationNumber");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "logarithmic"
      );
    }
  }
};
</script>

<style lang="scss" scoped></style>
