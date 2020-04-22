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
    console.log(this)
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
        name: "Gender",
        colorByPoint: true,
        data: [
        {
            name: "Male",
            y: data.dataPositiveTestsByAgeChart.maleTotal,
            drilldown: "Male"
          },
          {
            name: "Female",
            y: data.dataPositiveTestsByAgeChart.femaleTotal,
            drilldown: "Female"
          }
          ]
      }
        ],
        drilldown: {
        series:[
        {
        name: "Male",
        id: "Male",
        data: [
        ["negative", data.dataPositiveTestsByAgeChart.maleNegativeTotal],
        ["positive", data.dataPositiveTestsByAgeChart.malePositiveTotal]
        ]

        },
        {
        name: "Female",
        id: "Female",
        data: [
        ["negative", data.dataPositiveTestsByAgeChart.femaleNegativeTotal],
        ["positive", data.dataPositiveTestsByAgeChart.femalePositiveTotal

        ]
        ]

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
      this.chartOptions.title.text = this.$t("newCasesPerDay");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("confirmedCases");
      this.chartOptions.series[1].name = this.$t("recovered");
      this.chartOptions.series[2].name = this.$t("deceased");
    }
  }
  };


  // Fire when currentLocale computed property changes
</script>
