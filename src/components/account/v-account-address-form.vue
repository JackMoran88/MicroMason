<template>
  <v-account-form
    @toggle="close"
    @save="save"
    ref="account_form"
  >
    <div slot="header">
      <div class="form__title"><span>local_shipping</span>Адресс доставки</div>
    </div>

    <div slot="body" v-show="addressLength">

      <v-select
        v-if="ADDRESS.length > 0 && isSelector"
        :current="ADDRESS[0].id"
        @option:selected="changeAddress"
        :value="$search_by(address_options, 'value', curAddress)"
        placeholder="Выберите адрес доставки"
        :options="address_options"
        :clearable="false"
        :searchable="false"
      ></v-select>


      <ValidationObserver ref="form">
        <form @submit.prevent="save">
          <fieldset>
            <ValidationProvider
              name="first_name"
              rules="required|alpha|minmax:2,15"
            >
              <div slot-scope="{ errors}">
                <v-input
                  InputTitle="Имя"
                  v-model.trim="addressData.first_name"
                  :InputValue="addressData.first_name"
                  InputType='text'
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
                  v-model.trim="addressData.last_name"
                  :InputValue="addressData.last_name"
                  InputType='text'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>

            <ValidationProvider name="email" rules="required|email">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Электронная почта"
                  v-model.trim="addressData.email"
                  :InputValue="addressData.email"
                  InputType='email'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>

            <ValidationProvider name="phone" rules="required|phone">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Номер телефона"
                  v-model.trim="addressData.phone_number"
                  :InputValue="addressData.phone_number"
                  InputType='text'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
            <ValidationProvider name="city" rules="required">
              <div slot-scope="{ errors }">
                <v-search-city
                  :InputValue="addressData.city"
                  @input="updCityValue"
                  v-model="addressData.city"
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
            <ValidationProvider name="address" rules="">
              <div slot-scope="{ errors }">
                <v-input
                  InputTitle="Адрес"
                  v-model.trim="addressData.address"
                  :InputValue="addressData.address"
                  InputType='text'
                />
                <span class="invalid">{{ errors[0] }}</span>
              </div>
            </ValidationProvider>
          </fieldset>
        </form>
      </ValidationObserver>
    </div>
    <div slot="body" v-if="!addressLength">
      <v-title-small
        text="Адрессов не найдено"
      />
    </div>

    <v-btn
      v-if="curAddress"
      :BtnIcon="IS_MOBILE ? 'delete': ''"
      :BtnName="IS_DESKTOP ? 'Удалить': ''"
      BtnStyle="danger"
      class="mr-auto"
      slot="footer+"
      @click.native="DELETE_ADDRESS(curAddress)"
    />
    <v-btn
      v-if="isBtnAdd"
      BtnStyle="secondary"
      :BtnIcon="IS_MOBILE ? 'add': ''"
      :BtnName="IS_DESKTOP ? 'Добавить новый адресс': ''"
      slot="footer+"
      @click.native="createNewAddress"
    />
    <v-btn
      v-if="!isBtnAdd && IS_LOGGED_IN"
      BtnStyle="secondary"
      BtnName="Персонализировать"
      slot="footer+"
      @click.native="personalizeNewAddress"
    />
  </v-account-form>
</template>

<script>
  import {mapActions, mapGetters, mapMutations} from 'vuex';
  import vAccountForm from '@/components/app/form/v-account-form.vue';
  import vSearchCity from '@/components/app/form/v-search-city.vue';

  export default {
    name: 'v-account-address-form',
    props: {},
    components: {vAccountForm, vSearchCity},
    data() {
      return {
        curAddress: '',
        isSelector: false,
        isBtnAdd: true,
        addressLength: null,
        address_options: [],
        loading: false,
        addressData: {
          first_name: '',
          last_name: '',
          email: '',
          phone_number: '',
          address: '',
          city: '',
        },
      };
    },
    methods: {
      setLoading(value) {
        this.loading = value;
      },
      updCityValue(value) {
        this.addressData.city = value;
      },
      load() {
        this.setLoading(true)
        this.GET_ADDRESS().then(() => {
          if (this.ADDRESS.length) {
            this.addressLength = this.ADDRESS.length;
            this.curAddress = this.ADDRESS[0].id;
            this.loadAddressForm();
            this.loadAddress_options();
            this.SET_CHECKOUT_ADDRESS(this.curAddress);
            // Обновляю селектор, чтобы отобразился адрес
            this.isSelector = true;
          } else {
            this.addressLength = null;
            this.clearAddressForm();
          }
          this.isBtnAdd = true
          this.setLoading(false)
        });
      },
      loadAddressForm() {
        const curAddressData = this.$search_by(this.ADDRESS, 'id', this.curAddress);
        if (curAddressData) {
          this.addressData.first_name = curAddressData.first_name;
          this.addressData.last_name = curAddressData.last_name;
          this.addressData.email = curAddressData.email;
          this.addressData.phone_number = curAddressData.phone_number;
          this.addressData.address = curAddressData.address;
          // this.addressData.postal_code = curAddressData.postal_code
          this.addressData.city = curAddressData.city;
        }
      },
      clearAddressForm() {
        this.curAddress = '';
        for (const key of Object.keys(this.addressData)) {
          this.addressData[key] = '';
        }
        if (this.$refs.form) {
          this.$refs.form.reset()
        }
      },
      createNewAddress() {
        this.isSelector = false;
        this.isBtnAdd = false;
        this.clearAddressForm();
        this.addressLength = 1;
      },
      personalizeNewAddress() {
        if (this.IS_LOGGED_IN) {
          this.addressData.first_name = this.USER.first_name
          this.addressData.last_name = this.USER.last_name
          this.addressData.email = this.USER.email
          this.addressData.phone_number = this.USER.phone_number
        }
      },
      save() {
        if (!this.$refs.form) {
          this.$refs.account_form.toggle();
          return;
        }
        this.$refs.form.validate().then((success) => {
          if (!success) {
            return;
          }
          if (this.curAddress) {
            this.addressData.id = this.curAddress;
          }
          this.addressData.priority = true;
          this.CREATE_ADDRESS(this.addressData).then(() => {
            this.load();
          });
          this.$refs.account_form.toggle();
        })
      },
      close() {
        this.load();
      },
      loadAddress_options() {
        this.address_options = this.ADDRESS.map((value) => {
          return {
            label: `${value.first_name} ${value.last_name} - ${value.city}`,
            value: value.id
          }
        })
      },
      changeAddress(select) {
        this.curAddress = select.value;
        this.loadAddressForm()
        this.SET_CHECKOUT_ADDRESS(this.curAddress);
      },
      ...mapActions(['GET_ADDRESS', 'CREATE_ADDRESS', 'DELETE_ADDRESS']),
      ...mapMutations(['SET_CHECKOUT_ADDRESS'])
    },
    mounted() {
      this.load();
    },
    computed: {
      ...mapGetters(['ADDRESS', 'IS_LOGGED_IN', 'USER', 'IS_DESKTOP', 'IS_MOBILE']),
    },
    watch: {
      'curAddress'() {
        this.loadAddressForm();
      },
      'ADDRESS.length'() {
        this.load();
      },
      'USER'() {
        this.load()
      }
    },
  };
</script>

<style scoped lang="scss">
  .v-select {
    margin: .5rem 0;
  }
</style>
