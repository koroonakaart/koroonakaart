<template>
  <b-container fluid>
    <div v-if="loading" class="loading">
      {{ $t("loading") }}
    </div>

    <highcharts
      v-if="!loading"
      :constructor-type="'stockChart'"
      class="chart"
      :options="chartOptions"
      ref="thisChart"
    ></highcharts>
  </b-container>
</template>

<script>
import { capitalise, formatDate } from "../../utilities/helper";
import { formatNumberByLocale } from "../../utilities/formatNumberByLocale";

export default {
  name: "DailyCountyNewCasesChart",
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
      loading: true,
      chartType: "absolute",
      chartOptions: null,
    };
  },

  created() {
    this.fetchData();
  },

  methods: {
    fetchData() {
      let _this = this;
      import("../../data/DailyCountyNewCases.json").then((data) => {
        _this.chartOptions = _this.makeData(data);
        _this.loading = false;
      });
    },

    makeData(data) {
      return {
        title: {
          text: this.$t("confirmedNewCasesByCounties"),
          align: "left",
          y: 5,
        },

        chart: {
          type: "column",
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

        yAxis: {
          min: 0,
          title: {
            text: this.$t("numberOfCases"),
          },
          opposite: false,
        },

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
            var x = context.chart.hoverPoint.x;

            // Get data for this date
            var countyName = context.chart.hoverPoint.series.name;
            var color = context.chart.hoverPoint.series.color;
            var value = context.chart.hoverPoint.y;

            // Get localised date
            var dateOptions = {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
            };
            var tooltipDate = capitalise(
              formatDate(x, this.currentLocale, dateOptions)
            );

            // Compose tooltip
            var tooltip = tooltipDate + "<br>";
            tooltip += "<table>";
            tooltip += "<tr>";
            tooltip +=
              '<td><span style="color: ' +
              color +
              '">●</span> ' +
              countyName +
              "&nbsp;&nbsp;</td>";
            tooltip +=
              '<td style="text-align: right"><b>' +
              formatNumberByLocale(value, this.currentLocale) +
              "</b></td>";
            tooltip += "</tr>";
            tooltip += "</table>";

            return tooltip;
          },
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          split: false,
          useHTML: true,
        },

        rangeSelector: {
          selected: 0,
        },

        series: [
          {
            name: "Harjumaa",
            data: data.newCountyByDay.Harjumaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#2F7ED8",
            yAxis: 0,
          },
          {
            name: "Hiiumaa",
            data: data.newCountyByDay.Hiiumaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#456990",
            yAxis: 0,
          },
          {
            name: "Ida-Virumaa",
            data: data.newCountyByDay["Ida-Virumaa"],
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#49BEAA",
            yAxis: 0,
          },
          {
            name: "Jõgevamaa",
            data: data.newCountyByDay.Jõgevamaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#49DCB1",
            yAxis: 0,
          },
          {
            name: "Järvamaa",
            data: data.newCountyByDay.Järvamaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#EEB868",
            yAxis: 0,
          },
          {
            name: "Läänemaa",
            data: data.newCountyByDay.Läänemaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#7CB5EC",
            yAxis: 0,
          },
          {
            name: "Lääne-Virumaa",
            data: data.newCountyByDay["Lääne-Virumaa"],
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#6684A4",
            yAxis: 0,
          },
          {
            name: "Põlvamaa",
            data: data.newCountyByDay.Põlvamaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Pärnumaa",
            data: data.newCountyByDay.Pärnumaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Raplamaa",
            data: data.newCountyByDay.Raplamaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Saaremaa",
            data: data.newCountyByDay.Saaremaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Tartumaa",
            data: data.newCountyByDay.Tartumaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Valgamaa",
            data: data.newCountyByDay.Valgamaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Viljandimaa",
            data: data.newCountyByDay.Viljandimaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Võrumaa",
            data: data.newCountyByDay.Võrumaa,
            pointStart: Date.parse(data.caseDates[0]), // data.caseDates first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
        ],
      };
    },
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
      this.chartOptions.title.text = this.$t("confirmedNewCasesByCounties");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
    },
  },
};
</script>

<style lang="scss" scoped></style>
