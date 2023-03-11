<template>
  <b-container id="statsbar-container" class="mb-5" fluid v-if="loaded">
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("confirmedCases") }}</h5>
        </div>
        <h1>{{ confirmedCasesNumber | formatNumber(currentLocale) }}</h1>
        <h5 :class="
            rawConfirmedChanged === 0
              ? 'neutral'
              : rawConfirmedChanged > 0
              ? 'positive'
              : 'positive'">
          {{ confirmedChanged | formatNumber(currentLocale) }}
        </h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("activeCases") }}</h5>
        </div>
        <h1>{{ activeCasesNumber | formatNumber(currentLocale) }}</h1>
        <h5 :class="
            rawActiveChanged === 0
              ? 'neutral'
              : rawActiveChanged > 0
              ? 'positive'
              : 'negative'">
          {{ activeChanged }}
        </h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("perHundred") }}</h5>
        </div>
        <h1>{{ perHundred | formatNumber(currentLocale, 1) }}</h1>
        <h5 :class="
            rawPerHundredChanged === 0
              ? 'neutral'
              : rawPerHundredChanged > 0
              ? 'positive'
              : 'negative'">
          {{ rawPerHundredChanged | formatNumber(currentLocale, 1) }}
        </h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("testsAdministered") }}</h5>
        </div>
        <h1>{{ testsAdministeredNumber | formatNumber(currentLocale) }}</h1>
        <h5 :class="
            rawTestsChanged === 0
              ? 'neutral'
              : rawTestsChanged > 0
              ? 'negative'
              : 'positive'">
          {{ testsChanged | formatNumber(currentLocale) }}
        </h5>
      </b-col>
    </b-row>
    <br>
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("hospitalised") }}</h5>
        </div>
        <h1>{{ hospitalisedNumber | formatNumber(currentLocale) }}</h1>
        <h5 :class="
            rawHospitalisedChanged === 0
              ? 'neutral'
              : rawHospitalisedChanged > 0
              ? 'positive'
              : 'negative'">
          {{ hospitalisedChanged | formatNumber(currentLocale) }}
        </h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("onventilation") }}</h5>
        </div>
        <h1>{{ onVentilationNumber | formatNumber(currentLocale) }}</h1>
        <h5 :class="
            rawOnVentilationChanged === 0
              ? 'neutral'
              : rawOnVentilationChanged > 0
              ? 'positive'
              : 'negative'">
          {{ onVentilationChanged | formatNumber(currentLocale) }}
        </h5>
      </b-col>

      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("deceased") }}</h5>
        </div>
        <h1>{{ deceasedNumber | formatNumber(currentLocale) }}</h1>
        <h5 :class="
            rawDeceasedChanged === 0
              ? 'neutral'
              : rawDeceasedChanged > 0
              ? 'positive'
              : 'negative'">
          {{ deceasedChanged | formatNumber(currentLocale) }}
        </h5>
      </b-col>
      <b-col class="statsbar-item" md>
        <div class="statsbar-heading">
          <h5>{{ $t("pos14avg") }}</h5>
        </div>
        <h1>{{ positiveTestAverage14Percent | formatNumber(currentLocale, 1) }}%</h1>
      </b-col>
    </b-row>
    <br>
    <b-row class="mb-2">
      <b-col md>
        <h5 class="text-left">{{ $t("vaccination") }}</h5>
      </b-col>
    </b-row>
    <b-row>
      <b-col class="statsbar-item" md>
        <div class="vaccination-progress-label">
          <p class="vaccination-progress-text">{{ $t("atLeastOneDose") }}</p>
          <p class="vaccination-progress-value">{{ vaccinatedAtLeastOneDosePercentage | formatNumber(currentLocale, 1) }}%</p>
        </div>
        <div class="progress">
          <div class="progress-bar"
               :style="{width: vaccinatedAtLeastOneDosePercentage + '%'}">
          </div>
        </div>
      </b-col>
      <b-col class="statsbar-item" md>
        <div class="vaccination-progress-label">
          <p class="vaccination-progress-text">{{ $t("fullyVaccinated") }}</p>
          <p class="vaccination-progress-value">{{ fullyVaccinatedNumberPercentage | formatNumber(currentLocale, 1) }}%</p>
        </div>
        <div class="progress">
          <div class="progress-bar"
               :style="{width: fullyVaccinatedNumberPercentage + '%'}">
          </div>
        </div>
      </b-col>
    </b-row>


  </b-container>
</template>


