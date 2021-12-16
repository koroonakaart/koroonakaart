<template>
  <b-container>
    <highcharts v-if="mapOptions != null"
                :constructor-type="'mapChart'"
                :options="mapOptions"
                class="map"
                ref="highmap">
    </highcharts>
  </b-container>
</template>

<script>
import Highcharts from "highcharts";
import HighchartsMapModule from "highcharts/modules/map";
import drilldown from "highcharts/modules/drilldown";
import dataModule from "highcharts/modules/data";

import vueRoot from "../main.js";
import mapData from "../data/map/estonia.geo.json";
import importMap from "../utilities/importMap";  // Imports county-level GeoJSON

HighchartsMapModule(Highcharts);
drilldown(Highcharts);
dataModule(Highcharts);

Highcharts.maps["mapEstonia"] = mapData;
Highcharts.setOptions({
  lang: {
    drillUpText: "◁ {series.drillUpText}"
  },
  chart: {
    style: {
  //     fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, "Helvetica Neue", sans-serif'
         textDecoration: "none",
    }
  }
});

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
      mapOptions: null,
      // chartType: "active",
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
    chartData () {
      return this.$store.getters.chartData;
    },
  },

  methods: {
    getMapOptions(chartData) {
      return {
        chartType: "active",
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
              // const button = this.exportSVGElements[2];

              // States:
              // 0 - normal
              // 1 - hover
              // 2 - selected
              // 3 - disabled
              // button.setState(2);
            },

            redraw: function (e) {
              const motion = e.target.motion;
              if (motion) {
                motion.dataSeries = e.target.series;
              }

              if (!this.exportSVGElements) return;
              // Redraw seems to be async so setTimeout for the button to update state
              setTimeout(() => {
                let newTitleText;

                // alert('_this.mapOptions.chartType: ' + _this.mapOptions.chartType);

                switch (this.options.chartType) {
                  case "absolute":
                    newTitleText = vueRoot.$t("cumulativeCases");
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
                this.setTitle({ text: newTitleText });
              }, 100);
            },

            drilldown: function (e) {
              let chart = this;
              chart.motion.pause();

              if (!e.seriesOptions && chart.options.chartType === "absolute") {
                chart.motion.togglePlayControls();

                let drilldowns = chartData.dataMunicipalities.municipalitiesData.map(
                  (item) => {
                    return {
                      name: item[0],
                      id: item[0],
                      keys: [
                        "MNIMI",
                        "ONIMI",
                        "ANIMI",
                        "result",
                        "min",
                        "value",
                      ],
                      data: chartData.dataMunicipalities.municipalitiesData.filter(
                        (element) => element.MNIMI === item.MNIMI
                      ),
                      // evaluate template string to a value to be looked up from importMap
                      // eg item[0] is "Harjumaa"
                      mapData: importMap[`${item[0]}`],
                      joinBy: ["ONIMI"],
                      tooltip: {
                        pointFormat:
                          "{point.ONIMI}: {point.min} - {point.value}<br>",
                        backgroundColor: "#ffffff",
                        style: {
                          opacity: 0.95,
                        },
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
                  }
                );

                let series = drilldowns.find(
                  (element) => element.name === e.point.MNIMI
                );

                chart.addSeriesAsDrilldown(e.point, series);

                this.exportSVGElements[2].hide();
              }
            },

            drillup: function () {
              this.exportSVGElements[2].show();
              this.motion.togglePlayControls();
            },
          },
        },

        exporting: {
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
                "downloadPNG",
                "downloadSVG",
                "downloadCSV"
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
                  text: this.$t("cumulativeCases"),
                  onclick: function () {
                    this.options.chartType = "absolute";

                    this.update({
                      series: {
                        data: chartData.countyByDay.mapPlayback,
                        dataLabels: {
                          format: "{point.MNIMI}<br>{point.value}",
                        },
                      },
                    });

                    this.motion.updateToNewData();
                  },
                },
                {
                  text: this.$t("per10000"),
                  onclick: function () {
                    this.options.chartType = "per10k";

                    this.update({
                      series: {
                        data: chartData.countyByDay.mapPlayback10k,
                        dataLabels: {
                          format: "{point.MNIMI}<br>{point.value}",
                        },
                      },
                    });

                    this.motion.updateToNewData();
                  },
                },
                {
                  text: this.$t("active"),
                  onclick: function () {
                    this.options.chartType = "active";

                    this.update({
                      series: {
                        data: chartData.dataActiveInfectionsByCounty,
                        dataLabels: {
                          format: "{point.MNIMI}<br>{point.value}",
                        },
                      },
                    });

                    this.motion.updateToNewData();
                  },
                },
                {
                  text: this.$t("activeCounty100k"),
                  onclick: function () {
                    this.options.chartType = "active100k";

                    this.update({
                      series: {
                        data: chartData.dataCountyDailyActive.activeMap100kPlayback,
                        dataLabels: {
                          format: "{point.MNIMI}<br>{point.value}",
                        },
                      },
                    });

                    this.motion.updateToNewData();
                  },
                },
              ],
            },
          },

          fallbackToExportServer: false,
        },

        title: {
          text: this.$t("active"),
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
                    textDecoration: "none",
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

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true,
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
          //min: 1,
          //tickPixelInterval: 50,
          type: "linear",
          // Legacy blue colors
          // minColor: "#EEF1FC",
          // maxColor: "#011145",
          stops: [
            [0, "#FDFFDC"],
            [0.143, "#FFE7A4"],
            [0.286, "#FFD37E"],
            [0.429, "#FFBD5D"],
            [0.571, "#FA9A43"],
            [0.714, "#F16835"],
            [0.857, "#D63A2F"],
            [1.0, "#B20213"],
          ],
          // Legacy blue color scale
          // stops: [
          //   [0, "#E5E8F2"],
          //   [0.25, "#3A52A7"],
          //   [0.6, "#1C2F71"],
          //   [1.0, "#071239"],
          // ],

          /* labels: {
            formatter: function () {
              return this.value - 1;
            },
          }, */
        },

        //Legend max width
        legend: {
          symbolWidth: 300,
        },

        motion: {
          enabled: true,
          axisLabel: "date",
          labels: chartData.dates2,
          loop: false,
          series: 0, // The series which holds points to update
          updateInterval: 40,
          magnet: {
            round: "round", // ceil / floor / round
            step: 0.2,
          },
        },

        series: [
          {
            drillUpText: this.$t("faq.back"),
            drilldown: true,
            data: chartData.dataActiveInfectionsByCounty,
            // allowPointSelect: true,
            // keys: ["MNIMI", "sequence", "drilldown"],
            joinBy: "MNIMI",
            name: this.$t("cases"),
            borderColor: "black",
            borderWidth: 0.3,

            // zMin: 1,
            // zMax: 1100,

            states: {
              hover: {
                brightness: 0.15,
                // color: "#a4edba",
              },
            },

            // Customise tooltips
            tooltip: {
              pointFormat: "{point.MNIMI}: {point.value}<br>",

              pointFormatter: function () {
                if (this.value === 0.000001) {
                  return 0;
                } else {
                  return this.value;
                }
              },
              backgroundColor: "#ffffff",
              style: {
                opacity: 0.95,
              },
            },

            dataLabels: {
              enabled: true,
              allowOverlap: true,
              format: "{point.MNIMI}<br>{point.value}",
              //shape: "callout",
              //backgroundColor: "rgba(0, 0, 0, 0.75)",
              style: {
                fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, "Helvetica Neue", sans-serif',
                fontWeight: "500",
                fontSize: "9px",
                color: "#000000",
                "text-anchor": "middle",
                textOutline: "1px solid #ffffff80",  // White with 50% opacity
                // textShadow: "0px 0px 0.5px #333333",
                // textOutline: "1px solid white",
                textShadow: "0px 0px 2px #ffffff8c",  // White with 65% opacity
                textDecoration: "none",
              },
            },
          },

          // This needs to be true for the country map to diplay anything if no data
          /* allAreas: true, */
        ],

        drilldown: {
          activeAxisLabelStyle: {
            color: "darkgrey",
          },
          activeDataLabelStyle: {
            //"letter-spacing": "1px",
            fontWeight: "500",
            color: "black",
            textDecoration: "none",
          },
          series: [],
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
                minWidth: 800,
              },

              chartOptions: {
                series: [
                  {
                    dataLabels: {
                      style: {
                        fontWeight: "500",
                        fontSize: "13px",
                      },
                    },
                  },
                ],
                drilldown: {
                  activeDataLabelStyle: {
                    fontWeight: "500",
                    textDecoration: "none"
                  },
                },
                chart: { height: 600 },
                title: {
                  align: "center",
                  y: 10,
                },
              },
            },
          ],
        },
      };
    },
  },

  created: function () {
      if (this.loaded) {
        this.mapOptions = this.getMapOptions(this.chartData);
      }
  },

  watch: {
    loaded: function () {
      this.mapOptions = this.getMapOptions(this.chartData);
    },
    currentLocale() {
      this.mapOptions.series[0].name = this.$t("cases");
      this.mapOptions.exporting.buttons.toggle.text = this.$t("typeOfData") + " ▾";
      this.mapOptions.exporting.buttons.toggle.menuItems[0].text = this.$t("per10000");
      this.mapOptions.exporting.buttons.toggle.menuItems[1].text = this.$t("cumulativeCases");
      this.mapOptions.exporting.buttons.toggle.menuItems[2].text = this.$t("active");
      this.mapOptions.exporting.buttons.toggle.menuItems[3].text = this.$t("activeCounty100k");

      // Persist chart type selection through language change
      this.mapOptions.chartType === "absolute"
        ? (this.mapOptions.series[0] = this.chartData.dataInfectionsByCounty)
        : this.mapOptions.chartType === "per10k"
        ? (this.mapOptions.series[0] = this.chartData.dataInfectionsByCounty10000)
        : (this.mapOptions.series[0] = this.chartData.dataActiveInfectionsByCounty);

      this.$children[0].chart.drillUp();
    },
  },
};
</script>

