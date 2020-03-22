<template>
  <b-container id="statsbar-container" class="mb-5" fluid>
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("confirmedCases") }}</h5>
        </div>
        <h1>{{confirmedCasesNumber}}</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("activeCases") }}</h5>
        </div>
        <h1>{{activeCasesNumber}}</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("hospitalised") }}</h5>
        </div>
        <h1>{{hospitalisedNumber}}</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("deceased") }}</h5>
        </div>
        <h1>{{deceasedNumber}}</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("recovered") }}</h5>
        </div>
        <h1>{{recoveredNumber}}</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("testsAdministered") }}</h5>
        </div>
        <h1>{{testsAdministeredNumber}}</h1>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import {
  confirmedCasesNumber,
  activeCasesNumber,
  hospitalisedNumber,
  deceasedNumber,
  recoveredNumber,
  testsAdministeredNumber
} from "../dataConstants";

export default {
  name: "Statsbar",
  data() {
    return {
      confirmedCasesNumber,
      activeCasesNumber,
      hospitalisedNumber,
      deceasedNumber,
      recoveredNumber,
      testsAdministeredNumber
    };
  },
  /* updated() {
    console.log(this.$store.state.dataFromGoogleSheets);
  }, */
  computed: {
    // Disabled until later for data importing
    /* confirmedCasesNumber: function() {
      if (this.$store?.state?.dataFromGoogleSheets?.entry) {
        return this.$store?.state?.dataFromGoogleSheets?.entry[1].gsx$_d6ua4
          ?.$t;
      }
      return "";
    } */
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
}

.statsbar-item {
  height: 7em;

  @media only screen and (max-width: 766px) {
    margin-bottom: 1em;
  }
}
</style>
