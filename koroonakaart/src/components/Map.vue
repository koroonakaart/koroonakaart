<template>
  <b-container>
    <highcharts :constructor-type="'mapChart'" :options="mapOptions" class="map" ref="highmap"></highcharts>
  </b-container>
</template>

<script>
import Highcharts from "highcharts";
import HighchartsMapModule from "highcharts/modules/map";
import drilldown from "highcharts/modules/drilldown";
import dataModule from "highcharts/modules/data";

import vueRoot from "../main.js";
import mapData from "../data/map/estonia.geo.json";
import data from "../data.json";
import importMap from "../utilities/importMap";

HighchartsMapModule(Highcharts);
drilldown(Highcharts);
dataModule(Highcharts);

Highcharts.maps["mapEstonia"] = mapData;
Highcharts.setOptions({ lang: { drillUpText: "◁ {series.drillUpText}" } });

export default {
  name: "Map",

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
      mapOptions: {
        chartType: "absolute",

        chart: {
          marginTop: 30,
          map: "mapEstonia",
          // Set max height of the map
          height: this.height,
          width: this.width,
          events: {
            load: function () {
              if (!this.exportSVGElements) return;
              // Buttons have indexes go in even numbers (button1 [0], button2 [2])
              // Odd indexes are button symbols
              //const button = this.exportSVGElements[2];

              // States:
              // 0 - normal
              // 1 - hover
              // 2 - selected
              // 3 - disabled
              //button.setState(2);
            },

            redraw: function () {
              if (!this.exportSVGElements) return;
              // Redraw seems to be async so setTimeout for the button to update state
              let newTitleText;

              switch (this.options.chartType) {
                case "absolute":
                  newTitleText = vueRoot.$t("absolute");
                  break;
                case "per10k":
                  newTitleText = vueRoot.$t("per10000");
                  break;
                case "active":
                  newTitleText = vueRoot.$t("active");
                  break;
                case "active100k":
                  newTitleText = vueRoot.$t("active100k");
                  break;
              }

              setTimeout(() => {
                console.log(this);
                this.setTitle({ text: newTitleText });

                /* this.exportSVGElements[4].setState(
                  this.options.chartType === "absolute" ? 2 : 0
                );
                this.exportSVGElements[2].setState(
                  this.options.chartType === "per10k" ? 2 : 0
                );
                this.exportSVGElements[6].setState(
                  this.options.chartType === "active" ? 2 : 0
                );
                this.exportSVGElements[8].setState(
                  this.options.chartType === "active100k" ? 2 : 0
                ); */
              }, 100);
            },

            drilldown: function () {
              /* if (this.series[0].options._levelNumber != 1) { */
              this.exportSVGElements[2].hide();
              /* this.exportSVGElements[2].hide();
              this.exportSVGElements[4].hide();
              this.exportSVGElements[6].hide(); */
              /*  }

              this.redraw(); */
            },
            drillup: function () {
              /* if (this.series[0].options._levelNumber == 1) { */
              this.exportSVGElements[2].show();
              /* this.exportSVGElements[2].show();
              this.exportSVGElements[4].show();
              this.exportSVGElements[6].show(); */
              /* }
              this.redraw(); */
            },
          },
        },

        exporting: {
          menuItemDefinitions: {
            embed: {
              onclick: () => {
                this.$store.dispatch("setCurrentChartName", this.$options.name);
                this.$bvModal.show("embed-modal");
              },
              text: "Embed Graph",
            },
          },

          chartOptions: {
            // specific options for the exported image
            plotOptions: {
              series: {
                dataLabels: {
                  enabled: true,
                },
              },
            },
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
                "embed",
              ],
            },

            toggle: {
              text: this.$t("typeOfData") + " ▾",
              align: "right",
              fontSize: 20,
              x: -40,
              y: -15,
              theme: {
                paddingLeft: 10,
                paddingRight: 10,
                "stroke-width": 0,
                stroke: "#4072CD",
                r: 12,
              },
              menuItems: [
                {
                  text: this.$t("per10000"),
                  onclick: function () {
                    this.options.chartType = "per10k";

                    /* this.exportSVGElements[2].attr({
                      text: this.$t("per10000"),
                    }); */

                    this.update({
                      series: {
                        data: data.dataInfectionsByCounty10000,
                        dataLabels: {
                          format: "{point.MNIMI}",
                        },
                      },
                    });
                  },
                },

                {
                  text: this.$t("absolute"),
                  onclick: function () {
                    this.options.chartType = "absolute";

                    this.update({
                      series: {
                        data: data.dataInfectionsByCounty,
                        dataLabels: {
                          format: "{point.MNIMI}",
                        },
                      },
                    });
                  },
                },

                {
                  text: this.$t("active"),
                  onclick: function () {
                    this.options.chartType = "active";

                    this.update({
                      series: {
                        data: data.dataActiveInfectionsByCounty.map((point) => {
                          if (point[1] === 0) {
                            point[1] = point[1] + 0.000001;
                            return point;
                          } else return point;
                        }),
                        dataLabels: {
                          format: "{point.MNIMI}",
                        },
                      },
                    });
                  },
                },

                {
                  text: this.$t("activeCounty100k"),
                  onclick: function () {
                    this.options.chartType = "active100k";

                    this.update({
                      series: {
                        data: data.dataActiveInfectionsByCounty100k.map(
                          (point) => {
                            if (point[1] === 0) {
                              point[1] = point[1] + 0.000001;
                              return point;
                            } else return point;
                          }
                        ),
                        dataLabels: {
                          format: "{point.MNIMI}",
                        },
                      },
                    });
                  },
                },
              ],
            },
          },

          fallbackToExportServer: false,
        },

        title: {
          text: this.$t("absolute"),
          fontSize: 10,
          align: "left",
          y: 30,
          style: { fontSize: 18 },
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
                    letterSpacing: "-0.5px",
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

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false,
        },

        /*
        // Navigation controls like zoom etc
          mapNavigation: {
          enabled: true,
          buttonOptions: {
            verticalAlign: "bottom"
          }
        }, */

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
                [1, "#3366AA"], // end
              ],
            },
          },
        },

        //Legend max width
        legend: {
          symbolWidth: 300,
        },

        series: [
          {
            drillUpText: this.$t("faq.back"),
            data: data.dataInfectionsByCounty,
            /* allowPointSelect: true, */
            keys: ["MNIMI", "value", "drilldown"],
            joinBy: "MNIMI",
            name: this.$t("cases"),
            borderColor: "black",
            borderWidth: 0.3,
            states: {
              hover: {
                color: "#a4edba",
              },
            },

            // Customise tooltips
            tooltip: {
              pointFormat: "{point.MNIMI}: {point.value}<br/>",

              pointFormatter: function () {
                if (this.value === 0.000001) {
                  return 0;
                } else {
                  return this.value;
                }
              },
            },

            dataLabels: {
              enabled: true,
              format: "{point.MNIMI}",
              style: {
                fontWeight: "normal",
                fontSize: "9px",
              },
            },
          },

          // This needs to be true for the country map to diplay anything if no data
          /* allAreas: true, */
        ],
        drilldown: {
          series: data.dataMunicipalities.municipalitiesData.map((item) => {
            if (!item[0].length) {
              return;
            } else
              return {
                name: item[0],
                id: item[0],
                keys: ["MNIMI", "ONIMI", "ANIMI", "result", "min", "value"],
                data: data.dataMunicipalities.municipalitiesData,
                // evaluate template string to a value to be looked up from importMap
                // eg item[0] is "Harjumaa"
                mapData: importMap[`${item[0]}`],
                joinBy: ["ONIMI"],
                tooltip: {
                  pointFormat:
                    "{point.ONIMI}: {point.min} - {point.value}<br/>",
                },
                dataLabels: {
                  allAreas: true,
                  enabled: true,
                  format: "{point.ONIMI}",
                  style: {
                    fontWeight: "normal",
                    fontSize: "9px",
                  },
                },
              };
          }),
          /* [
            {
              name: "Harjumaa",
              id: "Harjumaa",
              keys: ["MNIMI", "ONIMI", "ANIMI", "result", "min", "value"],
              data: data.dataMunicipalities.municipalitiesData,
              mapData: Harjumaa,
              joinBy: ["ONIMI"],
              tooltip: {
                pointFormat: "{point.ONIMI}: {point.min} - {point.value}<br/>"
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
          ] */
        },

        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 500,
              },

              chartOptions: {
                navigation: {
                  buttonOptions: {
                    verticalAlign: "top",
                    theme: {
                      style: {
                        //width: "60px",
                      },
                    },
                  },
                },
              },
            },

            {
              condition: {
                minWidth: 1000,
              },

              chartOptions: {
                chart: { height: 600 },
                title: {
                  align: "center",
                  y: 10,
                },
              },
            },
          ],
        },
      },
    };
  },

  // Get current locale
  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },

    vueRoot() {
      return this.$root;
    },
  },

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale() {
      this.mapOptions.series[0].name = this.$t("cases");
      this.mapOptions.exporting.buttons.toggle.text =
        this.$t("typeOfData") + " ▾";
      this.mapOptions.exporting.buttons.toggle.menuItems[0].text = this.$t(
        "per10000"
      );
      this.mapOptions.exporting.buttons.toggle.menuItems[1].text = this.$t(
        "absolute"
      );
      this.mapOptions.exporting.buttons.toggle.menuItems[2].text = this.$t(
        "active"
      );
      this.mapOptions.exporting.buttons.toggle.menuItems[3].text = this.$t(
        "activeCounty100k"
      );

      // Persist chart type selection through language change
      this.mapOptions.chartType === "absolute"
        ? (this.mapOptions.series[0] = data.dataInfectionsByCounty)
        : this.mapOptions.chartType === "per10k"
        ? (this.mapOptions.series[0] = data.dataInfectionsByCounty10000)
        : (this.mapOptions.series[0] = data.dataActiveInfectionsByCounty);

      this.$children[0].chart.drillUp();
    },
  },
};
</script>

<style scoped></style>
