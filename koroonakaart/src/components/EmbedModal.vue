<template>
  <b-modal size="lg" id="embed-modal" hide-footer>
    <template v-slot:modal-title>Embed Graph</template>

    <div class="d-block text-center">
      <b-row class="mb-2 mt-3">
        <b-col cols="7" sm="4">
          <b>Chart height:</b>
        </b-col>
        <b-col cols="4" sm="2">
          <b-form-input size="sm" v-model="height"></b-form-input>
        </b-col>
      </b-row>

      <b-row class="mb-4">
        <b-col cols="7" sm="4">
          <b>Chart width:</b>
        </b-col>
        <b-col cols="4" sm="2">
          <b-form-input size="sm" v-model="width"></b-form-input>
        </b-col>
      </b-row>
      <div class="modal-code">
        <code>{{ iframeText }}</code>
      </div>
    </div>

    <div class="d-block text-center">
      <b-button
        align-h="center"
        size="sm"
        class="mt-3 w-25"
        variant="primary"
        @click="hideModal"
        >OK</b-button
      >
    </div>
  </b-modal>
</template>

<script>
export default {
  name: "EmbedModal",

  data() {
    return {
      height: "400",
      width: "400"
    };
  },

  methods: {
    hideModal: function() {
      this.$bvModal.hide("embed-modal");
    }
  },

  computed: {
    iframeText: function() {
      // prettier-ignore
      return `<iframe src="https://www.koroonakaart.ee/${this.$route.params.locale}/chart?chart=${this.$store.state.currentChartName}&height=${this.height}&width=${this.width}" scrolling="no" frameborder="0" style="overflow:hidden; height:${this.height}px; width:${this.width}px;" allowTransparency="true" loading="lazy"></iframe>`;
    }
  }
};
</script>

<style lang="scss" scoped>
.modal-code {
  background-color: rgb(240, 240, 240);
  border-radius: 4px;
  padding: 0.4em 1em;
  text-align: center;
  margin-bottom: 1em;

  & > code {
    color: rgb(255, 27, 27);
  }
}
</style>
