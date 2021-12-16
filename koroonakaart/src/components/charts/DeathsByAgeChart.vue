<template>
  <b-container fluid>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "DeathsByAgeChart",

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
      chartOptions: {
        title: {
          text: this.$t("deceasedTitle"),
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

        yAxis: {
          //          min: 0,
          title: {
            text: this.$t("deceased"),
          },
        },

        legend: {
          enabled: true,
          layout: "horizontal",
          align: "center",
          verticalAlign: "bottom",
          y: 0,
        },

        xAxis: {
          // categories: [this.$t("ages")]
          categories: ["0-50", "50-59", "60-69", "70-79", "80-89", "90+"],
        },

        series: [
          {
            name: this.$t("male"),
            data: [0, 4, 6, 18, 17, 8],
          },
          {
            name: this.$t("female"),
            data: [1, 1, 4, 13, 34, 14],
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
      this.chartOptions.title.text = this.$t("deceasedTitle");
      this.chartOptions.yAxis.title.text = this.$t("deceased");
      this.chartOptions.series[0].name = this.$t("male");
      this.chartOptions.series[1].name = this.$t("female");
    },
  },
};
</script>

<style lang="scss" scoped></style>
