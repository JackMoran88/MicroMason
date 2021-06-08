<template>
  <div class="v-custom-products-line"

  >
    <v-title
      :text="title"
      type="second"
      v-if="data && data.length >= minCount"
    />
    <v-card-line
      :Products="data"
      :preloading="preloading"
    />
  </div>
</template>

<script>
  import vCardLine from '@/components/app/container/v-card-line';

  export default {
    name: 'v-custom-products-line',
    components: {
      vCardLine,
    },
    props: {
      data: {
        type: Array,
      },
      title: {
        type: String,
      },
      preloading:{
        type: Boolean,
        default: false,
      },
      minCount: {
        type: Number,
        default: 1,
      }
    },
    methods: {},
    computed: {},
    mounted() {
    },
    watch: {},
  };
</script>

<style scoped lang="scss">

  .v-custom-products-line {
    width: 100%;
    max-width: 100%;
    margin-top: 2rem;
  }

</style>
