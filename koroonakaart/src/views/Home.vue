//Landing page of the app
<template>
  <b-container fluid="lg">
    <EmbedModal />
    <Statsbar />
    <SuveChatbot />

    <b-row class="mb-5">
      <Map :height="470" />
    </b-row>

    <b-row class="mb-5">
      <b-col cols="12" lg="6">
        <ConfirmedCasesByCountiesChart :height="470" />
      </b-col>
      <b-col cols="12" lg="6">
        <TestsPopRatioChart :height="470" />
      </b-col>
    </b-row>

    <b-row class="mb-5">
      <CumulativeCasesChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <NewCasesPerDayChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <DailyCountyCasesChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <CumulativeTestsChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <TestsPerDayChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <TestsAgeSexDistributionChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <PositiveNegativeChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <GenderChart :height="470" />
    </b-row>
  </b-container>
</template>

<script>
import EmbedModal from "../components/EmbedModal";
import Statsbar from "../components/Statsbar";

import Map from "../components/Map";
import CumulativeTestsChart from "../components/charts/CumulativeTestsChart";
import CumulativeCasesChart from "../components/charts/CumulativeCasesChart";
import NewCasesPerDayChart from "../components/charts/NewCasesPerDayChart";
import TestsPerDayChart from "../components/charts/TestsPerDayChart";
import GenderChart from "../components/charts/GenderChart";

//import PositiveTestsAgeDistributionChart from "../components/charts/PositiveTestsAgeDistributionChart";
import DailyCountyCasesChart from "../components/charts/DailyCountyCasesChart";
import TestsAgeSexDistributionChart from "../components/charts/TestsAgeSexDistributionChart";
import ConfirmedCasesByCountiesChart from "../components/charts/ConfirmedCasesByCountiesChart";
import PositiveNegativeChart from "../components/charts/PositiveNegativeChart";
import TestsPopRatioChart from "../components/charts/TestsPopRatioChart";

export default {
  name: "Home",
  //Register components you want to use in the page here
  components: {
    EmbedModal,
    Statsbar,
    Map,
    CumulativeTestsChart,
    CumulativeCasesChart,
    NewCasesPerDayChart,
    TestsPerDayChart,
    TestsAgeSexDistributionChart,
    //  PositiveTestsAgeDistributionChart,
    GenderChart,
    DailyCountyCasesChart,
    ConfirmedCasesByCountiesChart,
    PositiveNegativeChart,
    TestsPopRatioChart,
    SuveChatbot: () => import("../components/SuveChatbot")
  }
};
</script>

<style lang="scss" scoped></style>
