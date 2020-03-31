<template>
  <b-container id="footer-container" class="shadow-md p-3 text-dark" fluid>
    <b-container id="footer-innercontainer">
      <p>
        {{this.$t("footer1")}}
        <a
          href="https://garage48.org/blog/hack-the-crisis-from-an-idea-to-an-execution-in-just-6-hours"
          rel="noopener"
          target="_blank"
        >{{this.$t("footer2")}}</a>
        {{this.$t("footer3")}}
        <a
          href="https://www.terviseamet.ee"
          target="_blank"
          rel="noopener"
        >{{this.$t("footer4")}}</a>
        {{this.$t("footer5")}}
        <a
          href="https://github.com/buildig/EHAK"
          target="_blank"
          rel="noopener"
        >{{this.$t("footer6")}}</a>
        {{this.$t("footer7")}}
        <a
          href="https://www.stat.ee/"
          target="_blank"
          rel="noopener"
        >{{this.$t("footer8")}}</a>.
      </p>
      <p>
        {{this.$t("footer9")}}
        <a
          href="https://github.com/okestonia/koroonakaart/issues"
          target="_blank"
          rel="noreferrer"
        >https://github.com/okestonia/koroonakaart/issues</a>
      </p>
    </b-container>
  </b-container>
</template>

<script>
export default {
  name: "Footer"
};
</script>

<style lang="scss" scoped>
#footer-container {
  background-color: #eeeeee;
  border-top: 1px solid gainsboro;
}

#footer-innercontainer {
  word-wrap: break-word;
}
</style>
