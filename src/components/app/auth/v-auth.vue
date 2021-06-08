<template>
  <div class="auth">
    <v-form
      v-show="methodAuth === 1"
      novalidate
      class="type-1"
      @submit.prevent="login"
      ref="form__login"
    >
      <div slot="body">
        <ValidationObserver ref="obs__login">
            <fieldset>
              <ValidationProvider name="email" rules="required|email">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="E-mail"
                    v-model="email"
                    InputType='email'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>
              <ValidationProvider name="password" rules="required">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Пароль"
                    v-model="password"
                    InputType='password'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>
            </fieldset>
        </ValidationObserver>
      </div>
      <div slot="footer">
        <div class="remember-me">
          <div>
            <label>
              <p-check
                class="p-default p-round p-thick"
                color="primary-o"
                v-model="remember_me"
                :value="remember_me"
              >Запомнить меня
              </p-check>
            </label>
          </div>
          <v-btn
            BtnName="Забыл пароль"
            BtnStyle="secondary"
            class="btn-minimal"
            @click.native="setMethodAuth(3)"
          />
        </div>
        <v-btn
          BtnName="Войти"
          BtnType="submit"
          BtnStyle="success"
          class="w-100"
          @click.native="login"
          @click.native.prevent
        />
        <v-social-auth/>
        <v-btn
          BtnName="Зарегистрироваться"
          BtnStyle="secondary"
          class="w-100"
          @click.native="setMethodAuth(2)"
        />
      </div>
      <div slot="errors" class="form__errors" v-if="error_in">
        <div
          v-for="error in error_in" :key="error.id"
        >{{error}}
        </div>
      </div>
    </v-form>
    <v-form
      v-show="methodAuth === 2"
      novalidate
      class="type-1"
      @submit.prevent="register"
      ref="form__register"
    >
      <div slot="body">
        <ValidationObserver ref="obs__register">
            <fieldset>
              <ValidationProvider name="first_name" rules="required|alpha">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Имя"
                    v-model="first_name"
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>

              <ValidationProvider name="last_name" rules="required|alpha">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Фамилия"
                    v-model="last_name"

                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>

              <ValidationProvider name="email" rules="required|email">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="E-mail"
                    v-model="email"
                    InputType='email'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>

              <ValidationProvider name="password" rules="required|password" vid="password">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Пароль"
                    v-model="password"
                    InputType='password'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>

              <ValidationProvider name="password_confirm" rules="required|confirmed:password">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="Подтверждение пароля"
                    v-model="password_confirm"
                    InputType='password'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>

            </fieldset>
        </ValidationObserver>
      </div>
      <div slot="footer">
        <v-btn
          BtnName="Регистрация"
          class="w-100"
          @click.native="register"
          @click.native.prevent
          BtnStyle="success"
          BtnType="submit"
        />
        <v-btn
          BtnName="Войти"
          BtnStyle="secondary"
          class="w-100"
          @click.native="setMethodAuth(1)"
        />
      </div>
       <div slot="errors" class="form__errors" v-if="error_up">
        <div
          v-for="error in error_up" :key="error.id"
        >{{error}}
        </div>
      </div>
    </v-form>

    <v-form
      v-show="methodAuth === 3"
      novalidate
      class="type-1"
    >
      <div slot="body" v-if="!reset_email_sent">
        <ValidationObserver ref="obs__reset">
          <form @submit.prevent="reset_password" ref="form__reset">
            <fieldset>
              <ValidationProvider name="email" rules="required|email">
                <div slot-scope="{ errors }">
                  <v-input
                    InputTitle="E-mail"
                    v-model="email"
                    InputType='email'
                  />
                  <span class="invalid">{{ errors[0] }}</span>
                </div>
              </ValidationProvider>
            </fieldset>
          </form>
        </ValidationObserver>
      </div>
      <div slot="body" v-if="reset_email_sent">
        <v-title
          text="Сообщение отправлено!"
          class="my-5 text-center"
        />
      </div>
      <div slot="footer">
        <v-btn
          v-if="!reset_email_sent"
          BtnStyle="success"
          BtnName="Отправить"
          class="w-100"
          @click.native="reset_password()"
          @click.native.prevent
        />
        <v-btn
          BtnStyle="secondary"
          BtnName="Назад"
          class="w-100"
          @click.native="setMethodAuth(1)"
        />
      </div>
      <div slot="errors" class="form__errors" v-if="error_in">
        <div
          v-for="error in error_in" :key="error.id"
        >{{error}}
        </div>
      </div>
    </v-form>
  </div>
