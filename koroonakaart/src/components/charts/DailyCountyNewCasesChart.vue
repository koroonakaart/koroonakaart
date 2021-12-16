<template>
  <b-container fluid>
    <highcharts v-if="chartOptions"
                :constructor-type="'stockChart'"
                class="chart"
                :options="chartOptions"
                ref="thisChart">
    </highcharts>
  </b-container>
</template>

<script>
import { formatDate, capitalise } from "../../utilities/helper";
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

  data() {
    return {
      chartOptions: null
    };
  },

  // Get current locale
  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
    loaded () {
      return this.$store.state.loaded;
    },
    caseDates () {
      return this.$store.getters.caseDates;
    },
    countyByDay () {
      return this.$store.state.data.countyByDay;
    }
  },

  methods: {
    getChartOptions() {
      this.chartOptions = {
        title: {
          text: this.$t("confirmedNewCasesByCounty"),
          align: "left",
          y: 5,
        },

        chart: {
          type: "column",
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
            var tooltipDate = capitalise(formatDate(x, this.currentLocale, dateOptions));

            // Compose tooltip
            var tooltip = tooltipDate + "<br>";
            tooltip += "<table>";
            tooltip += "<tr>";
            tooltip += '<td><span style="color: ' + color + '">●</span> ' + countyName + "&nbsp;&nbsp;</td>";
            tooltip += '<td style="text-align: right"><b>' + formatNumberByLocale(value, this.currentLocale) + "</b></td>";
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
            data: this.countyByDay.newCountyByDay.Harjumaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#2F7ED8",
            yAxis: 0,
          },
          {
            name: "Hiiumaa",
            data: this.countyByDay.newCountyByDay.Hiiumaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#456990",
            yAxis: 0,
          },
          {
            name: "Ida-Virumaa",
            data: this.countyByDay.newCountyByDay["Ida-Virumaa"],
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#49BEAA",
            yAxis: 0,
          },
          {
            name: "Jõgevamaa",
            data: this.countyByDay.newCountyByDay.Jõgevamaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#49DCB1",
            yAxis: 0,
          },
          {
            name: "Järvamaa",
            data: this.countyByDay.newCountyByDay.Järvamaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#EEB868",
            yAxis: 0,
          },
          {
            name: "Läänemaa",
            data: this.countyByDay.newCountyByDay.Läänemaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#7CB5EC",
            yAxis: 0,
          },
          {
            name: "Lääne-Virumaa",
            data: this.countyByDay.newCountyByDay["Lääne-Virumaa"],
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#6684A4",
            yAxis: 0,
          },
          {
            name: "Põlvamaa",
            data: this.countyByDay.newCountyByDay.Põlvamaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Pärnumaa",
            data: this.countyByDay.newCountyByDay.Pärnumaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Raplamaa",
            data: this.countyByDay.newCountyByDay.Raplamaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Saaremaa",
            data: this.countyByDay.newCountyByDay.Saaremaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Tartumaa",
            data: this.countyByDay.newCountyByDay.Tartumaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Valgamaa",
            data: this.countyByDay.newCountyByDay.Valgamaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Viljandimaa",
            data: this.countyByDay.newCountyByDay.Viljandimaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Võrumaa",
            data: this.countyByDay.newCountyByDay.Võrumaa,
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
        ],
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
      this.chartOptions.title.text = this.$t("confirmedNewCasesByCounty");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
    },
  },
};
</script>

<style lang="scss" scoped></style>
