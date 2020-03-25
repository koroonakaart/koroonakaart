<template>
  <div id="chat-container1">
    <button class="chat-button1" type="button" @click="openChat">{{ $t("answerbot") }}</button>
  </div>
</template>

<script>
export default {
  name: "SuveChatbot",
  mounted() {
    // Chati avamiseks automaatselt
    //	chatPanel.show();
  },
  computed: {
    chatPanel: function() {
      return window.boostChatPanel({
        apiUrlBase: "https://316eebot.boost.ai/api",
        language:
          this.$route.params.locale === "en"
            ? "en-US"
            : this.$route.params.locale === "ru"
            ? "ru-RU"
            : "et-EE"

        //  eesti keel on vaikimisi aktiivne
        // inglise lehelt avades vajalik määrata tervitusteksti keel 'en-US' ja vene lehelt 'ru-RU'
        //	language:'et-EE'
      });
    }
  },
  methods: {
    openChat: function() {
      this.chatPanel.show();
    }
  }
};
</script>

<style lang="scss" scoped>
.chat-button1 {
  border: none;
  position: fixed;
  bottom: 60px;
  right: 140px;
  font-size: 16px;
  line-height: 20px;
  padding: 10px 15px;
  border-radius: 6px;
  background: none;
  box-shadow: none;
  height: auto;
  margin: 0;
  text-shadow: none;
  background-color: #00698c;
  color: #fff;
  z-index: 999;
  box-sizing: border-box;

  @media only screen and (max-width: 600px) {
    font-size: 12px;
    padding: 7px 10px;
    bottom: 20px;
    right: 80px;
  }
}

.chat-button1:hover,
.chat-button1:focus {
  box-shadow: none;
  background: none;
  background-color: #00698c;
  outline: 0;
}

.chat-button1:before {
  content: "";
  display: block;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 7px 0 7px 8px;
  border-color: transparent transparent transparent #00698c;
  position: absolute;
  left: 100%;
  top: 13px;
  @media only screen and (max-width: 600px) {
    top: 10px;
  }
}

.chat-button1:after {
  content: "";
  display: block;
  width: 80px;
  height: 80px;
  position: absolute;
  left: calc(100% + 20px);
  top: -20px;
  border-radius: 50%;
  background-image: url(../assets/robot.svg);
  background-repeat: no-repeat;
  background-size: 60px 60px;
  background-position: center;
  background-color: #00698c;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);

  @media only screen and (max-width: 600px) {
    background-size: 30px 30px;
    left: calc(100% + 20px);
    top: 0px;
    height: 40px;
    width: 40px;
  }
}
</style>