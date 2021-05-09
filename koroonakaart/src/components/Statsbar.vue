<template>
  <b-container id="statsbar-container" class="mb-5" fluid>
    <b-row
      ><small style="margin-bottom: 20px">{{ $t("faq.a5") }}</small></b-row
    >
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("confirmedCases") }}</strong>
        </div>
        <h1>{{ confirmedCasesNumber | formatNumber(currentLocale) }}</h1>
        <strong
          :class="
            rawConfirmedChanged === 0
              ? 'neutral'
              : rawConfirmedChanged > 0
              ? 'positive'
              : 'positive'
          "
        >
          {{ confirmedChanged | formatNumber(currentLocale) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("activeCases") }}</strong>
        </div>
        <h1>{{ activeCasesNumber | formatNumber(currentLocale) }}</h1>
        <strong
          :class="
            rawActiveChanged === 0
              ? 'neutral'
              : rawActiveChanged > 0
              ? 'positive'
              : 'negative'
          "
        >
          {{ activeChanged }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("perHundred") }}</strong>
        </div>
        <h1>{{ perHundred | formatNumber(currentLocale, 1) }}</h1>
        <strong
          :class="
            rawPerHundredChanged === 0
              ? 'neutral'
              : rawPerHundredChanged > 0
              ? 'positive'
              : 'negative'
          "
        >
          {{ rawPerHundredChanged | formatNumber(currentLocale, 1) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("testsAdministered") }}</strong>
        </div>
        <h1>{{ testsAdministeredNumber | formatNumber(currentLocale) }}</h1>
        <strong
          :class="
            rawTestsChanged === 0
              ? 'neutral'
              : rawTestsChanged > 0
              ? 'negative'
              : 'positive'
          "
        >
          {{ testsChanged | formatNumber(currentLocale) }}
        </strong>
      </b-col>
    </b-row>
    <br />
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("hospitalized") }}</strong>
        </div>
        <h1>{{ hospitalizedNumber | formatNumber(currentLocale) }}</h1>
        <strong
          :class="
            rawHospitalizedChanged === 0
              ? 'neutral'
              : rawHospitalizedChanged > 0
              ? 'positive'
              : 'negative'
          "
        >
          {{ hospitalizedChanged | formatNumber(currentLocale) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("recovered") }}</strong>
        </div>
        <h1>{{ recoveredNumber | formatNumber(currentLocale) }}</h1>
        <strong
          :class="
            rawRecoveredChanged === 0
              ? 'neutral'
              : rawRecoveredChanged > 0
              ? 'negative'
              : 'positive'
          "
        >
          {{ recoveredChanged | formatNumber(currentLocale) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("deceased") }}</strong>
        </div>
        <h1>{{ deceasedNumber | formatNumber(currentLocale) }}</h1>
        <strong
          :class="
            rawDeceasedChanged === 0
              ? 'neutral'
              : rawDeceasedChanged > 0
              ? 'positive'
              : 'negative'
          "
        >
          {{ deceasedChanged | formatNumber(currentLocale) }}
        </strong>
      </b-col>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("pos14avg") }}</strong>
        </div>
        <h1>
          {{ positiveTestAverage14Percent | formatNumber(currentLocale, 1) }}%
        </h1>
      </b-col>
    </b-row>
    <br />
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("allVaccinated") }}</strong>
        </div>
        <h1>{{ allVaccinationNumberTotal | formatNumber(currentLocale) }}</h1>
        <strong class="negative">
          {{ allVaccinationNumberLastDay | formatNumber(currentLocale) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("allVaccinatedPercentage") }}</strong>
        </div>
        <h1>
          {{
            allVaccinationFromPopulationPercentage
              | formatNumber(currentLocale, 1)
          }}%
        </h1>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("vaccinationNumber") }}</strong>
        </div>
        <h1>{{ vaccinationNumberTotal | formatNumber(currentLocale) }}</h1>
        <strong class="negative">
          {{ vaccinationNumberLastDay | formatNumber(currentLocale) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{ $t("completedVaccinationNumber") }}</strong>
        </div>
        <h1>
          {{ completedVaccinationNumberTotal | formatNumber(currentLocale) }}
        </h1>
        <strong class="negative">
          {{ completedVaccinationNumberLastDay | formatNumber(currentLocale) }}
        </strong>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <strong>{{
            $t("completelyVaccinatedFromTotalVaccinatedPercentage")
          }}</strong>
        </div>
        <h1>
          {{
            completelyVaccinatedFromTotalVaccinatedPercentage
              | formatNumber(currentLocale, 1)
          }}%
        </h1>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import data from "../data/StatsBar.json";
import { positiveSign } from "../utilities/helper";
import { formatNumberByLocale } from "../utilities/formatNumberByLocale";
export default {
  name: "Statsbar",

  data() {
    return Object.freeze({
      activeCasesNumber: data.activeCasesNumber,
      activeChanged: positiveSign(data.activeChanged),
      allVaccinationFromPopulationPercentage:
        data.allVaccinationFromPopulationPercentage,
      allVaccinationNumberLastDay: positiveSign(
        data.allVaccinationNumberLastDay
      ),
      allVaccinationNumberTotal: data.allVaccinationNumberTotal,
      completedVaccinationNumberLastDay: positiveSign(
        data.completedVaccinationNumberLastDay
      ),
      completedVaccinationNumberTotal: data.completedVaccinationNumberTotal,
      completelyVaccinatedFromTotalVaccinatedPercentage:
        data.completelyVaccinatedFromTotalVaccinatedPercentage,
      confirmedCasesNumber: data.confirmedCasesNumber,
      confirmedChanged: positiveSign(data.confirmedChanged),
      deceasedChanged: positiveSign(data.deceasedChanged),
      deceasedNumber: data.deceasedNumber,
      hospitalizedChanged: positiveSign(data.hospitalizedChanged),
      hospitalizedNumber: data.hospitalizedNumber,
      perHundred: data.perHundred,
      positiveTestAverage14Percent: data.positiveTestAverage14Percent,
      rawActiveChanged: data.rawActiveChanged,
      rawConfirmedChanged: data.rawConfirmedChanged,
      rawDeceasedChanged: Number(data.deceasedChanged),
      rawHospitalizedChanged: Number(data.hospitalizedChanged),
      rawPerHundredChanged: positiveSign(data.rawPerHundredChanged.toFixed(2)),
      rawRecoveredChanged: Number(data.recoveredChanged),
      rawTestsChanged: Number(data.testsChanged),
      recoveredChanged: positiveSign(data.recoveredChanged),
      recoveredNumber: data.recoveredNumber,
      testsAdministeredNumber: data.testsAdministeredNumber,
      testsChanged: positiveSign(data.testsChanged),
      vaccinationNumberLastDay: positiveSign(data.vaccinationNumberLastDay),
      vaccinationNumberTotal: data.vaccinationNumberTotal,
    });
  },

  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
  },

  filters: {
    formatNumber: function (number, currentLocale, precision) {
      let result = "";

      if (typeof number === "string" && number.startsWith("+")) {
        const actualNumber = number.split("+")[1];
        result =
          "+" + formatNumberByLocale(actualNumber, currentLocale, precision);
      } else {
        result = formatNumberByLocale(number, currentLocale, precision);
      }

      return result.replace(/\s/g, "\u202F");
    },
  },
};
</script>

<style lang="scss" scoped>
strong {
  font-size: 18px;
  font-weight: 500;
  margin-top: 0;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

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
  margin-bottom: -0.4em;
}

.positive {
  color: red;
}

.negative {
  color: green;
}

.neutral {
  color: rgb(97, 97, 97);
}

.statsbar-item {
  //  height: 7em;

  @media only screen and (max-width: 766px) {
    margin-bottom: 1em;
  }
}
</style>
