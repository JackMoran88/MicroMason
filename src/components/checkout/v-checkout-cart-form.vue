<template>
    <v-account-form
        :actions="false"
    >
        <div slot="header">
            <div class="form__title"><span>local_shipping</span>Ваш заказ</div>
        </div>
        <div slot="body">
            <v-cart
                    :checkout="true"
            />
        </div>
    </v-account-form>
</template>

<script>
import vAccountForm from '@/components/app/form/v-account-form';
import vCart from '@/components/app/cart/v-cart';

export default {
  name: 'v-checkout-cart-form',
  props: {},
  components: { vAccountForm, vCart },
};
</script>

<style scoped>

</style>
