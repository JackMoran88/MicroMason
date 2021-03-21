<template>
  <v-account-form
    @save="preSave"
    @toggle="toggle"
    ref="account_form"
  >
    <div slot="header">
      <div class="form__title"><span>account_circle</span>Личные данные</div>
    </div>
    <div slot="body">
      <ValidationObserver ref="form">
        <form @submit.prevent="preSave">
          <fieldset>
            <ValidationProvider
              name="first_name"
              rules="required|alpha|minmax:2,15"
            >
              <div slot-scope="{ errors}">
                <v-input
                  InputTitle="Имя"
                  v-model.trim="userData.first_name"
                  :InputValue="userData.first_name"
                  InputType='text'
                  :InputLoading="loading"
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
            <ValidationProvider
              name="last_name"
              rules="required|alpha|minmax:2,15">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Фамилия"
                  v-model.trim="userData.last_name"
                  :InputValue="userData.last_name"
                  InputType='text'
                  :InputLoading="loading"
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </fieldset>
        </form>
      </ValidationObserver>

      <b-modal
        id="account_form__passModal"
        title="Подтверждение"
        hide-footer
        centered
        scrollable
      >
        <ValidationObserver ref="account_form__password">
          <form @submit.prevent="save">
            <fieldset>
              <ValidationProvider
                name="first_name"
                rules="required"
              >
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Пароль"
                    v-model.trim="userData.password"
                    :InputValue="userData.password"
                    InputType='password'

                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>
            </fieldset>
            <v-btn
              BtnStyle="success"
              BtnType="submit"
              BtnName="Подтвердить"
              class="w-100"

            />
          </form>
        </ValidationObserver>

      </b-modal>
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
          first_name: '',
          last_name: '',
          password: '',
        },
        loading: false,
      };
    },
    methods: {
      load() {
        this.setLoading(true)
        this.GET_CUSTOMER_DETAIL(this.TOKEN).then(() => {
          this.getData();
        });
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
      },
      getData() {
        if (this.USER === null) {
          this.clearData();
          return;
        }
        this.userData.first_name = this.USER.first_name;
        this.userData.last_name = this.USER.last_name;
        this.setLoading(false)
      },
      preSave() {
        this.$refs.form.validate().then((success) => {
          if (!success) {
            return;
          }
          this.$bvModal.show('account_form__passModal')
        })
      },
      save() {
        this.$refs.account_form__password.validate().then((success) => {
          if (!success) {
            return;
          }
          const {first_name} = this.userData;
          const {last_name} = this.userData;
          const {password} = this.userData;

          this.SET_CUSTOMER_CHANGES({first_name, last_name, password}).then(() => {
            this.$refs.account_form.toggle();
            this.$toast('success', 'Настройки успешно применены!');
          }).catch((error) => {
            let errors = this.$request_errors(error)
            for (error of errors) {
              this.$toast('error', error);
            }
          }).finally(() => {
            this.clearData();
            this.getData();
            this.$bvModal.hide('account_form__passModal')
          })


        });
      },
      toggle() {
        this.getData();
      },
      ...mapActions(['GET_CUSTOMER_DETAIL', 'SET_CUSTOMER_CHANGES']),
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
