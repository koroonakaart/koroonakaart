<template>
  <b-container fluid>
    <highcharts v-if="chartOptions"
                :constructor-type="'stockChart'"
                class="chart"
                :options="chartOptions">
    </highcharts>
  </b-container>
</template>

<script>
import { formatTooltip } from "../../utilities/formatTooltip";

export default {
  name: "NewCasesPerDayChart",

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
    dataNewCasesPerDayChart () {
      return this.$store.state.data.dataNewCasesPerDayChart;
    },
  },

  methods: {
    getChartOptions() {
      this.chartOptions = {
        title: {
          text: this.$t("newCases"),
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
          //          min: 0,
          title: {
            text: this.$t("numberOfCases"),
          },
        },

        tooltip: {
          formatter: (context) => {
            return formatTooltip(
              context,
              this.chartOptions.series,
              this.currentLocale,
              0,
              true
            );
          },
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          split: false,
          useHTML: true,
          distance: 20,
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
            pointWidth: 10,
            pointPadding: -0.2,
            borderWidth: 0,
          },
        },

        rangeSelector: {
          selected: 1,
        },

        series: [
          {
            name: this.$t("confirmedCases"),
            color: "#7cb5ec",
            pointStart: Date.parse(this.caseDates[0]), // data.dates2 first entry to UTC
            pointInterval: 24 * 3600 * 1000, // one day
            data: this.dataNewCasesPerDayChart.confirmedCases,
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
      this.chartOptions.title.text = this.$t("newCases");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("confirmedCases");
    },
  },
};
</script>

<style lang="scss" scoped></style>
