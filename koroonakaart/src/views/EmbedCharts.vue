<template>
  <div>
    <component :is="chartToDisplay" />
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */
export default {
  name: "EmbedCharts",

  components: {
    Map: () => import("../components/Map"),
    CumulativeTestsChart: () =>
      import("../components/charts/CumulativeTestsChart"),
    CumulativeCasesChart: () =>
      import("../components/charts/CumulativeCasesChart"),
    NewCasesPerDayChart: () =>
      import("../components/charts/NewCasesPerDayChart"),
    TestsPerDayChart: () => import("../components/charts/TestsPerDayChart"),
    TestsAgeSexDistributionChart: () =>
      import("../components/charts/TestsAgeSexDistributionChart"),
    DailyCountyCasesChart: () =>
      import("../components/charts/DailyCountyCasesChart"),
    ConfirmedCasesByCountiesChart: () =>
      import("../components/charts/ConfirmedCasesByCountiesChart"),
    PositiveNegativeChart: () =>
      import("../components/charts/PositiveNegativeChart"),
    TestsPopRatioChart: () => import("../components/charts/TestsPopRatioChart")
    //  PositiveTestsAgeDistributionChart:() => import("../components/charts/PositiveTestsAgeDistributionChart.vue"),
  },

  mounted() {
    console.log(this.$route.query);
  },

  data() {
    return {
      chartToDisplay: this.$route.query.chart
    };
  }
};
</script>

<style lang="scss" scoped>
</style>