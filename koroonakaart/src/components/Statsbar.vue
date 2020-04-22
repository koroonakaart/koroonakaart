<template>
  <b-container id="statsbar-container" class="mb-5" fluid>
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("confirmedCases") }}</h5>
        </div>
        <h1>{{confirmedCasesNumber}}</h1>
        <h5>( {{confirmedChanged}} )</h5>
      </b-col>

      <!--<b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("activeCases") }}</h5>
        </div>
        <h1>{{activeCasesNumber}}</h1>
      </b-col>-->

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("hospitalised") }}</h5>
        </div>
        <h1>{{hospitalisedNumber}}</h1>
        <h5>( {{hospitalisedChanged}} )</h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("deceased") }}</h5>
        </div>
        <h1>{{deceasedNumber}}</h1>
        <h5>( {{deceasedChanged}} )</h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("recovered") }}</h5>
        </div>
        <h1>{{recoveredNumber}}</h1>
        <h5>( {{recoveredChanged}} )</h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("testsAdministered") }}</h5>
        </div>
        <h1>{{testsAdministeredNumber}}</h1>
        <h5>( {{testsChanged}} )</h5>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import data from "../data.json";
import {positiveSign} from "../utilities/helper"
export default {
  name: "Statsbar",
  data() {
    return {
      confirmedCasesNumber: data.confirmedCasesNumber,
      activeCasesNumber: data.activeCasesNumber,
      hospitalisedNumber: data.hospitalisedNumber,
      deceasedNumber: data.deceasedNumber,
      recoveredNumber: data.recoveredNumber,
      testsAdministeredNumber: data.testsAdministeredNumber,
      hospitalisedChanged: positiveSign(data.hospitalChanged),
      recoveredChanged: positiveSign(data.recoveredChanged),
      deceasedChanged: positiveSign(data.deceasedChanged),
      confirmedChanged: positiveSign(data.dataNewCasesPerDayChart.confirmedCases[data.dataNewCasesPerDayChart.confirmedCases.length -1]),
      testsChanged: positiveSign(data.dataCumulativeTestsChart.testsAdminstered[data.dataCumulativeTestsChart.testsAdminstered.length -1] - data.dataCumulativeTestsChart.testsAdminstered[data.dataCumulativeTestsChart.testsAdminstered.length -2])

    };
  }
};
</script>

<style lang="scss" scoped>
#statsbar-container {
  @media only screen and (max-width: 766px) {
    margin-bottom: 0;
  }
}

.statsbar-heading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 4em;
  margin-bottom: -.5em;
}

.statsbar-item {
//  height: 7em;

  @media only screen and (max-width: 766px) {
    margin-bottom: 1em;
  }
}
</style>
