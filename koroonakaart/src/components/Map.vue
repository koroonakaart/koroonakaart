<template>
  <b-container>
    <highcharts :constructor-type="'mapChart'" :options="mapOptions" class="map"></highcharts>
  </b-container>
</template>

<script>
import Highcharts from "highcharts";
import HighchartsMapModule from "highcharts/modules/map";
import mapData from "../data/map/estonia.geo.json";

import { infectionsByCounty } from "../data/map/mapData";

HighchartsMapModule(Highcharts);

Highcharts.maps["mapEstonia"] = mapData;

export default {
  name: "Map",

  data() {
    return {
      mapOptions: {
        chart: {
          map: "mapEstonia",
          // Set max height of the map
          height: 470
        },
        exporting: {
          buttons: {
            customButton: {
              text: this.$t("showValues"),
              onclick: function() {
                this.update({
                  series: {
                    dataLabels: {
                      format: "{point.MNIMI}" + ": " + "{point.value}"
                    }
                  }
                });
              }
            },
            customButton2: {
              text: this.$t("hideValues"),
              onclick: function() {
                this.update({
                  series: {
                    dataLabels: {
                      format: "{point.MNIMI}"
                    }
                  }
                });
              }
            }
          }
        },

        title: {
          text: ""
        },
        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15
          }
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
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
          tickPixelInterval: 25,
          lineColor: {
            color: {
              linearGradient: {
                x1: 0,
                x2: 0,
                y1: 0,
                y2: 1
              },
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
            data: infectionsByCounty,
            keys: ["MNIMI", "value"],
            joinBy: "MNIMI",
            name: this.$t("cases"),
            states: {
              hover: {
                color: "#a4edba"
              }
            },

            // Customise tooltips
            tooltip: {
              pointFormat: "{point.MNIMI}: {point.value}<br/>"
            },

            dataLabels: {
              enabled: true,
              format: "{point.MNIMI}",
              style: {
                fontWeight: "normal",
                fontSize: "9px"
              }
            }
          }

          // This needs to be true for the country map to diplay anything if no data
          /* allAreas: true, */
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
      this.mapOptions.series[0].name = this.$t("cases");
    }
  }
};
</script>

// Border for debugging purposes only
<style scoped>
</style>
