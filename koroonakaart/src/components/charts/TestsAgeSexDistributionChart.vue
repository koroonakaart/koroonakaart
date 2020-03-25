<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
import data from "../../data.json";

export default {
  name: "TestsAgeSexDistributionChart",

  categories: ["0 - 4", "5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54", "55 - 59", "60 - 64", "65+",],
  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("distributionOfAgeSexTests"),
          align: "left",
          y: 30
        },
        exporting: {
          buttons: {
            customButton: {
              text: "Abs",
              onclick: function() {
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
        chart: {
          type: "column",
          height: 470
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

        xAxis: [{
          categories: this.categories,
          reversed: false,
          labels: {
             step:1
          }},
          {
            opposite: true,
            reversed: false,
            categories: this.categories,
            linkedTo: 0,
            labels: {
                step: 1
            },
        }],

        yAxis: {
          title: {
            text: this.$t("numberOfTests")
          },
    labels: {
      formatter: function () {
        return Math.abs(this.value);
			}
      }
        },
        plotOptions: {
          column: {
            stacking: "normal",
            enableMouseTracking: true
          }
        },
        
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + ', this.$t("age") ' + this.point.category + '</b><br/>' +
                'this.$t("numberOfTests")' + ': ' + Math.abs(this.point.y);
        }
    },
        series: [
	{
    name: this.$t("maleNegative"),
            data: data.dataPositiveTestsByAgeChart.maleNegative.map(x => x * (-1)),
            color: "#97beeb" 
          },
          {
            name: this.$t("malePositive"),
            data: data.dataPositiveTestsByAgeChart.malePositive.map(x => x * (-1)),
            color: "#2f7ed8" 
          },
           {
            name: this.$t("femaleNegative"),
            data: data.dataPositiveTestsByAgeChart.femaleNegative,
            color: "#917ea9"
          },
          {
            name: this.$t("femalePositive"),
            data: data.dataPositiveTestsByAgeChart.femalePositive,
            color: "#492970"
          },
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
      this.chartOptions.title.text = this.$t("distributionOfAgeSexTests");
      this.chartOptions.xAxis.title.text = this.$t("age");
      this.chartOptions.yAxis.title.text = this.$t("numberOfTests"); 
      this.chartOptions.series[1].name = this.$t("maleNegative");
      this.chartOptions.series[0].name = this.$t("malePositive");
      this.chartOptions.series[3].name = this.$t("femaleNegative");
      this.chartOptions.series[2].name = this.$t("femalePositive");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
