/* Landing page of the app */
<template>
  <b-container fluid="lg">
    <Statsbar />
    <SuveChatbot />

    <!--<b-row class="mb-5">
      <Map />
    </b-row>

    <b-row class="mb-5">
      <b-col cols="12" lg="6">
        <ConfirmedCasesByCountiesChart />
      </b-col>
      <b-col cols="12" lg="6">
        <TestsPopRatioChart />
      </b-col>
    </b-row>-->
     <b-row class="mb-5">
      <CumulativeCasesChart />
    </b-row>
 <b-row class="mb-5">
      <NewCasesPerDayChart />
    </b-row>
    <!--   <b-row class="mb-5">
      <DailyCountyCasesChart />
    </b-row>-->
    <b-row class="mb-5">
      <CumulativeTestsChart />
    </b-row>
    <b-row class="mb-5">
      <TestsPerDayChart />
    </b-row>
  <!-- <b-row class="mb-5">
      <b-col cols="12" lg="12">
        <PositiveTestsAgeDistributionChart />
    </b-col>-->
    <!--<b-col cols="12" lg="6">
        <PositiveNegativeChart />
    </b-col>-->
    <!-- </b-row> -->
  </b-container>
</template>

<script>
import Statsbar from "../components/Statsbar";

/*import Map from "../components/Map";
import CumulativeTestsChart from "../components/charts/CumulativeTestsChart";
import CumulativeCasesChart from "../components/charts/CumulativeCasesChart";
import NewCasesPerDayChart from "../components/charts/NewCasesPerDayChart";
import TestsPerDayChart from "../components/charts/TestsPerDayChart";

import PositiveTestsAgeDistributionChart from "../components/charts/PositiveTestsAgeDistributionChart";
import DailyCountyCasesChart from "../components/charts/DailyCountyCasesChart";
// import TestsAgeSexDistributionChart from "../components/charts/TestsAgeSexDistributionChart";
import ConfirmedCasesByCountiesChart from "../components/charts/ConfirmedCasesByCountiesChart";
// import PositiveNegativeChart from "../components/charts/PositiveNegativeChart";
import TestsPopRatioChart from "../components/charts/TestsPopRatioChart";*/

export default {
  name: "Home",
  // Register components you want to use in the page here
  components: {
    Statsbar,

  /*   Map,
  CumulativeTestsChart,
  CumulativeCasesChart,
  NewCasesPerDayChart,
  TestsPerDayChart,

    PositiveTestsAgeDistributionChart,
    DailyCountyCasesChart,
    ConfirmedCasesByCountiesChart,
    // PositiveNegativeChart,
    TestsPopRatioChart,*/
    SuveChatbot: () => import("../components/SuveChatbot")
  }
};
</script>

<style lang="scss" scoped>
</style>
