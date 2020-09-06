<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

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
          width: this.width
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
            name: this.$t("active100k"),
            color: "#2f7ed8",
            data: data.dataCumulativeCasesChart.active100k
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
      this.chartOptions.title.text = this.$t("cumulativeCasesPer100k");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("active100k");
    }
  }
};
</script>

<style lang="scss" scoped></style>
