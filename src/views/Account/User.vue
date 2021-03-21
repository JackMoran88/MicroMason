<template>
  <div class="USER">

    <v-form
      novalidate
      class="type-1"
    >
      <div slot="header">
        СБРОС ПАРОЛЯ
      </div>
      <div slot="body">
        <ValidationObserver ref="form">
          <form @submit.prevent="change_password">
            <fieldset>
              <ValidationProvider name="password" rules="required|password" vid="password">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Новый пароль"
                    v-model="user.password"
                    InputType='password'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>

              <ValidationProvider name="password_confirm" rules="required|confirmed:password">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Подтверждение пароля"
                    v-model="user.password_confirm"
                    InputType='password'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>
            </fieldset>
          </form>
        </ValidationObserver>
      </div>
      <div slot="errors" class="form__errors" v-if="errors">
        <!--        У error нет id-->
        <div
          v-for="error in errors" :key="error.id"
        >{{error}}
        </div>
      </div>
      <div slot="footer">
        <v-btn
          BtnName="Изменить"
          BtnStyle="success"
          @click.native.prevent="validate"
          @click.native="change_password"
        />
      </div>
    </v-form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'User',
  data() {
    return {
      user: {
        password: '',
        confirm_password: '',
      },
      errors: [],
    };
  },
  methods: {
    change_password() {
      this.$refs.form.validate().then((success) => {
        if (!success) {
          return;
        }
        const data = {
          uid: this.$route.params.uid,
          token: this.$route.params.token,
          new_password: this.user.password,
        };
        this.CHANGE_PASSWORD(data)
          .then(() => {
            this.$router.replace({ name: 'Home' });
          })
          .catch((error) => {
            this.errors = this.$request_errors(error);
          });
      });
    },
    ...mapActions(['CHANGE_PASSWORD']),
  },
  computed: {},
  mounted() {

  },

};
</script>

<style scoped lang="scss">
  .USER {
    width: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;

    .form {
      max-width: 500px;
      margin: auto 0;

      button {
        width: 100%;
      }
    }
  }
</style>