<script>
import { positiveSign } from "../utilities/helper";
import { formatNumberByLocale } from "../utilities/formatNumberByLocale";
export default {
  name: "Statsbar",

  computed: {
    currentLocale: function () {
      return this.$i18n.locale;
    },
    loaded () {
      return this.$store.state.loaded;
    },
    activeCasesNumber () {
      return this.$store.state.data.activeCasesNumber;
    },
    positiveTestAverage14Percent () {
      return this.$store.state.data.dataTestsPerDayChart.positiveTestAverage14Percent;
    },
    confirmedCasesNumber () {
      return this.$store.state.data.confirmedCasesNumber;
    },
    deceasedNumber () {
      return this.$store.state.data.deceasedNumber;
    },
    perHundred () {
      return this.$store.state.data.dataCumulativeCasesChart.active100k[
        this.$store.state.data.dataCumulativeCasesChart.active100k.length - 1
      ];
    },
    hospitalisedNumber () {
      return this.$store.state.data.hospital.activehospitalizations[
        this.$store.state.data.hospital.activehospitalizations.length - 1
      ];
    },
    onVentilationNumber () {
      return this.$store.state.data.onVentilationNumber;
    },
    testsAdministeredNumber () {
      return this.$store.state.data.testsAdministeredNumber;
    },
    rawActiveChanged () {
      return Number(
        this.$store.state.data.dataCumulativeCasesChart.active[
          this.$store.state.data.dataCumulativeCasesChart.active.length - 1
        ] -
        this.$store.state.data.dataCumulativeCasesChart.active[
          this.$store.state.data.dataCumulativeCasesChart.active.length - 2
        ]
      );
    },
    rawConfirmedChanged () {
      return Number(
        this.$store.state.data.dataNewCasesPerDayChart.confirmedCases[
          this.$store.state.data.dataNewCasesPerDayChart.confirmedCases.length - 1
        ]
      );
    },
    rawPerHundredChanged () {
      return positiveSign(
        Number(
          this.$store.state.data.dataCumulativeCasesChart.active100k[
            this.$store.state.data.dataCumulativeCasesChart.active100k.length - 1
          ] -
            this.$store.state.data.dataCumulativeCasesChart.active100k[
              this.$store.state.data.dataCumulativeCasesChart.active100k.length - 2
            ]
        ).toFixed(2)
      );
    },
    rawDeceasedChanged () {
      return Number(
        this.$store.state.data.deceasedChanged
      );
    },
    rawHospitalisedChanged () {
      return Number(
        this.$store.state.data.hospitalChanged
      );
    },
    rawOnVentilationChanged () {
      return Number(
        this.$store.state.data.onVentilationChanged
      );
    },
    rawTestsChanged () {
      return Number(
        this.$store.state.data.dataCumulativeTestsChart.testsAdministered[
          this.$store.state.data.dataCumulativeTestsChart.testsAdministered.length - 1
        ] -
        this.$store.state.data.dataCumulativeTestsChart.testsAdministered[
          this.$store.state.data.dataCumulativeTestsChart.testsAdministered.length - 2
        ]
      );
    },
    activeChanged () {
      return positiveSign(
        this.$store.state.data.activeChanged
      );
    },
    deceasedChanged () {
      return positiveSign(
        this.$store.state.data.deceasedChanged
      );
    },
    confirmedChanged () {
      return positiveSign(
        this.$store.state.data.dataNewCasesPerDayChart.confirmedCases[
          this.$store.state.data.dataNewCasesPerDayChart.confirmedCases.length - 1
        ]
      );
    },
    hospitalisedChanged () {
      return positiveSign(
        this.$store.state.data.hospitalChanged
      );
    },
    onVentilationChanged () {
      return positiveSign(
        this.$store.state.data.onVentilationChanged
      );
    },
    testsChanged () {
      return positiveSign(
        this.$store.state.data.dataCumulativeTestsChart.testsAdministered[
          this.$store.state.data.dataCumulativeTestsChart.testsAdministered.length - 1
        ] -
        this.$store.state.data.dataCumulativeTestsChart.testsAdministered[
          this.$store.state.data.dataCumulativeTestsChart.testsAdministered.length - 2
        ]
      );
    },
    vaccinatedAtLeastOneDoseNumber () {
      return this.$store.state.data.vaccinatedAtLeastOneDoseNumber;
    },
    vaccinatedAtLeastOneDoseChange () {
      return positiveSign(this.$store.state.data.vaccinatedAtLeastOneDoseChange);
    },
    vaccinatedAtLeastOneDosePercentage () {
      return this.$store.state.data.vaccinatedAtLeastOneDosePercentage;
    },
    fullyVaccinatedNumber () {
      return this.$store.state.data.fullyVaccinatedNumber;
    },
    fullyVaccinatedNumberChange () {
      return positiveSign(this.$store.state.data.fullyVaccinatedNumberChange);
    },
    fullyVaccinatedNumberPercentage () {
      return this.$store.state.data.fullyVaccinatedNumberPercentage;
    },
  },

  filters: {
    formatNumber: function (number, currentLocale, precision) {
      let result = "";

      if (typeof number === "string" && number.startsWith("+")) {
        const actualNumber = number.split("+")[1];
        result = "+" + formatNumberByLocale(actualNumber, currentLocale, precision);
      } else {
        result = formatNumberByLocale(number, currentLocale, precision);
      }

      return result.replace(/\s/g, "\u202F");
    },
  },
};
</script>


<style lang="scss" scoped>
h5 {
  font-size: 18px;
  font-weight: 500;
}

.vaccination-progress-label {
  display: flex;
  justify-content: space-between;
}
.vaccination-progress-text {
  font-size: 16px;
  text-align: left;
  margin-bottom: 0.25rem;
}
.vaccination-progress-value {
  font-size: 16px;
  margin-bottom: 0.25rem;
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

.progress {
  margin-bottom: 1rem;
}

.progress-bar {
  background-color: #7cb5ec;
}

.statsbar-item {
  //  height: 7em;

  @media only screen and (max-width: 766px) {
    margin-bottom: 1em;
  }
}
</style>