<style global lang="scss">
#play-controls {
  margin: 0 auto;
  max-width: 750px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  padding-top: 4px;
  padding-bottom: 7px;
}

#play-pause-button {
  border: 1px solid gray;
  height: 24px;
  width: 36px;
  border-radius: 8px;
}

#play-range {
  min-width: 280px;
  margin: 0 0.5rem;
  flex: 1;
}

#play-output {
  margin: 0;
}

$track-color: #eceff1 !default;
$thumb-color: #4072cd !default;

$thumb-radius: 12px !default;
$thumb-height: 24px !default;
$thumb-width: 24px !default;
$thumb-shadow-size: 4px !default;
$thumb-shadow-blur: 4px !default;
$thumb-shadow-color: rgba(0, 0, 0, 0.2) !default;
$thumb-border-width: 2px !default;
$thumb-border-color: #eceff1 !default;

$track-width: 80% !default;
$track-height: 6px !default;
$track-shadow-size: 0px !default;
$track-shadow-blur: 0px !default;
$track-shadow-color: rgba(0, 0, 0, 0.2) !default;
$track-border-width: 1px !default;
$track-border-color: #555555 !default;

$track-radius: 5px !default;
$contrast: 5% !default;

$ie-bottom-track-color: darken($track-color, $contrast) !default;

