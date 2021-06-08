<template>
  <div class="v-social-auth">
    <font-awesome-icon
      :icon="['fab', 'google']"
      size="2x"
      @click="AuthProvider('google')"
    />
  </div>
</template>

<script>
  import {mapActions} from 'vuex';
  import {library} from "@fortawesome/fontawesome-svg-core";
  import {faGoogle} from '@fortawesome/free-brands-svg-icons';
  import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

  library.add(faGoogle);

  export default {
    name: 'v-social-auth',
    components: {
      FontAwesomeIcon
    },
    data() {
      return {};
    },
    methods: {
      AuthProvider(provider) {
        this.$auth.authenticate(provider).then((response) => {
          const data = {
            provider,
            response,
            code: response.code,
          };
          this.SOCIAL_AUTH(data);
        }).catch((error) => {
          console.log(error);
        });
      },
      ...mapActions(['SOCIAL_AUTH']),
    },
    mounted() {

    },
  };
</script>

<style scoped lang="scss">

  .v-social-auth {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;

    margin: .75rem 0;

    > * {
      cursor: pointer;
    }
  }

</style>
