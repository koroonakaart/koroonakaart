<template>
  <component
    :is="this.$route.query.chart"
    :height="this.$route.query.height"
    :width="this.$route.query.width"
  />
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
    CumulativeCasesPer100kChart: () =>
      import("../components/charts/CumulativeCasesPer100kChart"),
    NewCasesPerDayChart: () =>
      import("../components/charts/NewCasesPerDayChart"),
    TestsPerDayChart: () => import("../components/charts/TestsPerDayChart"),
    TestsAgeSexDistributionChart: () =>
      import("../components/charts/TestsAgeSexDistributionChart"),
    DailyCountyCasesChart: () =>
      import("../components/charts/DailyCountyCasesChart"),
    DailyCountyNewCasesChart: () =>
      import("../components/charts/DailyCountyNewCasesChart"),
    ConfirmedCasesByCountiesChart: () =>
      import("../components/charts/ConfirmedCasesByCountiesChart"),
    PositiveNegativeChart: () =>
      import("../components/charts/PositiveNegativeChart"),
    TestsPopRatioChart: () => import("../components/charts/TestsPopRatioChart"),
    //  PositiveTestsAgeDistributionChart:() => import("../components/charts/PositiveTestsAgeDistributionChart.vue"),
    GenderChart: () => import("../components/charts/GenderChart"),
    VaccinatedPeopleChart: () =>
      import("../components/charts/VaccinatedPeopleChart"),
  },

  mounted() {
    console.log(this.$route.query);
    /* this.classList.remove("container"); */
  },
};
</script>

<style lang="scss" scoped>
#embed-container {
  width: 100vh;
}
</style>
