<template>
  <headroom>
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
          <small class="navbar-updated"
            >{{ $t("navbarUpdated") }}: {{ updatedOn }}</small
          >
        </b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <!--<b-nav-item class="navbar-updated">
          </b-nav-item>-->
            <b-dropdown-divider />
            <!--  <b-nav-item class="navbar-description"> -->
            <!-- <small>{{ $t("faq.a5") }}</small> -->

            <small
              >{{ $t("hoia.me") }}
              <a href="https://hoia.me" rel="noopener" target="_blank"
                >hoia.me</a
              ></small
            >

          <!--  <small>NB!  Viimase 24h COVID-19 testide tulemused viibivad tehnilisel põhjusel. Probleemiga tegeletakse ja esialgse prognoosi kohaselt peaks andmed laekuma täna pärastlõunal. Laboritest on veel saabumata ligi tuhande koroonaviiruse testi tulemus.</small>-->


            <!--  </b-nav-item> -->
          </b-navbar-nav>
          <b-navbar-nav class="ml-auto">
            <b-dropdown-divider />
            <b-nav-item toggle-class="nav-link-custom">
              <div
                class="navbar-faq"
                :class="{ active: this.$store.state.faqActive }"
                @click.prevent="toggleFaqActive"
              >
                {{ $t("faq.faqShort") }}
              </div>
            </b-nav-item>
            <b-dropdown-divider />
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav>
            <b-nav-item-dropdown id="navbar-langselect" right>
              <template align="center" v-slot:button-content>
                <Earth id="navbar-langicon" />
                <em>{{ $t("language") }}</em>
              </template>
              <b-dropdown-item
                @click="changeCurrentLanguage(locale)"
                v-for="(locale, index) in locales"
                :key="locale"
                >{{ languageNames[index] }}</b-dropdown-item
              >
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>
  </headroom>
</template>

<script>
import Earth from "vue-material-design-icons/Earth.vue";
import { headroom } from "vue-headroom";

import data from "../data.json";

export default {
  name: "Navbar",

  components: {
    //Earth icon
    Earth,
    headroom,
  },

  data() {
    return {
      languageNames: ["Eesti", "English", "Русский"],
      updatedOn: data.updatedOn,
      faqActive: false,
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
        initialLocales[0],
      ];
      return initialLocales;
    },
    linkToFaq: function() {
      return `/${this.$i18n.locale}/faq`;
    },
  },

  // Change current locale to targetLanguage and change route to the targetLanguage
  methods: {
    changeCurrentLanguage: function(targetLanguage) {
      if (this.$i18n.locale === targetLanguage) return;

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
      if (this.$route.path === `/${this.$i18n.locale}/faq`) return;

      this.$store.dispatch("toggleFaqActive");
      this.$router.push({ path: `/${this.$i18n.locale}/faq` });
    },
  },
};
</script>

<style lang="scss" scoped>
.navbar-brand small {
  display: block;
  font-size: 12px;
}

.navbar-toggle {
  top: 10px;
}

.navbar-description {
  word-wrap: break-word;

  & > *:hover {
    color: rgba(0, 0, 0, 0.5) !important;
    cursor: default !important;
  }
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

.navbar-updated {
  cursor: default;
}
</style>
