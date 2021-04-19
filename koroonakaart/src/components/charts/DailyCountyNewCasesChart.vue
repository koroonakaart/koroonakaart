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
import data from "../../data.json";

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
      chartType: "absolute",
      chartOptions: {
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
              text: "Embed Graph",
            },
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
                "embed",
              ],
            },
          },
        },

        // Remove Highcharts.com link from bottom right
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
            day: "%Y<br/>%m-%d",
            week: "%Y<br/>%m-%d",
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
          headerFormat:
            '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b> ({point.percentage:.0f}%)</td></tr>',
          split: false,
          useHTML: true,
        },

        rangeSelector: {
            selected: 0
        },

        series: [
          {
            name: "Harjumaa",
            data: data.countyByDay.newCountyByDay.Harjumaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#2F7ED8",
            yAxis: 0,
          },
          {
            name: "Hiiumaa",
            data: data.countyByDay.newCountyByDay.Hiiumaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#456990",
            yAxis: 0,
          },
          {
            name: "Ida-Virumaa",
            data: data.countyByDay.newCountyByDay["Ida-Virumaa"],
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#49BEAA",
            yAxis: 0,
          },
          {
            name: "Jõgevamaa",
            data: data.countyByDay.newCountyByDay.Jõgevamaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#49DCB1",
            yAxis: 0,
          },
          {
            name: "Järvamaa",
            data: data.countyByDay.newCountyByDay.Järvamaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#EEB868",
            yAxis: 0,
          },
          {
            name: "Läänemaa",
            data: data.countyByDay.newCountyByDay.Läänemaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Lääne-Virumaa",
            data: data.countyByDay.newCountyByDay["Lääne-Virumaa"],
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            color: "#6684A4",
            yAxis: 0,
          },
          {
            name: "Põlvamaa",
            data: data.countyByDay.newCountyByDay.Põlvamaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Pärnumaa",
            data: data.countyByDay.newCountyByDay.Pärnumaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Raplamaa",
            data: data.countyByDay.newCountyByDay.Raplamaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Saaremaa",
            data: data.countyByDay.newCountyByDay.Saaremaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Tartumaa",
            data: data.countyByDay.newCountyByDay.Tartumaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Valgamaa",
            data: data.countyByDay.newCountyByDay.Valgamaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Viljandimaa",
            data: data.countyByDay.newCountyByDay.Viljandimaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
          {
            name: "Võrumaa",
            data: data.countyByDay.newCountyByDay.Võrumaa,
            pointStart: Date.parse(data.dates2[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            yAxis: 0,
          },
        ],
      },
    };
  },

  // Get current locale
  computed: {
    currentLocale: function() {
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
