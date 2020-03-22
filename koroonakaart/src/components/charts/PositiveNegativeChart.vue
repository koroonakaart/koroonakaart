<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "PositiveNegativeChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("positiveNegativeTitle"),
          align: "left",
          y: 30        },

        chart: {
          type: "column",
          height: 470
        },

        exporting: {
          buttons: {
              customButton: {
                  text: "Abs",
                  onclick: function() {
                  this.update({
                  plotOptions: {
                  column: {
                  stacking: 'normal'
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
                  stacking: 'percent'
                  }
                  },
                  yAxis: {
                  title: {
                  text: "%"
                  }

                  }
                  });
                  }
              }}},

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },
        navigation: {
        buttonOptions: {
            verticalAlign: 'top',
            y: -15
        }},
        xAxis: {
          labels: {
            style: {
              fontSize: "13px",
              fontWeight: "bold"
            }
          },
          categories: [
            this.$t("insufficientData"),
            "Lääne-Virumaa",
            "Valgamaa",
            "Jõgevamaa",
            "Järvamaa",
            "Läänemaa",
            "Hiiumaa",
            "Viljandimaa",
            "Raplamaa",
            "Põlvamaa",
            "Ida-Virumaa",
            "Tartumaa",
            "Pärnumaa",
            "Võrumaa",
            "Saaremaa",
            "Harjumaa"
          ]
        },

        yAxis: {
          title: {
            text: "%",
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
        plotOptions: {
          column: {
          stacking: "percent",
          enableMouseTracking: true
          }
        },

        series: [
          {
            name: this.$t("negative"),
            data: [165, 47, 23, 21, 18, 21, 17, 44, 69, 20, 40, 183, 189, 85, 345, 1616],
            color: "#A6C96A"
          },
          {
            name: this.$t("positive"),
            data: [11, 1, 1, 1, 1, 2, 2, 2, 2, 3, 6, 21, 22, 34, 94, 123],
            color: "#910000"
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
      this.chartOptions.title.text = this.$t("positiveNegativeTitle");
    //  this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("negative");
      this.chartOptions.series[1].name = this.$t("positive");
      this.chartOptions.xAxis.categories[0] = this.$t("insufficientData");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
