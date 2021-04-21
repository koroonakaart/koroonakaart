<template>
  <b-container fluid>
    <highcharts :constructor-type="'stockChart'" class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "DailyCountyCasesChart",

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
      chartOptions: {
        chartType: "linear",

        title: {
          text: this.$t("confirmedCasesByCounties"),
          align: "left",
          y: 5,
        },

        chart: {
          height: this.height,
          width: this.width,
          events: {
            load: function () {
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
            redraw: function () {
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
                  this.options.chartType === "active" ? 2 : 0
                );
              }, 100);
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

            customButton: {
              text: this.$t("logarithmic"),
              onclick: function () {
                this.update({
                  series: [
                    {
                      name: "Harjumaa",
                      data: data.countyByDay.countyByDay.Harjumaa,
                      color: "#2F7ED8",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Hiiumaa",
                      data: data.countyByDay.countyByDay.Hiiumaa,
                      color: "#456990",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Ida-Virumaa",
                      data: data.countyByDay.countyByDay["Ida-Virumaa"],
                      color: "#49BEAA",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Jõgevamaa",
                      data: data.countyByDay.countyByDay.Jõgevamaa,
                      color: "#49DCB1",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Järvamaa",
                      data: data.countyByDay.countyByDay.Järvamaa,
                      color: "#EEB868",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Läänemaa",
                      data: data.countyByDay.countyByDay.Läänemaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Lääne-Virumaa",
                      data: data.countyByDay.countyByDay["Lääne-Virumaa"],
                      color: "#6684A4",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Põlvamaa",
                      data: data.countyByDay.countyByDay.Põlvamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Pärnumaa",
                      data: data.countyByDay.countyByDay.Pärnumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Raplamaa",
                      data: data.countyByDay.countyByDay.Raplamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Saaremaa",
                      data: data.countyByDay.countyByDay.Saaremaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Tartumaa",
                      data: data.countyByDay.countyByDay.Tartumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Valgamaa",
                      data: data.countyByDay.countyByDay.Valgamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Viljandimaa",
                      data: data.countyByDay.countyByDay.Viljandimaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Võrumaa",
                      data: data.countyByDay.countyByDay.Võrumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                  ],
                });
                this.options.chartType = "logarithmic";

                this.yAxis[0].update({
                  type: "logarithmic",
                  allowNegativeLog: true,
                });
              },
            },
            customButton2: {
              text: this.$t("linear"),
              onclick: function () {
                this.update({
                  series: [
                    {
                      name: "Harjumaa",
                      data: data.countyByDay.countyByDay.Harjumaa,
                      color: "#2F7ED8",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Hiiumaa",
                      data: data.countyByDay.countyByDay.Hiiumaa,
                      color: "#456990",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Ida-Virumaa",
                      data: data.countyByDay.countyByDay["Ida-Virumaa"],
                      color: "#49BEAA",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Jõgevamaa",
                      data: data.countyByDay.countyByDay.Jõgevamaa,
                      color: "#49DCB1",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Järvamaa",
                      data: data.countyByDay.countyByDay.Järvamaa,
                      color: "#EEB868",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Läänemaa",
                      data: data.countyByDay.countyByDay.Läänemaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Lääne-Virumaa",
                      data: data.countyByDay.countyByDay["Lääne-Virumaa"],
                      color: "#6684A4",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Põlvamaa",
                      data: data.countyByDay.countyByDay.Põlvamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Pärnumaa",
                      data: data.countyByDay.countyByDay.Pärnumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Raplamaa",
                      data: data.countyByDay.countyByDay.Raplamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Saaremaa",
                      data: data.countyByDay.countyByDay.Saaremaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Tartumaa",
                      data: data.countyByDay.countyByDay.Tartumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Valgamaa",
                      data: data.countyByDay.countyByDay.Valgamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Viljandimaa",
                      data: data.countyByDay.countyByDay.Viljandimaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Võrumaa",
                      data: data.countyByDay.countyByDay.Võrumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                  ],
                });
                this.options.chartType = "linear";

                this.yAxis[0].update({
                  type: "linear",
                });
              },
            },
            customButton3: {
              text: this.$t("active"),
              onclick: function () {
                this.update({
                  series: [
                    {
                      name: "Harjumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Harjumaa,
                      color: "#2F7ED8",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Hiiumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Hiiumaa,
                      color: "#456990",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Ida-Virumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive[
                          "Ida-Virumaa"
                        ],
                      color: "#49BEAA",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Jõgevamaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Jõgevamaa,
                      color: "#49DCB1",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Järvamaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Järvamaa,
                      color: "#EEB868",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Läänemaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Läänemaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Lääne-Virumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive[
                          "Lääne-Virumaa"
                        ],
                      color: "#6684A4",
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Põlvamaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Põlvamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Pärnumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Pärnumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Raplamaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Raplamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Saaremaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Saaremaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Tartumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Tartumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Valgamaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Valgamaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Viljandimaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive
                          .Viljandimaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                    {
                      name: "Võrumaa",
                      data:
                        data.dataCountyDailyActive.countyByDayActive.Võrumaa,
                      pointStart: Date.parse(data.dates2[0]),
                      pointInterval: 24 * 3600 * 1000,
                    },
                  ],
                });
                this.options.chartType = "active";

                this.yAxis[0].update({
                  type: "linear",
                });
              },
            },
          },
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: true,
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
          /* min: 0, */
          allowNegativeLog: true,
          title: {
            text: this.$t("numberOfCases"),
          },
        },

        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
          footerFormat: "</table>",
          split: false,
          useHTML: true,
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
              enabled: false,
            },
          },
          series: {
            showInNavigator: true,
            label: {
              connectorAllowed: false
            }
          }
        },

        series: [
          {
            name: "Harjumaa",
            data: data.countyByDay.countyByDay.Harjumaa,
            color: "#2F7ED8",
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Hiiumaa",
            data: data.countyByDay.countyByDay.Hiiumaa,
            color: "#456990",
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Ida-Virumaa",
            data: data.countyByDay.countyByDay["Ida-Virumaa"],
            color: "#49BEAA",
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Jõgevamaa",
            data: data.countyByDay.countyByDay.Jõgevamaa,
            color: "#49DCB1",
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Järvamaa",
            data: data.countyByDay.countyByDay.Järvamaa,
            color: "#EEB868",
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Läänemaa",
            data: data.countyByDay.countyByDay.Läänemaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Lääne-Virumaa",
            data: data.countyByDay.countyByDay["Lääne-Virumaa"],
            color: "#6684A4",
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Põlvamaa",
            data: data.countyByDay.countyByDay.Põlvamaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Pärnumaa",
            data: data.countyByDay.countyByDay.Pärnumaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Raplamaa",
            data: data.countyByDay.countyByDay.Raplamaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Saaremaa",
            data: data.countyByDay.countyByDay.Saaremaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Tartumaa",
            data: data.countyByDay.countyByDay.Tartumaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Valgamaa",
            data: data.countyByDay.countyByDay.Valgamaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Viljandimaa",
            data: data.countyByDay.countyByDay.Viljandimaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
          {
            name: "Võrumaa",
            data: data.countyByDay.countyByDay.Võrumaa,
            pointStart: Date.parse(data.dates2[0]),
            pointInterval: 24 * 3600 * 1000,
          },
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
                        width: "70px",
                      },
                    },
                  },
                },
              },
            },
            {
              condition: {
                maxWidth: 575
              },

              chartOptions: {
                legend: {
                  enabled: true
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
  },

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale() {
      this.chartOptions.title.text = this.$t("confirmedCasesByCounties");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.exporting.buttons.customButton.text = this.$t(
        "logarithmic"
      );
      this.chartOptions.exporting.buttons.customButton2.text = this.$t(
        "linear"
      );
      this.chartOptions.exporting.buttons.customButton3.text = this.$t(
        "active"
      );
    },
  },
};
</script>

<style lang="scss" scoped></style>
