<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions" ref="thisChart"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";
import Highcharts from "highcharts";
import drilldown from "highcharts/modules/drilldown";
import dataModule from "highcharts/modules/data";
dataModule(Highcharts);
drilldown(Highcharts);

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
          text: "Test",
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
        tooltip: {
          headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
          pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
        },

        series: [
        {
        name: "Genders",
        colorByPoint: true,
        data: [
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
          ]
      }
        ],
        drilldown: {
        series:[
        {
        name: "Male",
        id: "MALE",
        data: [
        ["negative", data.dataPositiveTestsByAgeChart.maleNegative],
        ["positive", data.dataPositiveTestsByAgeChart.malePositive]
        ]

        },
        {
        name: "Female",
        id: "FEMALE",
        data: [
        ["negative", data.dataPositiveTestsByAgeChart.femaleNegative
        ],
        ["positive", data.dataPositiveTestsByAgeChart.femalePositive

        ]
        ]

        }
        ]
      }
      }
    };
  }
  }


  // Fire when currentLocale computed property changes
</script>

<style lang="scss" scoped>
</style>
