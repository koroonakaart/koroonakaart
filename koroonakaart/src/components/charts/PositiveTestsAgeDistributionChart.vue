<template>
  <b-container>
    <highcharts class="chart" :options="chartOptions"></highcharts>
  </b-container>
</template>

<script>
export default {
  name: "PositiveTestsAgeDistributionChart",

  data() {
    return {
      chartOptions: {
        title: {
          text: this.$t("distributionOfPositiveTests")
        },

        chart: {
          type: "column",
          height: 470
        },

        // Remove Highcharts.com link from bottom right
        credits: {
          enabled: false
        },

        xAxis: {
          title: {
            text: this.$t("age")
          },
          categories: [
            "0 - 4",
            "5 - 9",
            "10 - 14",
            "15 - 19",
            "20 - 24",
            "25 - 29",
            "30 - 34",
            "35 - 39",
            "40 - 44",
            "45 - 49",
            "50 - 54",
            "55 - 59",
            "60 - 64",
            "65+",
            this.$t("unknown")
          ]
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases")
          }
        },

        series: [
          {
            name: this.$t("numberOfCases"),
            data: [2,1,9,6,10,13,32,41,33,40,40,20,16,19,1]
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
      this.chartOptions.title.text = this.$t("distributionOfPositiveTests");
      this.chartOptions.xAxis.title.text = this.$t("age");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("numberOfCases");
      this.chartOptions.xAxis.categories[
        this.chartOptions.xAxis.categories.length - 1
      ] = this.$t("unknown");
    }
  }
};
</script>

<style lang="scss" scoped>
</style>
