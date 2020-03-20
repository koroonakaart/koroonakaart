/* Landing page of the app */
<template>
  <b-container fluid="lg">
    <Statsbar />
    <b-row class="mb-5">
      <b-col cols="12" lg="7">
        <Map />
      </b-col>
      <b-col cols="12" lg="5">
        <ConfirmedCasesByCountiesChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <b-col cols="12" lg="6">
        <CumulativeCasesChart />
      </b-col>
      <b-col cols="12" lg="6">
        <NewCasesPerDayChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <b-col cols="12" lg="6">
        <CumulativeTestsChart />
      </b-col>
      <b-col cols="12" lg="6">
        <TestsPerDayChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <b-col>
        <PositiveTestsAgeDistributionChart />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Statsbar from "../components/Statsbar";
import Map from "../components/Map";
import CumulativeTestsChart from "../components/charts/CumulativeTestsChart";
import CumulativeCasesChart from "../components/charts/CumulativeCasesChart";
import NewCasesPerDayChart from "../components/charts/NewCasesPerDayChart";
import TestsPerDayChart from "../components/charts/TestsPerDayChart";
import PositiveTestsAgeDistributionChart from "../components/charts/PositiveTestsAgeDistributionChart";
import ConfirmedCasesByCountiesChart from "../components/charts/ConfirmedCasesByCountiesChart";

export default {
  name: "Home",
  // Register components you want to use in the page here
  components: {
    Statsbar,
    Map,
    CumulativeTestsChart,
    CumulativeCasesChart,
    NewCasesPerDayChart,
    TestsPerDayChart,
    PositiveTestsAgeDistributionChart,
    ConfirmedCasesByCountiesChart
  }
};
</script>

<style lang="scss" scoped>
</style>
