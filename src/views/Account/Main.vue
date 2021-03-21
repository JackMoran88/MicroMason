<template>
  <div id="account-main" v-if="IS_LOGGED_IN">
    <v-title
      text="Личные данные"
    />

    <v-account-main-form/>

    <v-account-contact-form/>

    <v-account-address-form/>

    <v-account-password-form/>

  </div>
</template>

<script>
import vAccountAddressForm from '@/components/account/v-account-address-form.vue';
import vAccountContactForm from '@/components/account/v-account-contact-form.vue';
import vAccountMainForm from '@/components/account/v-account-main-form.vue';
import vAccountPasswordForm from '@/components/account/v-account-password-form.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'v-main',
  components: {
    vAccountAddressForm, vAccountContactForm, vAccountMainForm,vAccountPasswordForm
  },
  data() {
    return {};
  },
  methods: {
  },
  computed: {
    ...mapGetters(['IS_LOGGED_IN'])
  },
  mounted() {
  },
};
</script>

<style scoped lang="scss">

</style>
