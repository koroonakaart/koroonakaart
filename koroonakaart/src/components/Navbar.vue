<template>
  <b-navbar
    class="shadow-sm p-3 mb-4 bg-white rounded"
    sticky
    toggleable="md"
    type="light"
    variant="light"
  >
    <b-container fluid="lg">
      <b-navbar-brand>
        <span id="navbar-headingleft" @click="this.goBackHome">Koroona</span>
        <span id="navbar-headingright" @click="this.goBackHome">kaart</span>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item toggle-class="nav-link-custom">
            <div
              class="navbar-faq"
              :class="{ active: this.$store.state.faqActive }"
              @click.prevent="toggleFaqActive"
            >{{ $t("faq.faqLong") }}</div>
          </b-nav-item>
          <!-- <b-nav-item class="navbar-description">
            <small>{{ $t("disclaimerNavbar") }}</small>
          </b-nav-item>-->
          <b-nav-item id="navbar-interpunct">·</b-nav-item>
          <b-nav-item class="navbar-updated">
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

import data from "../data.json";

export default {
  name: "Navbar",

  components: {
    //Earth icon
    Earth
  },

  data() {
    return {
      languageNames: ["Eesti", "English", "Русский"],
      updatedOn: data.updatedOn,
      faqActive: false
    };
  },

  // On navbar update change locale to current route suffix (ee, en or ru)
  updated() {
    if (this.$i18n.locale !== this.$route.params.locale)
      this.changeCurrentLanguage(this.$route.params.locale);
  },

  // Get available locales
  computed: {
    locales: function() {
      const initialLocales = this.$i18n.availableLocales;
      // Swap order of locales so et would become before en
      [initialLocales[0], initialLocales[1]] = [
        initialLocales[1],
        initialLocales[0]
      ];
      return initialLocales;
    },
    linkToFaq: function() {
      return `/${this.$i18n.locale}/faq`;
    }
  },

  // Change current locale to targetLanguage and change route to the targetLanguage
  methods: {
    changeCurrentLanguage: function(targetLanguage) {
      if (this.$route.path.includes("faq")) {
        this.$router.push({ path: `/${targetLanguage}/faq` });
      } else {
        this.$router.push(targetLanguage);
      }

      this.$i18n.locale = targetLanguage;

      const language = targetLanguage !== undefined ? targetLanguage : "et";
      localStorage.setItem("koroonaLang", language);
    },

    goBackHome: function() {
      if (this.$route.path === `/${this.$i18n.locale}`) return;

      this.$store.dispatch("toggleFaqInactive");
      this.$router.push(`/${this.$i18n.locale}`);
    },
    toggleFaqActive: function() {
      this.$store.dispatch("toggleFaqActive");
      this.$router.push({ path: `/${this.$i18n.locale}/faq` });
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
  cursor: pointer;
  font-size: 1.2em;
  font-weight: 900;
}

#navbar-headingright {
  color: #4072cd;
  cursor: pointer;
  font-size: 1.2em;
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

.navbar-faq {
  color: black;
  font-weight: 500;
  margin-left: 2em;

  &:hover {
    text-decoration: underline;
  }
}

.active {
  text-decoration: underline;
}

.menu-item {
  background-color: #4072cd;
}

.nav-item.navbar-updated {
  small {
    &:hover {
      cursor: default !important;
    }
  }

  &:hover {
    cursor: default !important;
  }
}
</style>
