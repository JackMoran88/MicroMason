<template>
    <button
            class="btn btn-compare card-btn"
            :class="{'fill': COMPARE_IDS.includes(ProductId)}"
            @click="click"
    ></button>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'v-btn-compare',
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
    load() {

    },
    click() {
      if (this.COMPARE_IDS.includes(this.ProductId)) {
        this.DELETE_FROM_COMPARE(this.ProductId);
      } else {
        this.ADD_TO_COMPARE(this.ProductId);
      }
    },
    ...mapActions(['ADD_TO_COMPARE', 'DELETE_FROM_COMPARE']),
  },
  computed: {
    ...mapGetters(['COMPARE', 'COMPARE_IDS']),
  },
  mounted() {
    this.load();
  },
};
</script>

<style scoped lang="scss">
    button {
        z-index: 12;
    }
</style>
