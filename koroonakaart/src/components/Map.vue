<template>
  <b-container>
    <highcharts :constructor-type="'mapChart'" :options="mapOptions" class="map" ref="highmap"></highcharts>
  </b-container>
</template>

<script>
import Highcharts from "highcharts";
import HighchartsMapModule from "highcharts/modules/map";
import dataModule from "highcharts/modules/data";
import drilldown from "highcharts/modules/drilldown";

import mapData from "../data/map/estonia.geo.json";
import Harjumaa from "../data/map/Harju-maakond.geo.json";
import data from "../data.json";

HighchartsMapModule(Highcharts);
dataModule(Highcharts);
drilldown(Highcharts);

Highcharts.maps["mapEstonia"] = mapData;

export default {
  name: "Map",

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
      mapOptions: {
        chartType: "absolute",

        chart: {
          marginTop: 30,
          map: "mapEstonia",
          // Set max height of the map
          height: this.height,
          width: this.width,
          events: {
            drilldown: function(e) {
              console.log(e);
            },

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
                  this.options.chartType === "absolute" ? 2 : 0
                );
                this.exportSVGElements[2].setState(
                  this.options.chartType === "per10k" ? 2 : 0
                );
                this.exportSVGElements[6].setState(
                  this.options.chartType === "active" ? 2 : 0
                );
              }, 100);
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

          chartOptions: {
            // specific options for the exported image
            plotOptions: {
              series: {
                dataLabels: {
                  enabled: true
                }
              }
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
              text: this.$t("per10000"),
              onclick: function() {
                this.options.chartType = "per10k";

                this.update({
                  series: {
                    data: data.dataInfectionsByCounty10000,
                    dataLabels: {
                      format: "{point.MNIMI}"
                    }
                  }
                });
              }
            },

            customButton2: {
              text: this.$t("absolute"),
              onclick: function() {
                this.options.chartType = "absolute";

                this.update({
                  series: {
                    data: data.dataInfectionsByCounty,
                    dataLabels: {
                      format: "{point.MNIMI}"
                    }
                  }
                });
              }
            },
            customButton3: {
              text: this.$t("active"),
              onclick: function() {
                this.options.chartType = "active";

                this.update({
                  series: {
                    data: data.dataActiveInfectionsByCounty.map(point => {
                      if (point[1] === 0) {
                        point[1] = point[1] + 0.000001;
                        return point;
                      } else return point;
                    }),
                    dataLabels: {
                      format: "{point.MNIMI}"
                    }
                  }
                });
              }
            }
          },

          fallbackToExportServer: false
        },

        title: {
          text: ""
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

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        // Navigation controls like zoom etc
        mapNavigation: {
          /* enabled: true, */
          /* enableDoubleClickZoomTo: true, */
          buttonOptions: {
            verticalAlign: "bottom"
          }
        },

        // Legend bar density
        colorAxis: {
          min: 1,
          tickPixelInterval: 50,
          type: "logarithmic",
          /* minColor: "#EEEEFF",
          maxColor: "#000022", */
          /* labels: {
            formatter: function() {
              return this.value - 1;
            }
          }, */

          lineColor: {
            color: {
              /* linearGradient: {
                x1: 0,
                x2: 0,
                y1: 0,
                y2: 1
              }, */

              stops: [
                [0, "#003399"], // start
                [0.5, "#ffffff"], // middle
                [1, "#3366AA"] // end
              ]
            }
          }
        },

        //Legend max width
        legend: {
          symbolWidth: 300
        },

        series: [
          {
            data: data.dataInfectionsByCounty,
            /* allowPointSelect: true, */
            keys: ["MNIMI", "value", "drilldown"],
            joinBy: "MNIMI",
            name: this.$t("cases"),
            borderColor: "black",
            borderWidth: 0.3,
            states: {
              hover: {
                color: "#a4edba"
              }
            },

            // Customise tooltips
            tooltip: {
              pointFormat: "{point.MNIMI}: {point.value}<br/>",

              pointFormatter: function() {
                if (this.value === 0.000001) {
                  return 0;
                } else {
                  return this.value;
                }
              }
            },

            dataLabels: {
              // This needs to be true for the country map to diplay anything if no data
              allAreas: true,
              enabled: true,
              format: "{point.MNIMI}",
              style: {
                fontWeight: "normal",
                fontSize: "9px"
              }
            }
          }
        ],

        drilldown: {
          //dummy data
          series: [
            {
              name: "Harjumaa",
              id: "Harjumaa",
              keys: ["ONIMI", "value"],
              data: [
                ["Harku vald", 58],
                ["Tallinn", 122],
                ["Jõelähtme vald", 88],
                ["Viimsi vald", 41],
                ["Maardu linn", 64]
              ],
              mapData: Harjumaa,
              joinBy: ["ONIMI"],
              tooltip: {
                pointFormat: "{point.ONIMI}: {point.value}<br/>"
              },
              dataLabels: {
                // This needs to be true for the country map to diplay anything if no data
                allAreas: true,
                enabled: true,
                format: "{point.ONIMI}",
                style: {
                  fontWeight: "normal",
                  fontSize: "9px"
                }
              }
            }
          ]

          // This needs to be true for the country map to diplay anything if no data
          /* allAreas: true, */
        ],

        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 500
              },

              chartOptions: {
                navigation: {
                  buttonOptions: {
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
                minWidth: 1000
              },

              chartOptions: {
                chart: { height: 600 }
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
      this.mapOptions.series[0].name = this.$t("cases");
      this.mapOptions.exporting.buttons.customButton.text = this.$t("per10000");
      this.mapOptions.exporting.buttons.customButton2.text = this.$t(
        "absolute"
      );
      this.mapOptions.exporting.buttons.customButton3.text = this.$t("active");

      // Persist chart type selection through language change
      this.mapOptions.chartType === "absolute"
        ? (this.mapOptions.series[0] = data.dataInfectionsByCounty)
        : this.mapOptions.chartType === "per10k"
        ? (this.mapOptions.series[0] = data.dataInfectionsByCounty10000)
        : (this.mapOptions.series[0] = data.dataActiveInfectionsByCounty);
    }
  }
};
</script>

<style scoped></style>
