<template>
    <button
            class="btn btn-wish card-btn"
            :class="{'fill': WISH_IDS && WISH_IDS.includes(ProductId)}"
            @click="click"
    ></button>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'v-btn-wish',
  components: {},
  data() {
    return {};
  },
  props: {
    ProductId: {
      type: Number,
    },
  },
  methods: {
    click() {
      if (this.WISH_IDS && this.WISH_IDS.includes(this.ProductId)) {
        this.DELETE_WISH(this.ProductId);
      } else {
        this.ADD_WISH(this.ProductId);
      }
    },
    ...mapActions(['ADD_WISH', 'DELETE_WISH']),
  },
  computed: {
    ...mapGetters(['WISH_IDS', 'IS_LOGGED_IN', 'authStatus']),
  },
};
</script>

<style scoped lang="scss">
    button {
        z-index: 12;
    }
</style>
