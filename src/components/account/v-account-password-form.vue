<template>
  <v-account-form
    @save="preSave"
    @toggle="toggle"
    ref="secure_form"
  >
    <div slot="header">
      <div class="form__title"><span>lock</span>Безопасность</div>
    </div>
    <div slot="body">
      <ValidationObserver ref="form">
        <form @submit.prevent="preSave">
          <fieldset>
            <ValidationProvider
              name="password"
              rules="required"
            >
              <div slot-scope="{ errors}">
                <v-input
                  InputTitle="Текущий пароль"
                  v-model.trim="userData.password"
                  :InputValue="userData.password"
                  InputType='password'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
            <ValidationProvider
              name="new_password"
              rules="required|password"
              vid="new_password"
            >
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Новый пароль"
                  v-model.trim="userData.new_password"
                  :InputValue="userData.new_password"
                  InputType='password'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
            <ValidationProvider
              name="new_password_confirm"
              rules="required|confirmed:new_password">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Подтверждение текущего пароля"
                  v-model.trim="userData.new_password_confirm"
                  :InputValue="userData.new_password_confirm"
                  InputType='password'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </fieldset>
        </form>
      </ValidationObserver>
    </div>
  </v-account-form>
</template>

<script>
  import vAccountForm from '@/components/app/form/v-account-form.vue';
  import {mapActions, mapGetters} from 'vuex';

  export default {
    name: 'v-account-main-form',
    components: {
      vAccountForm,
    },
    data() {
      return {
        userData: {
          password: '',
          new_password: '',
          new_password_confirm: '',
        },
        loading: false,
      };
    },
    methods: {
      load() {
        this.setLoading(true)
      },
      setLoading(value) {
        this.loading = value;
      },
      clearData() {
        this.userData = {
          first_name: '',
          last_name: '',
          password: '',
        };
        this.$refs.form.reset()
      },
      preSave() {
        this.$refs.form.validate().then((success) => {
          if (!success) {
            return;
          }
          this.save()

        })
      },
      save() {
        const {password} = this.userData;
        const {new_password} = this.userData;

        this.SET_CUSTOMER_CHANGES({password, new_password}).then(() => {
          this.$refs.secure_form.toggle();
          this.$toast('success', 'Настройки успешно применены!');
        }).catch((error) => {
          let errors = this.$request_errors(error)
          for (error of errors) {
            this.$toast('error', error);
          }
        })
      },
      toggle() {
        this.clearData()
      },
      ...mapActions(['SET_CUSTOMER_CHANGES']),
    },
    computed: {
      ...mapGetters(['USER', 'TOKEN']),
    },
    mounted() {
      this.load()
    },
  };
</script>

<style scoped lang="scss">

</style>
