<template>
  <div>
    <b-modal size="lg" v-model="show" id="disclaimer-modal">
      <b-container fluid>"Praegune valitsuskoalitsioon on näidanud korduvalt, et neile on osa inimesi võrdsemad kui teised. Globaalse pandeemia ajal, kui perekonnad Eestis ja mujal kannatavad, on valitsuse jaoks oluliseim, kas kaks inimest, kes üksteist armastavad, võivad abielluda. Portaal oli algselt ehitatud, et toetada valitsust, andmaks Eesti inimestele täpset ja ajakohast informatsiooni. Projekti juhina ja välismaalasena, LGBTQ õiguste toetajana, ei saa ma enam hoida seda lehekülge üleval, toetamaks valitsust, kes ei soovi austada Eesti põhiseadust ning luua toleratsent ja aktsepteerivat ühiskonda kõigile."<br><br>"The current government coalition has shown time and time again that, to them, some people are more equal than others. During a global pandemic, when families all around Estonia are suffering, the government’s most pressing issue is whether or not two people who love each other can get married. This portal was originally built to support the government in providing clear and accurate information to the Estonian people. However, as project manager, a foreigner, and supporter of LGBTQ rights, I can no longer keep this site up and running in support of a government that does not uphold the Estonian constitution or help to create a more tolerant acceptable society."<br><br></b-container>
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
