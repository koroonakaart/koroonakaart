// "Cases by county" chart
<template>
  <intersect @enter="visible = true">
    <b-container fluid>
      <Loading v-if="!loaded" />
      <highcharts
        v-if="loaded"
        class="chart"
        :options="chartOptions"
      ></highcharts>
    </b-container>
  </intersect>
</template>

<script>
import Intersect from "vue-intersect";
import Loading from "../Loading";

export default {
  name: "ConfirmedCasesByCountiesChart",

  components: { Intersect, Loading },

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
      visible: false,
      loaded: false,
      loading: false,
      chartOptions: null,
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
    visible() {
      if (this.visible) {
        this.fetchData();
      }
    },
    currentLocale() {
      this.chartOptions.title.text = this.$t("confirmedCasesByCounties");
      this.chartOptions.yAxis.title.text = this.$t("numberOfCases");
      this.chartOptions.series[0].name = this.$t("numberOfCases");
      this.chartOptions.series[1].name = this.$t("newPositive");
      this.chartOptions.xAxis.categories[15] = this.$t("insufficientData");
    },
  },

  methods: {
    fetchData() {
      let _this = this;
      if (_this.loaded || _this.loading) {
        return;
      }
      _this.loading = true;
      import("../../data/ConfirmedCasesByCounties.json").then((data) => {
        _this.loading = false;
        _this.chartOptions = Object.freeze(_this.makeData(data));
        _this.loaded = true;
      });
    },

    makeData(data) {
      return {
        title: {
          text: this.$t("confirmedCasesByCounties"),
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
            // specific options for the exported image
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
          headerFormat: "<span>{point.key}</span><table>",
          pointFormat:
            '<tr><td><span style="color:{series.color}">●</span> {series.name}&nbsp;&nbsp;</td>' +
            '<td style="padding:0; text-align: right"><b>{point.y}</b></tr>',
          footerFormat: "</table>",
          backgroundColor: "#ffffff",
          style: {
            opacity: 0.95,
          },
          shared: true,
          useHTML: true,
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
            this.$t("insufficientData"),
          ],
        },

        yAxis: {
          title: {
            text: this.$t("numberOfCases"),
          },
        },

        plotOptions: {
          bar: {
            //            dataLabels: {
            //              enabled: true
            //            },
            enableMouseTracking: true,
          },
        },

        series: [
          {
            dataLabels: {
              enabled: true,
            },
            name: this.$t("numberOfCases"),
            data: data.dataConfirmedCasesByCounties,
          },
          {
            name: this.$t("newPositive"),
            data: data.countyByDay.countyByDayNew,
          },
        ],
      };
    },
  },
};
</script>

<style lang="scss" scoped></style>
