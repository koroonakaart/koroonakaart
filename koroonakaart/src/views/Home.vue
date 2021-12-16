// Landing page of the app
<template>
  <b-container fluid="lg">
    <Statsbar />

    <b-row class="mb-5">
      <Map :height="470" />
    </b-row>

    <b-row class="mb-5">
      <b-col cols="12" lg="6">
        <ConfirmedCasesByCountyChart :height="470" />
      </b-col>
      <b-col cols="12" lg="6">
        <TestsPopRatioChart :height="470" />
      </b-col>
    </b-row>

    <b-row class="mb-5">
      <NewCasesChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <CumulativeCasesPer100kChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <CumulativeCasesChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <DailyCountyCasesChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <DailyCountyNewCasesChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <TestsAdministeredChart :height="470" />
    </b-row>
    <b-row class="mb-5">
      <CumulativeTestsChart :height="470" />
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
    <b-row class="mb-5">
      <VaccinatedPeopleChart :height="470" />
    </b-row>
  </b-container>
</template>

<script>
import Statsbar from "../components/Statsbar";

import Map from "../components/Map";
import CumulativeTestsChart from "../components/charts/CumulativeTestsChart";
import CumulativeCasesChart from "../components/charts/CumulativeCasesChart";
import CumulativeCasesPer100kChart from "../components/charts/CumulativeCasesPer100kChart";
import NewCasesChart from "../components/charts/NewCasesChart";
import TestsAdministeredChart from "../components/charts/TestsAdministeredChart";
import GenderChart from "../components/charts/GenderChart";
import VaccinatedPeopleChart from "../components/charts/VaccinatedPeopleChart";
import DailyCountyCasesChart from "../components/charts/DailyCountyCasesChart";
import DailyCountyNewCasesChart from "../components/charts/DailyCountyNewCasesChart";
import TestsAgeSexDistributionChart from "../components/charts/TestsAgeSexDistributionChart";
import ConfirmedCasesByCountyChart from "../components/charts/ConfirmedCasesByCountyChart";
import PositiveNegativeChart from "../components/charts/PositiveNegativeChart";
import TestsPopRatioChart from "../components/charts/TestsPopRatioChart";

export default {
  name: "Home",
  //Register components you want to use in the page here
  components: {
    Statsbar,
    Map,
    CumulativeTestsChart,
    CumulativeCasesChart,
    CumulativeCasesPer100kChart,
    NewCasesChart,
    TestsAdministeredChart,
    TestsAgeSexDistributionChart,
    GenderChart,
    VaccinatedPeopleChart,
    DailyCountyCasesChart,
    DailyCountyNewCasesChart,
    ConfirmedCasesByCountyChart,
    PositiveNegativeChart,
    TestsPopRatioChart,
  },
};
</script>

<style lang="scss" scoped></style>
