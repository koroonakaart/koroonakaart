<template>
  <div class="loading">
    {{ $t("loading") }}
  </div>
</template>

<script>
export default {
  name: "Loading",
};
</script>

<style lang="scss" scoped>
.loading {
  padding: 3rem;
  text-align: center;
  vertical-align: center;
  display: block;
}
</style>
