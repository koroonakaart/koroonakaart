<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "CumulativeCasesChart",

  data() {
    return {
      chartType: "linear",

      chartOptions: {
        title: {
          text: this.$t("cumulativeCases"),
          align: "left",
          y: 30
        },

        exporting: {
          buttons: {
            customButton: {
              text: this.$t("logarithmic"),
              onclick: function() {
                this.chartType = "logarithmic";
                const button1 = this.exportSVGElements[4];
                const button2 = this.exportSVGElements[2];

                button1.setState(this.chartType === "linear" ? 2 : 0);
                button2.setState(this.chartType === "logarithmic" ? 2 : 0);

                this.yAxis[0].update({
                  type: "logarithmic"
                });
              }
            },
            customButton2: {
              text: this.$t("linear"),
              onclick: function() {
                this.chartType = "linear";
                const button1 = this.exportSVGElements[4];
                const button2 = this.exportSVGElements[2];

                button1.setState(this.chartType === "linear" ? 2 : 0);
                button2.setState(this.chartType === "logarithmic" ? 2 : 0);

                this.yAxis[0].update({
                  type: "linear"
                });
              }
            }
          }
        },

        chart: {
          height: 470,
          events: {
            load: function() {
              // Buttons have indexes go in even numbers (button1 [0], button2 [2])
              // Odd indexes are button symbols
              const button = this.exportSVGElements[4];

              // States:
              // 0 - normal
              // 1 - hover
              // 2 - selected
              // 3 - disabled
              button.setState(2);
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
          categories: data.dates2,
          plotLines: [{
              color: 'red', // Color value
              value: 18, // Value of where the line will appear
              width: 1,
              label: {
              text: this.$t("method"),
              align: "left"
              }
            }, {
                color: 'red', // Color value
                value: 28, // Value of where the line will appear
                width: 1,
                label: {
                text: this.$t("method"),
                align: "left",
                x: -20

                }}
            ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
          }
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
      this.xAxis[0].plotLines.text = this.$t("method");
      this.xAxis[1].plotLines.text = this.$t("method");

    }
  }
};
</script>

<style lang="scss" scoped>
</style>
