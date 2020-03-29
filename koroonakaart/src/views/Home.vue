/* Landing page of the app */
<template>
  <b-container fluid="lg">
    <Statsbar />
    <b-row class="mb-5">
      <Map />

      <SuveChatbot />
    </b-row>

    <b-row class="mb-5">
      <b-col
        cols="12"
        lg="6"
      >
        <ConfirmedCasesByCountiesChart />
      </b-col>
      <b-col
        cols="12"
        lg="6"
      >
        <TestsPopRatioChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <b-col
        cols="12"
        lg="6"
      >
        <CumulativeCasesChart />
      </b-col>
      <b-col
        cols="12"
        lg="6"
      >
        <NewCasesPerDayChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <DailyCountyCasesChart />
    </b-row>
    <b-row class="mb-5">
      <b-col
        cols="12"
        lg="6"
      >
        <CumulativeTestsChart />
      </b-col>
      <b-col
        cols="12"
        lg="6"
      >
        <TestsPerDayChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <b-col
        cols="12"
        lg="6"
      >
        <TestsAgeSexDistributionChart />
      </b-col>
      <b-col
        cols="12"
        lg="6"
      >
        <TestsAgeSexRelationalDistributionChart />
      </b-col>
    </b-row>
    <b-row class="mb-5">
      <PositiveNegativeChart />
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
import TestsAgeSexDistributionChart from "../components/charts/TestsAgeSexDistributionChart";
import TestsAgeSexRelationalDistributionChart from "../components/charts/TestsAgeSexRelationalDistributionChart";
import ConfirmedCasesByCountiesChart from "../components/charts/ConfirmedCasesByCountiesChart";
import PositiveNegativeChart from "../components/charts/PositiveNegativeChart";
import TestsPopRatioChart from "../components/charts/TestsPopRatioChart";
import DailyCountyCasesChart from "../components/charts/DailyCountyCasesChart";

import SuveChatbot from "../components/SuveChatbot";

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
    TestsAgeSexDistributionChart,
    TestsAgeSexRelationalDistributionChart,
    ConfirmedCasesByCountiesChart,
    PositiveNegativeChart,
    TestsPopRatioChart,
    DailyCountyCasesChart,
    SuveChatbot
  }
};
</script>

<style lang="scss" scoped>
</style>
