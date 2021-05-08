<template>
  <b-container fluid>
    <highcharts
      :constructor-type="'stockChart'"
      class="chart"
      :options="chartOptions"
      ref="thisChart"
    ></highcharts>
  </b-container>
</template>

<script>
import data from "../../data/TestsPerDay.json";
import { formatDate, capitalise } from "../../utilities/helper";
import { formatNumberByLocale } from "../../utilities/formatNumberByLocale";

export default {
  name: "TestsPerDayChart",
  props: {
    height: {
      default: null,
    },
    width: {
      default: null,
    },
  },

  mounted() {
    /* console.log(this.chartOptions.yAxis.title.text); */
  },

  data() {
    return {
      chartType: "absolute",
      chartOptions: {
        title: {
          text: this.$t("testsPerDay"),
          align: "left",
          y: 5,
        },

        chart: {
          type: "column",
          height: this.height,
          width: this.width,
          events: {
            // Use lambda to get the component context
            load: () => {
              // setTimeout to be able to access this.$children[0].chart.exportSVGElements
              setTimeout(() => {
                if (!this.$children[0].chart.exportSVGElements) return;

                // Buttons have indexes go in even numbers (button1 [0], button2 [2])
                // Odd indexes are button symbols
                const button = this.$children[0].chart.exportSVGElements[2];

                // States:
                // 0 - normal
                // 1 - hover
                // 2 - selected
                // 3 - disabled
                button.setState(2);
              }, 50);
            },

            redraw: () => {
              // Redraw seems to be async aswell so setTimeout for the button to update state
              setTimeout(() => {
                if (!this.$children[0].chart.exportSVGElements) return;

                this.$children[0].chart.exportSVGElements[4].setState(
                  this.chartType === "percent" ? 2 : 0
                );

                this.$children[0].chart.exportSVGElements[2].setState(
                  this.chartType === "absolute" ? 2 : 0
                );
              }, 50);
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
              text: "Embed chart",
            },
          },
          buttons: {
            contextButton: {
              menuItems: [
                "viewFullscreen",
                "printChart",
                "separator",
                "downloadPNG",
                "downloadSVG",
                "downloadCSV",
                "separator",
                "embed",
              ],
            },
            customButton: {
              text: this.$t("abs"),
              onclick: () => {
                this.chartType = "absolute";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "normal";
                this.$refs.thisChart.options.yAxis[0].title.text = this.$t(
                  "numberOfTests"
                );
              },
            },

            customButton2: {
              text: "%",
              onclick: () => {
                this.chartType = "percent";

                this.$refs.thisChart.options.plotOptions.column.stacking =
                  "percent";
                this.$refs.thisChart.options.yAxis[0].title.text = "%";
              },
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
            day: "%Y<br>%m-%d",
            week: "%Y<br>%m-%d",
            month: "%Y-%m",
            year: "%Y",
          },
          labels: {
            style: {
              fontSize: "11px",
            },
          },
        },

        yAxis: [
          {
            min: 0,
            title: {
              text: this.$t("numberOfTests"),
            },
            opposite: false,
          },
          {
            max: 100,
            title: {
              text: this.$t("percentPositiveTests"),
            },
            opposite: true,
          },
        ],

        legend: {
          enabled: true,
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
          y: 0,
        },

        plotOptions: {
          column: {
            stacking: "normal",
            enableMouseTracking: true,
          },
          spline: {
            /* or spline, area, series, areaspline etc.*/
            marker: {
              enabled: false,
            },
          },
        },

        tooltip: {
          formatter: (context) => {
            // Identify which position in the series and date we are dealing with
            var index = context.chart.hoverPoint.index;
            var x = context.chart.hoverPoint.x;
            // var currentDataGroupingUnit = context.chart.series[0].currentDataGrouping.unitName;

            // Debug
            // console.log('index:');
            // console.log(index);
            // console.log('currentDataGroupingUnit:');
            // console.log(currentDataGroupingUnit);
            // console.log('context.chart:');
            // console.log(context.chart);
            // console.log('');

            // Get data for this date
            var positive;
            if (context.chart.series[0].visible) {
              positive = context.chart.series[0].points.find(
                (element) => element.index === index
              );
            }
            var negative;
            if (context.chart.series[1].visible) {
              negative = context.chart.series[1].points.find(
                (element) => element.index === index
              );
            }
            var positiveTestPercentage;
            if (context.chart.series[2].visible) {
              positiveTestPercentage = context.chart.series[2].points.find(
                (element) => element.index === index
              );
            }

            // Calculate tooltip title
            var tooltipTitle;
            // Get localised date
            // TODO: When data on the chart has been grouped into weeks, the tooltip title should be
            //       in the format: "Week beginning [date]"
            // Get localised date
            var dateOptions = {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
            };
            tooltipTitle = capitalise(
              formatDate(x, this.currentLocale, dateOptions)
            );

            // Compose tooltip
            var tooltip = tooltipTitle + "<br>";
            tooltip += "<table>";
            if (positive !== undefined) {
              tooltip += "<tr>";
              tooltip +=
                "<td>" + context.chart.series[0].name + "&nbsp;&nbsp;</td>";
              tooltip +=
                '<td style="text-align: right"><b>' +
                formatNumberByLocale(positive.y, this.currentLocale) +
                "</b>&nbsp;&nbsp;</td>";
              tooltip +=
                '<td style="text-align: right">(' +
                positive.percentage.toFixed(1) +
                "%)</td>";
              tooltip += "</tr>";
            }
            if (negative !== undefined) {
              tooltip += "<tr>";
              tooltip +=
                "<td>" + context.chart.series[1].name + "&nbsp;&nbsp;</td>";
              tooltip +=
                '<td style="text-align: right"><b>' +
                formatNumberByLocale(negative.y, this.currentLocale) +
                "</b>&nbsp;&nbsp;</td>";
              tooltip +=
                '<td style="text-align: right">(' +
                negative.percentage.toFixed(1) +
                "%)</td>";
              tooltip += "</tr>";
            }
            if (
              positiveTestPercentage !== undefined &&
              positive === undefined
            ) {
              tooltip += "<tr>";
              tooltip +=
                "<td>" + context.chart.series[2].name + "&nbsp;&nbsp;</td>";
              tooltip +=
                '<td style="text-align: right"><b>' +
                positiveTestPercentage.y.toFixed(1) +
                "</b>&nbsp;&nbsp;</td>";
              tooltip += "</tr>";
            }
            tooltip += "</table>";

            return tooltip;
          },
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true,
        },

        series: [
          {
            name: this.$t("positive"),
            data: data.dataTestsPerDayChart.positiveTestsPerDay,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#000000",
            yAxis: 0,
          },
          {
            name: this.$t("negative"),
            data: data.dataTestsPerDayChart.negativeTestsPerDay,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: this.$t("percentPositiveTests"),
            data: data.dataTestsPerDayChart.positiveTestsPercentage,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            type: "spline",
            yAxis: 1,
            // enableMouseTracking: false,
          },
        ],
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
      this.chartOptions.title.text = this.$t("testsPerDay");
      this.chartOptions.yAxis[0].title.text = this.$t("numberOfTests");
      this.chartOptions.yAxis[1].title.text = this.$t("percentPositiveTests");
      this.chartOptions.series[0].name = this.$t("positive");
      this.chartOptions.series[1].name = this.$t("negative");
      this.chartOptions.series[2].name = this.$t("percentPositiveTests");
    },
  },
};
</script>

<style lang="scss" scoped></style>