</template>

<script>
  import {mapActions, mapGetters} from 'vuex';
  import vSocialAuth from '@/components/app/auth/v-social-auth.vue';
  import PCheck from 'pretty-checkbox-vue/check';

  export default {
    name: 'v-auth',
    components: {
      vSocialAuth, PCheck,
    },
    data() {
      return {
        methodAuth: 1,

        first_name: '',
        last_name: '',
        email: '',
        password: '',
        password_confirm: '',

        error_in: [],
        error_up: [],

        remember_me: false,

        reset_email_sent: false,
      };
    },
    methods: {
      setModalTitle(value) {
        document.querySelector('#authModal .modal-header h5').innerHTML = value
      },
      setMethodAuth(value) {
        this.methodAuth = value;

        switch (this.methodAuth) {
          case 1:
            this.setModalTitle('Вход');
            break;
          case 2:
            this.setModalTitle('Регистрация');
            break;
          case 3:
            this.setModalTitle('Востановление пароля');
            break;
          default:
            this.setModalTitle('Вход');
            break;
        }

        this.clear();
      },

      clear() {
        if (this.$refs.form__login) {
          this.$refs.obs__login.reset()
          this.$refs.form__login.reset()
        }
        if (this.$refs.form__register) {
          this.$refs.obs__register.reset()
          this.$refs.form__register.reset()
        }
        if (this.$refs.form__reset) {
          this.$refs.obs__reset.reset()
          this.$refs.form__reset.reset()
        }
        this.error_in = [];
        this.error_up = [];
        this.remember_me = false;

        this.first_name = '';
        this.last_name = '';
        this.email = '';
        this.password = '';
        this.password_confirm = '';

        this.reset_email_sent = false;
      },

      reset_password() {
        this.$refs.obs__reset.validate().then((success) => {
          if (!success) {
            return;
          }
          const data = {
            email: this.email,
          };
          this.SEND_EMAIL_TO_RESET_PASSWORD(data).then(() => {
            this.reset_email_sent = true;
          });
        });
      },
      login() {
        this.$refs.obs__login.validate().then((success) => {
          if (!success) {
            return;
          }
          const data = {
            email: this.email,
            password: this.password,
            remember: this.remember_me,
          };
          this.LOGIN(data)
            .then(() => {
              this.$bvModal.hide('authModal');
              this.$toast('success', `Добро пожаловать, ${this.FULL_USER_NAME}!`)
            })
            .catch((error) => {
              this.error_in = this.$request_errors(error);
            });
        });
      },
      register() {
        this.$refs.obs__register.validate().then((success) => {
          if (!success) {
            return;
          }
          const data = {
            first_name: this.first_name,
            last_name: this.last_name,
            email: this.email,
            password: this.password,
          };
          this.REGISTER(data)
            .then(() => {
              this.$bvModal.hide('authModal');
              this.$toast('success', 'Вы успешно зарегистрировались!')
            })
            .catch((error) => {
              this.error_up = this.$request_errors(error);
            });
        });
      },

      ...mapActions(['LOGIN', 'REGISTER', 'SEND_EMAIL_TO_RESET_PASSWORD']),
    },
    computed: {
      ...mapGetters(['FULL_USER_NAME'])
    },
    mounted() {
    },
    destroyed() {
      this.clear();
    },
  };
</script>

<style scoped lang="scss">
  div.auth {
    width: 100%;

    form {
      .remember-me {
        display: flex;
        justify-content: space-between;
        padding: 0 .3rem;

        a {
          text-decoration: none;
          @include link($hover: none);
        }
      }

      .social_auth {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;

        button {
          width: 60px;
          height: 60px;
          border-radius: 50px;

          img {
            max-width: 100%;
            max-height: 100%;
          }
        }
      }

      button.w-100 {
        width: 100%;
        display: flex;
        justify-content: center;
      }
    }
    button.secondary.w-100{
      margin: .75rem 0;
    }
  }

</style>
