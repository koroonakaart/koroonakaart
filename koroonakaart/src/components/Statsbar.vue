<template>
  <b-container id="statsbar-container" class="mb-5" fluid>
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("confirmedCases") }}</h5>
        </div>
        <h1>306</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("activeCases") }}</h5>
        </div>
        <h1>304</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("hospitalised") }}</h5>
        </div>
        <h1>14</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("deceased") }}</h5>
        </div>
        <h1>0</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("recovered") }}</h5>
        </div>
        <h1>2</h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("testsAdministered") }}</h5>
        </div>
        <h1>2812</h1>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: "Statsbar",
  /* updated() {
    console.log(this.$store.state.dataFromGoogleSheets);
  }, */
  computed: {
    confirmedCasesNumber: function() {
      if (this.$store?.state?.dataFromGoogleSheets?.entry) {
        return this.$store?.state?.dataFromGoogleSheets?.entry[1].gsx$_d6ua4
          ?.$t;
      }
      return "";
    }
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
