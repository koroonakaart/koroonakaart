<template>
  <div>
    <b-modal v-model="show" centered id="disclaimer-modal">
      <b-container fluid>{{this.$t("disclaimerModal")}}</b-container>
      <template v-slot:modal-footer>
        <div class="w-100 text-center">
          <b-button variant="primary" size="sm" @click="show=false">OK</b-button>
        </div>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "DisclaimerModal",
  data() {
    return {
      show: false
    };
  }
};
</script>

<style lang="scss" scoped>
</style>