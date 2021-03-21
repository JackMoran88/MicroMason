<template>
  <v-account-form
    @save="preSave"
    @toggle="toggle"
    ref="contact_form"
  >
    <div slot="header">
      <div class="form__title"><span>email</span>Контакты</div>
    </div>
    <div slot="body">
      <ValidationObserver ref="form">
        <form @submit.prevent="preSave">
          <fieldset>
            <ValidationProvider name="phone" rules="required|phone">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Номер телефона"
                  v-model.trim="userData.phone"
                  :InputValue="userData.phone"
                  InputType='text'
                  :InputLoading="loading"
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
            <ValidationProvider name="email" rules="required|email">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Логин(электронная почта)"
                  v-model.trim="userData.email"
                  :InputValue="userData.email"
                  InputType='email'
                  :InputLoading="loading"
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </fieldset>
        </form>
      </ValidationObserver>

      <b-modal
        id="contact_form__passModal"
        title="Подтверждение"
        hide-footer
        centered
        scrollable
      >
        <ValidationObserver ref="contact_form__password">
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
    name: 'v-account-contact-form',
    components: {
      vAccountForm,
    },
    data() {
      return {
        userData: {
          email: '',
          phone: '',
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
          email: '',
          phone: '',
          password: '',
        };
      },
      getData() {
        if (this.USER === null) {
          this.clearData();
          return;
        }
        this.userData.email = this.USER.email;
        this.userData.phone = this.USER.phone_number;
        this.setLoading(false)
      },
      toggle() {
        this.getData();
      },
      preSave() {
        this.$refs.form.validate().then((success) => {
          if (!success) {
            return;
          }
          this.$bvModal.show('contact_form__passModal')
        })
      },
      save() {
        this.$refs.contact_form__password.validate().then((success) => {
          if (!success) {
            return;
          }
          const {email} = this.userData;
          const {phone} = this.userData;
          const {password} = this.userData;

          this.SET_CUSTOMER_CHANGES({email, phone, password}).then(() => {
            this.$toast('success', 'Настройки успешно применены!');
            this.$refs.contact_form.toggle();
          })
            .catch((error) => {
              let errors = this.$request_errors(error)
              for (error of errors) {
                this.$toast('error', error);
              }
            })
            .finally(() => {
              this.clearData();
              this.getData();
              this.$bvModal.hide('contact_form__passModal')
            })

        });
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
