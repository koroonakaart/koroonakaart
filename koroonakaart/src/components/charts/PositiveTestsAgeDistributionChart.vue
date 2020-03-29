<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "PositiveTestsAgeDistributionChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("distributionOfPositiveTests"),
          align: "left",
          y: 30
        },

        chartType: "absolute",

        chart: {
          type: "column",
          height: 470,
          events: {
            load: function() {
              // Buttons have indexes go in even numbers (button1 [0], button2 [2])
              // Odd indexes are button symbols
              const button = this.exportSVGElements[2];

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
                this.exportSVGElements[4].setState(
                  this.options.chartType === "percent" ? 2 : 0
                );
                this.exportSVGElements[2].setState(
                  this.options.chartType === "absolute" ? 2 : 0
                );
              }, 100);
            }
          }
        },

        exporting: {
          buttons: {
            customButton: {
              text: "Abs",
              onclick: function() {
                this.options.chartType = "absolute";

                console.log(this);

                this.update({
                  plotOptions: {
                    column: {
                      stacking: "normal"
                    }
                  },
                  yAxis: {
                    title: {
                      text: "Abs"
                    }
                  }
                });
              }
            },

            customButton2: {
              text: "%",
              onclick: function() {
                this.options.chartType = "percent";

                this.update({
                  plotOptions: {
                    column: {
                      stacking: "percent"
                    }
                  },
                  yAxis: {
                    title: {
                      text: "%"
                    }
                  }
                });
              }
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
        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        xAxis: {
          title: {
            text: this.$t("age")
          },
          categories: [
            "0 - 4",
            "5 - 9",
            "10 - 14",
            "15 - 19",
            "20 - 24",
            "25 - 29",
            "30 - 34",
            "35 - 39",
            "40 - 44",
            "45 - 49",
            "50 - 54",
            "55 - 59",
            "60 - 64",
            "65+",
            this.$t("unknown")
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfTests")
          }
        },
        plotOptions: {
          column: {
            stacking: "normal",
            enableMouseTracking: true
          }
        },
        tooltip: {
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b> ({point.percentage:.0f}%)</td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true
        },
        series: [
          {
            name: this.$t("positive"),
            data: data.dataPositiveTestsByAgeChart.positive
          },
          {
            name: this.$t("negative"),
            data: data.dataPositiveTestsByAgeChart.negative
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
      this.chartOptions.title.text = this.$t("distributionOfPositiveTests");
      this.chartOptions.xAxis.title.text = this.$t("age");
      this.chartOptions.yAxis.title.text = this.$t("numberOfTests");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.series[1].name = this.$t("negative");
      this.chartOptions.xAxis.categories[
        this.chartOptions.xAxis.categories.length - 1
      ] = this.$t("unknown");
      this.chartOptions.exporting.buttons.customButton.text = this.$t("abs");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
