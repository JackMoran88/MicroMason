<template>
  <v-account-form
    @toggle="close"
    :actions="false"
    :state="true"
  >
    <div slot="header">
      <div class="form__title"><span>local_shipping</span>Способ доставки</div>
    </div>
    <div slot="body">
      <v-select
        v-if="SHIPPING.length > 0"
        placeholder="Служба доставки"
        @option:selected="changeShipping"
        ref="address_selector"
        :options="shipping_options"
        :clearable="false"
        :value="$search_by(shipping_options, 'value', curShipping)"
      />

      <v-select
        v-if="branches && branches.length > 0 && CHECKOUT.shipping"
        placeholder="Отделение"
        @option:selected="changeBranch"
        :options="branch_options"
        :clearable="false"
        autocomplete="on"
      />


    </div>

  </v-account-form>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import vAccountForm from '@/components/app/form/v-account-form';

export default {
  name: 'v-checkout-shipping-form',
  components: {
    vAccountForm,
  },
  data() {
    return {
      curShipping: '',
      curBranch: 0,
      branches: [],

      shipping_options: [],
      branch_options: [],
    };
  },
  methods: {
    load() {
      this.GET_SHIPPING().then(() => {
        if (this.SHIPPING.length) {
          this.loadShippingOptions()
        }
      });
      this.getBranches();
    },
    getBranches() {
      if (!this.ADDRESS[0]) {
        return;
      }
      this.GET_BRANCH_BY_QUERY(this.ADDRESS[0].city).then((response) => {
        this.branches = [];
        if (response.length > 0) {
          response.forEach((value, index) => {
            this.branches.push({ id: index, name: value.description });
          });
          this.loadBranchOptions()
        }
      });
    },
    changeShipping(select) {
      this.curShipping = select.value;
      this.SET_CHECKOUT_SHIPPING(this.curShipping)
    },
    changeBranch(select) {
      this.curBranch = select.value;
       this.SET_CHECKOUT_BRANCH(select.label)
    },
    close() {
      this.load();
    },
    loadShippingOptions(){
      this.shipping_options = this.SHIPPING.map((value)=>{
        return {
            label: `${value.name}`,
            value: value.id
          }
      })
    },
    loadBranchOptions(){
      this.branch_options = this.branches.map((value)=>{
        return {
            label: `${value.name}`,
            value: value.id
          }
      })
    },
    ...mapActions(['GET_SHIPPING', 'GET_BRANCH_BY_QUERY']),
    ...mapMutations(['SET_CHECKOUT_BRANCH', 'SET_CHECKOUT_SHIPPING', 'SET_CHECKOUT_ADDRESS', ]),
  },
  computed: {
    ...mapGetters(['SHIPPING', 'ADDRESS', 'CHECKOUT']),
  },
  mounted() {
    this.load();
  },
  watch: {
    ADDRESS() {
      this.getBranches();
    },
  },
};
</script>

<style scoped lang="scss">
  .v-select {
    margin: .5rem 0;
  }
</style>
