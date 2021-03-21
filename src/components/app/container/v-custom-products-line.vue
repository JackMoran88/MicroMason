<template>
  <div class="v-custom-products-line"
       v-if="data && data.length >= minCount"
  >
    <v-title
      :text="title"
      type="second"
    />
    <v-card-line
      :Products="data"
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
