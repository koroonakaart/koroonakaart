<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions" ref="thisChart"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "genderChart",
  props: {
    height: {
      default: null
    },
    width: {
      default: null
    }
  },

  mounted() {
    /* console.log(this.chartOptions.yAxis.title.text); */
  },

  data() {
    return {
      chartType: "pie",
      chartOptions: {
        title: {
          text: this.$t("testsPerDay"),
          align: "left",
          y: 25
        },

        chart: {
          type: "pie",
          height: this.height,
          width: this.width,
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
              text: this.$t("abs"),
              onclick: () => {
                this.chartType = "absolute";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "normal";
                this.$refs.thisChart.options.yAxis.title.text = this.$t(
                  "numberOfTests"
                );
              }
            },

            customButton2: {
              text: "%",
              onclick: () => {
                this.chartType = "percent";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "percent";
                this.$refs.thisChart.options.yAxis.title.text = "%";
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
            y: -15
          }
        },
        xAxis: {
          categories: data.dates2,
          crosshair: true
        },

        yAxis: [
          {
            min: 0,
            title: {
              text: this.$t("numberOfTests")
            }
          },
          {
            max: 100,
            title: {
              text: this.$t("percentPositiveTests")
            },
            opposite: true
          }
        ],

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
          shared: true,
          useHTML: true
        },

        series: [
          {
            name: "MALE",
            data: data.dataPositiveTestsByAgeChart.maleTotal,
            drilldown: "MALE"
          },
          {
            name: "FEMALE",
            data: data.dataPositiveTestsByAgeChart.femaleTotal,
            drilldown: "FEMALE"
          }
        ],
        drilldown: {
        series:[
        {
        name: "Male",
        id: "MALE",
        data: [
        ["negative",        data.dataPositiveTestsByAgeChart.maleNegative
        ],
        ["positive", data.dataPositiveTestsByAgeChart.malePositive

        ]
        ]
        },
        {
        name: "Female",
        id: "FEMALE",
        data: [
        ["negative",        data.dataPositiveTestsByAgeChart.femaleNegative
        ],
        ["positive", data.dataPositiveTestsByAgeChart.femalePositive

        ]
        ]

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
      this.chartOptions.title.text = this.$t("testsPerDay");
      this.chartOptions.yAxis[0].title.text = this.$t("numberOfTests");
      this.chartOptions.yAxis[1].title.text = this.$t("percentPositiveTests");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.series[1].name = this.$t("negative");
      this.chartOptions.series[2].name = this.$t("percentPositiveTests");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
