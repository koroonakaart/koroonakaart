<template>
  <b-navbar
    class="shadow-sm p-3 mb-4 bg-white rounded"
    sticky
    toggleable="lg"
    type="light"
    variant="light"
  >
    <b-container fluid="lg">
      <b-navbar-brand>
        <span id="navbar-headingleft">Koroona</span>
        <span id="navbar-headingright">kaart</span>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item class="navbar-description">
            <small>{{ $t("navbarDescription") }}</small>
          </b-nav-item>
          <b-nav-item id="navbar-interpunct">·</b-nav-item>
          <b-nav-item>
            <small>{{ $t("navbarUpdated") }}: {{updatedOn}}</small>
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown id="navbar-langselect" right>
            <template align="center" v-slot:button-content>
              <Earth id="navbar-langicon" />
              <em>{{ $t("language") }}</em>
            </template>
            <b-dropdown-item
              @click="changeCurrentLanguage(locale)"
              v-for="(locale, index) in locales"
              :key="locale"
            >{{ languageNames[index] }}</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-container>
  </b-navbar>
</template>

<script>
import Earth from "vue-material-design-icons/Earth.vue";

import { updatedOn } from "../dataConstants";

export default {
  name: "Navbar",

  components: {
    //Earth icon
    Earth
  },

  data() {
    return {
      languageNames: ["Eesti", "English", "Pусский"],
      updatedOn
    };
  },

  computed: {
    locales: function() {
      return this.$i18n.availableLocales;
    }
  },

  methods: {
    changeCurrentLanguage: function(targetLanguage) {
      if (this.$route.params.locale !== targetLanguage) {
        this.$router.push(targetLanguage);
      }
      this.$i18n.locale = targetLanguage;
      window.location.reload();
    }
  }
};
</script>

<style lang="scss" scoped>
.navbar-description {
  word-wrap: break-word;
}

#navbar-headingleft {
  color: black;
  font-weight: 900;
}

#navbar-headingright {
  color: #4072cd;
  font-weight: 900;
}

#navbar-interpunct {
  font-weight: 900;
}

#navbar-langicon {
  padding: 0em 1.5em;
}

#navbar-langselect {
  font-size: 1.2em;
  text-align: center;
}
</style>
