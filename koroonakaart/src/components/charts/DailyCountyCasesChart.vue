<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "DailyCountyCasesChart",

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

        title: {
          text: this.$t("confirmedCasesByCounties"),
          align: "left",
          y: 25
        },

        chart: {
          height: this.height,
          width: this.width,
          events: {
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
                  this.options.chartType === "linear" ? 2 : 0
                );
                this.exportSVGElements[2].setState(
                  this.options.chartType === "logarithmic" ? 2 : 0
                );
                this.exportSVGElements[6].setState(
                  this.options.chartType === "linear" ? 2 : 0
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
              text: this.$t("logarithmic"),
              onclick: function() {
              this.update({
              series: [
                {
                  name: "Harjumaa",
                  data: data.countyByDay.Harjumaa,
                  color: "#2F7ED8"
                },
                {
                  name: "Hiiumaa",
                  data: data.countyByDay.Hiiumaa,
                  color: "#456990"
                },
                {
                  name: "Ida-Virumaa",
                  data: data.countyByDay.IdaVirumaa,
                  color: "#49BEAA"
                },
                {
                  name: "Jõgevamaa",
                  data: data.countyByDay.Jõgevamaa,
                  color: "#49DCB1"
                },
                {
                  name: "Järvamaa",
                  data: data.countyByDay.Järvamaa,
                  color: "#EEB868"
                },
                {
                  name: "Läänemaa",
                  data: data.countyByDay.Läänemaa
                },
                {
                  name: "Lääne-Virumaa",
                  data: data.countyByDay.LääneVirumaa,
                  color: "#6684A4"
                },
                {
                  name: "Põlvamaa",
                  data: data.countyByDay.Põlvamaa
                },
                {
                  name: "Pärnumaa",
                  data: data.countyByDay.Pärnumaa
                },
                {
                  name: "Raplamaa",
                  data: data.countyByDay.Raplamaa
                },
                {
                  name: "Saaremaa",
                  data: data.countyByDay.Saaremaa
                },
                {
                  name: "Tartumaa",
                  data: data.countyByDay.Tartumaa
                },
                {
                  name: "Valgamaa",
                  data: data.countyByDay.Valgamaa
                },
                {
                  name: "Viljandimaa",
                  data: data.countyByDay.Viljandimaa
                },
                {
                  name: "Võrumaa",
                  data: data.countyByDay.Võrumaa
                }
              ]
              });
              this.options.chartType = "logarithmic";

              this.yAxis[0].update({
                type: "logarithmic",
                allowNegativeLog: true

              });
              }
            },
            customButton2: {
              text: this.$t("linear"),
              onclick: function() {

                this.update({
                series: [
                  {
                    name: "Harjumaa",
                    data: data.countyByDay.Harjumaa,
                    color: "#2F7ED8"
                  },
                  {
                    name: "Hiiumaa",
                    data: data.countyByDay.Hiiumaa,
                    color: "#456990"
                  },
                  {
                    name: "Ida-Virumaa",
                    data: data.countyByDay.IdaVirumaa,
                    color: "#49BEAA"
                  },
                  {
                    name: "Jõgevamaa",
                    data: data.countyByDay.Jõgevamaa,
                    color: "#49DCB1"
                  },
                  {
                    name: "Järvamaa",
                    data: data.countyByDay.Järvamaa,
                    color: "#EEB868"
                  },
                  {
                    name: "Läänemaa",
                    data: data.countyByDay.Läänemaa
                  },
                  {
                    name: "Lääne-Virumaa",
                    data: data.countyByDay.LääneVirumaa,
                    color: "#6684A4"
                  },
                  {
                    name: "Põlvamaa",
                    data: data.countyByDay.Põlvamaa
                  },
                  {
                    name: "Pärnumaa",
                    data: data.countyByDay.Pärnumaa
                  },
                  {
                    name: "Raplamaa",
                    data: data.countyByDay.Raplamaa
                  },
                  {
                    name: "Saaremaa",
                    data: data.countyByDay.Saaremaa
                  },
                  {
                    name: "Tartumaa",
                    data: data.countyByDay.Tartumaa
                  },
                  {
                    name: "Valgamaa",
                    data: data.countyByDay.Valgamaa
                  },
                  {
                    name: "Viljandimaa",
                    data: data.countyByDay.Viljandimaa
                  },
                  {
                    name: "Võrumaa",
                    data: data.countyByDay.Võrumaa
                  }
                ]
                });
                this.options.chartType = "linear";

                this.yAxis[0].update({
                  type: "linear"
                });
              }
            }
          ,
          customButton3: {
            text: this.$t("active"),
            onclick: function() {
              this.update({
              series: [
                {
                  name: "Harjumaa",
                  data: data.dataCountyDailyActive.Harjumaa,
                  color: "#2F7ED8"
                },
                {
                  name: "Hiiumaa",
                  data: data.dataCountyDailyActive.Hiiumaa,
                  color: "#456990"
                },
                {
                  name: "Ida-Virumaa",
                  data: data.dataCountyDailyActive.IdaVirumaa,
                  color: "#49BEAA"
                },
                {
                  name: "Jõgevamaa",
                  data: data.dataCountyDailyActive.Jõgevamaa,
                  color: "#49DCB1"
                },
                {
                  name: "Järvamaa",
                  data: data.dataCountyDailyActive.Järvamaa,
                  color: "#EEB868"
                },
                {
                  name: "Läänemaa",
                  data: data.dataCountyDailyActive.Läänemaa
                },
                {
                  name: "Lääne-Virumaa",
                  data: data.dataCountyDailyActive.LääneVirumaa,
                  color: "#6684A4"
                },
                {
                  name: "Põlvamaa",
                  data: data.dataCountyDailyActive.Põlvamaa
                },
                {
                  name: "Pärnumaa",
                  data: data.dataCountyDailyActive.Pärnumaa
                },
                {
                  name: "Raplamaa",
                  data: data.dataCountyDailyActive.Raplamaa
                },
                {
                  name: "Saaremaa",
                  data: data.dataCountyDailyActive.Saaremaa
                },
                {
                  name: "Tartumaa",
                  data: data.dataCountyDailyActive.Tartumaa
                },
                {
                  name: "Valgamaa",
                  data: data.dataCountyDailyActive.Valgamaa
                },
                {
                  name: "Viljandimaa",
                  data: data.dataCountyDailyActive.Viljandimaa
                },
                {
                  name: "Võrumaa",
                  data: data.dataCountyDailyActive.Võrumaa
                }
              ]
              });

                          this.yAxis[0].update({
                            type: "linear"
                          });
                          this.options.chartType = "linear";
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
          categories: data.dates2,
          crosshair: true
        },

        yAxis: {
          /* min: 0, */
          allowNegativeLog: true,
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
            name: "Harjumaa",
            data: data.countyByDay.Harjumaa,
            color: "#2F7ED8"
          },
          {
            name: "Hiiumaa",
            data: data.countyByDay.Hiiumaa,
            color: "#456990"
          },
          {
            name: "Ida-Virumaa",
            data: data.countyByDay.IdaVirumaa,
            color: "#49BEAA"
          },
          {
            name: "Jõgevamaa",
            data: data.countyByDay.Jõgevamaa,
            color: "#49DCB1"
          },
          {
            name: "Järvamaa",
            data: data.countyByDay.Järvamaa,
            color: "#EEB868"
          },
          {
            name: "Läänemaa",
            data: data.countyByDay.Läänemaa
          },
          {
            name: "Lääne-Virumaa",
            data: data.countyByDay.LääneVirumaa,
            color: "#6684A4"
          },
          {
            name: "Põlvamaa",
            data: data.countyByDay.Põlvamaa
          },
          {
            name: "Pärnumaa",
            data: data.countyByDay.Pärnumaa
          },
          {
            name: "Raplamaa",
            data: data.countyByDay.Raplamaa
          },
          {
            name: "Saaremaa",
            data: data.countyByDay.Saaremaa
          },
          {
            name: "Tartumaa",
            data: data.countyByDay.Tartumaa
          },
          {
            name: "Valgamaa",
            data: data.countyByDay.Valgamaa
          },
          {
            name: "Viljandimaa",
            data: data.countyByDay.Viljandimaa
          },
          {
            name: "Võrumaa",
            data: data.countyByDay.Võrumaa
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
      this.chartOptions.title.text = this.$t("confirmedCasesByCounties");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.exporting.buttons.customButton.text = this.$t(
        "logarithmic"
      );
      this.chartOptions.exporting.buttons.customButton2.text = this.$t("linear");
      this.chartOptions.exporting.buttons.customButton3.text = this.$t(
        "active"
      );
    }
  }
};
</script>

<style lang="scss" scoped></style>
