<template>
  <b-container fluid>
    <highcharts v-if="chartOptions"
                class="chart"
                :options="chartOptions"
                ref="thisChart">
    </highcharts>
  </b-container>
</template>

<script>
import Highcharts from "highcharts";
import drilldown from "highcharts/modules/drilldown";
import dataModule from "highcharts/modules/data";

dataModule(Highcharts);
drilldown(Highcharts);

Highcharts.setOptions({ lang: { drillUpText: "◁ {series.drillUpText}" } });

export default {
  name: "GenderChart",

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
      chartOptions: null
    };
  },

  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
    loaded () {
      return this.$store.state.loaded;
    },
    dataPositiveTestsByAgeChart () {
      return this.$store.state.data.dataPositiveTestsByAgeChart;
    }
  },

  methods: {
    getChartOptions() {
      this.chartOptions = {
        title: {
          text: this.$t("genderChart"),
          align: "left",
          y: 5,
        },

        chart: {
          type: "pie",
          height: this.height,
          width: this.width,
        },

        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "downloadPNG",
                "downloadSVG",
                "downloadCSV",
              ],
            },
          },
        },

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true,
        },
        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15,
          },
        },
        tooltip: {
          pointFormat:
            '<tr><td style="color:{series.color};padding:0"></td>' +
            '<td style="padding:0"><b>{point.y}</b>&nbsp;&nbsp;({point.percentage:.1f}%)</td></tr>',
          footerFormat: "</table>",
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true,
        },

        series: [
          {
            name: "chart",
            drillUpText: this.$t("faq.back"),
            colorByPoint: true,
            data: [
              {
                name: this.$t("male"),
                y: this.dataPositiveTestsByAgeChart.maleTotal,
                drilldown: "MALE",
              },
              {
                name: this.$t("female"),
                y: this.dataPositiveTestsByAgeChart.femaleTotal,
                drilldown: "FEMALE",
              },
            ],
          },
        ],

        drilldown: {
          series: [
            {
              name: this.$t("male"),
              id: "MALE",
              tooltip: {
                pointFormat:
                  '<tr><td style="color:{series.color};padding:0"></td>' +
                  '<td style="padding:0"><b>{point.y}</b>&nbsp;&nbsp;({point.percentage:.1f}%)</td></tr>',
                footerFormat: "</table>",
                backgroundColor: "#ffffff",
                style: {
                  opacity: 0.95,
                },
                shared: true,
                useHTML: true,
              },
              data: [
                [
                  this.$t("maleNegative"),
                  this.dataPositiveTestsByAgeChart.maleNegative.reduce(
                    (a, b) => a + b,
                    0
                  ),
                ],
                [
                  this.$t("malePositive"),
                  this.dataPositiveTestsByAgeChart.malePositive.reduce(
                    (a, b) => a + b,
                    0
                  ),
                ],
              ],
            },
            {
              name: this.$t("female"),
              id: "FEMALE",
              tooltip: {
                pointFormat:
                  '<tr><td style="color:{series.color};padding:0"></td>' +
                  '<td style="padding:0"><b>{point.y}</b>&nbsp;&nbsp;({point.percentage:.1f}%)</td></tr>',
                footerFormat: "</table>",
                shared: true,
                useHTML: true,
              },
              data: [
                [
                  this.$t("femaleNegative"),
                  this.dataPositiveTestsByAgeChart.femaleNegative.reduce(
                    (a, b) => a + b,
                    0
                  ),
                ],
                [
                  this.$t("femalePositive"),
                  this.dataPositiveTestsByAgeChart.femalePositive.reduce(
                    (a, b) => a + b,
                    0
                  ),
                ],
              ],
            },
          ],
        },
      };
    }
  },

  created: function () {
      if (this.loaded) {
        this.getChartOptions();
      }
  },

  watch: {
    loaded: function () {
      this.getChartOptions();
    },
    currentLocale() {
      this.chartOptions.title.text = this.$t("genderChart");
      this.chartOptions.series[0].data[0].name = this.$t("male");
      this.chartOptions.series[0].data[1].name = this.$t("female");
      this.chartOptions.drilldown.series[0].data[0][0] = this.$t(
        "maleNegative"
      );
      this.chartOptions.drilldown.series[0].data[1][0] = this.$t(
        "malePositive"
      );
      this.chartOptions.drilldown.series[1].data[0][0] = this.$t(
        "femaleNegative"
      );
      this.chartOptions.drilldown.series[1].data[1][0] = this.$t(
        "femalePositive"
      );

      this.$children[0].chart.drillUp();
    },
  },
};
</script>

<style lang="scss" scoped></style>