@mixin shadow($shadow-size, $shadow-blur, $shadow-color) {
  box-shadow: $shadow-size $shadow-size $shadow-blur $shadow-color,
    0 0 $shadow-size lighten($shadow-color, 5%);
}

@mixin track {
  cursor: default;
  height: $track-height;
  transition: all 0.2s ease;
  width: $track-width;
}

@mixin thumb {
  @include shadow($thumb-shadow-size, $thumb-shadow-blur, $thumb-shadow-color);
  background: $thumb-color;
  border: $thumb-border-width solid $thumb-border-color;
  border-radius: $thumb-radius;
  box-sizing: border-box;
  cursor: default;
  height: $thumb-height;
  width: $thumb-width;
}

[type="range"] {
  -webkit-appearance: none;
  background: transparent;
  margin: $thumb-height / 2 0;
  width: $track-width;

  &::-moz-focus-outer {
    border: 0;
  }

  &:focus {
    outline: 0;

    &::-webkit-slider-runnable-track {
      background: lighten($track-color, $contrast);
    }

    &::-ms-fill-lower {
      background: $track-color;
    }

    &::-ms-fill-upper {
      background: lighten($track-color, $contrast);
    }
  }

  &::-webkit-slider-runnable-track {
    @include track;
    @include shadow(
      $track-shadow-size,
      $track-shadow-blur,
      $track-shadow-color
    );
    background: $track-color;
    border: $track-border-width solid $track-border-color;
    border-radius: $track-radius;
  }

  &::-webkit-slider-thumb {
    @include thumb;
    -webkit-appearance: none;
    margin-top: (
      (-$track-border-width * 2 + $track-height) / 2 - $thumb-height / 2
    );
  }

  &::-moz-range-track {
    @include shadow(
      $track-shadow-size,
      $track-shadow-blur,
      $track-shadow-color
    );
    @include track;
    background: $track-color;
    border: $track-border-width solid $track-border-color;
    border-radius: $track-radius;
    height: $track-height / 2;
  }

  &::-moz-range-thumb {
    @include thumb;
  }

  &::-ms-track {
    @include track;
    background: transparent;
    border-color: transparent;
    border-width: ($thumb-height / 2) 0;
    color: transparent;
  }

  &::-ms-fill-lower {
    @include shadow(
      $track-shadow-size,
      $track-shadow-blur,
      $track-shadow-color
    );
    background: $ie-bottom-track-color;
    border: $track-border-width solid $track-border-color;
    border-radius: ($track-radius * 2);
  }

  &::-ms-fill-upper {
    @include shadow(
      $track-shadow-size,
      $track-shadow-blur,
      $track-shadow-color
    );
    background: $track-color;
    border: $track-border-width solid $track-border-color;
    border-radius: ($track-radius * 2);
  }

  &::-ms-thumb {
    @include thumb;
    margin-top: $track-height / 4;
  }

  &:disabled {
    &::-webkit-slider-thumb,
    &::-moz-range-thumb,
    &::-ms-thumb,
    &::-webkit-slider-runnable-track,
    &::-ms-fill-lower,
    &::-ms-fill-upper {
      cursor: not-allowed;
    }
  }
}
</style>
