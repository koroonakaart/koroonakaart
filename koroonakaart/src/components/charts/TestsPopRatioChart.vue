<template>
  <b-container fluid>
    <div v-if="loading" class="loading">
      {{ $t("loading") }}
    </div>

    <highcharts
      v-if="!loading"
      class="chart"
      :options="chartOptions"
    ></highcharts>
  </b-container>
</template>

<script>
import { formatTooltip } from "../../utilities/formatTooltip";
import { formatNumberByLocale } from "../../utilities/formatNumberByLocale";

export default {
  name: "TestsPopRatioChart",

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
      loading: true,
      chartOptions: null,
    };
  },

  created() {
    this.fetchData();
  },

  // Get current locale
  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
  },

  methods: {
    fetchData() {
      let _this = this;
      import("../../data/TestsPopRatio.json").then((data) => {
        _this.chartOptions = _this.makeData(data);
        _this.loading = false;
      });
    },

    makeData(data) {
      var context = this;
      return {
        title: {
          text: this.$t("testsPer10000"),
          align: "left",
          y: 5,
        },

        navigation: {
          buttonOptions: {
            verticalAlign: "top",
            y: -15,
          },
        },

        chart: {
          type: "bar",
          height: this.height,
          width: this.width,
          marginTop: 40,
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

          chartOptions: {
            // Specific options for the exported image
            plotOptions: {
              series: {
                dataLabels: {
                  enabled: true,
                },
              },
            },
          },
          fallbackToExportServer: false,
        },

        tooltip: {
          formatter: (context) => {
            return formatTooltip(
              context,
              this.chartOptions.series,
              this.currentLocale,
              1,
              false
            );
          },
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true,
          valueDecimals: 1,
        },

        // Show Highcharts.com link at bottom right
        credits: {
          enabled: true,
        },

        xAxis: {
          labels: {
            style: {
              fontSize: "13px",
              fontWeight: "bold",
            },
          },
          categories: [
            "Harjumaa",
            "Hiiumaa",
            "Ida-Virumaa",
            "Jõgevamaa",
            "Järvamaa",
            "Läänemaa",
            "Lääne-Virumaa",
            "Põlvamaa",
            "Pärnumaa",
            "Raplamaa",
            "Saaremaa",
            "Tartumaa",
            "Valgamaa",
            "Viljandimaa",
            "Võrumaa",
          ],
        },

        yAxis: {
          title: {
            text: this.$t("testsPer10000Axis"),
          },
        },

        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true,
              formatter: function () {
                return formatNumberByLocale(this.y, context.currentLocale, 1);
                // return Highcharts.numberFormat(this.y, 1);
              },
            },
            enableMouseTracking: true,
          },
        },

        series: [
          {
            name: this.$t("numberOfCases"),
            data: data.dataTestsPopRatio,
          },
        ],

        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 350,
              },

              chartOptions: {
                chart: { marginTop: 60 },
              },
            },
          ],
        },
      };
    },
  },

  // Fire when currentLocale computed property changes
  watch: {
    currentLocale() {
      this.chartOptions.title.text = this.$t("testsPer10000");
      this.chartOptions.yAxis.title.text = this.$t("testsPer10000Axis");
      this.chartOptions.series[0].name = this.$t("numberOfCases");
      //  this.chartOptions.xAxis.categories[0] = this.$t("insufficientData");
    },
  },
};
</script>

<style lang="scss" scoped></style>
