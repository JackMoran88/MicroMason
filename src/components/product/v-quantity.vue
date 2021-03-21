<template>
  <div class="quantity">
    <i class="quantity__minus"
       @click="qtyMinus"
       :class="{disabled : qty<=1 }"
    >remove</i>
    <input
      type="number"
      class="quantity__qty"
      v-model="qty"
      :max="qty_max"
      @blur="getValue"
      @keyup.enter="getValue"
    >
    <i class="quantity__plus" @click="qtyPlus">add</i>
  </div>
</template>

<script>
export default {
  name: 'v-quantity',
  props: {
    Qty: {
      type: Number,
    },
  },
  data() {
    return {
      qty: 1,
      qty_min: 1,
      qty_max: 100,
    };
  },
  methods: {
    qtyPlus() {
      if (this.qty < this.qty_max) {
        this.qty++;
        this.getValue();
      }
    },
    qtyMinus() {
      if (this.qty > this.qty_min) {
        this.qty--;
        this.getValue();
      }
    },
    getValue() {
      this.$emit('value', this.qty);
    },
  },
  created() {
    this.qty = this.Qty;
  },
};
</script>

<style scoped lang="scss">
  .quantity {
    display: flex;
    //border: 1px solid var(--background-light);
    border-radius: 4px;
    padding: .2rem;
    height: 30px;

    &__minus, &__plus {
      @extend %_material-icons;
      display: flex !important;
      justify-content: center;
      align-items: center;
      font-size: 20px;
      width: 40px;
      cursor: pointer;
      user-select: none;
      color: var(--text-main);

      &.disabled {
        color: var(--text-main);
      }

    }

    &__minus {

    }

    input {
      border: none;
      border-right: 1px solid var(--background-light);
      border-left: 1px solid var(--background-light);
      max-width: 50px;
      text-align: center;
      background: transparent;
      color: var(--text-main);
      /* Chrome, Safari, Edge, Opera */
      &::-webkit-outer-spin-button,
      &::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }

      /* Firefox */
      &[type=number] {
        -moz-appearance: textfield;
      }
    }

    &__plus {

    }
  }
</style>
