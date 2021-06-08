<template>
  <div class="v-viewed-products">
    <v-title
      text="Просмотренные товары"
      type="second"
      v-if="VIEWED.load && VIEWED.queryset.length"
    />
    <v-card-line
      :Products="VIEWED.queryset"
      :preloading="!VIEWED.load"
    />
  </div>
</template>

<script>
  import vCardLine from '@/components/app/container/v-card-line';
  import {mapGetters, mapActions, mapMutations} from 'vuex';

  export default {
    name: 'v-viewed-products',
    components: {
      vCardLine,
    },
    methods: {
      load() {
        if (this.VIEWED_IDS && this.VIEWED_IDS.length) {
          this.GET_PRODUCTS_BY_IDS(this.VIEWED_IDS).then((data) => {
            this.SET_VIEWED_TO_STATE(data);
          });
        } else {
          //  VIEWED_IDS EMPTY, turn off preloader
          this.SET_VIEWED_TO_STATE([])
        }
      },
      ...mapActions(['GET_PRODUCTS_BY_IDS']),
      ...mapMutations(['SET_VIEWED_TO_STATE', 'SET_VIEWED_IDS_TO_STATE']),
    },
    computed: {
      ...mapGetters(['VIEWED', 'VIEWED_IDS']),
    },
    mounted() {
      this.load();
    },
    watch: {
      VIEWED_IDS() {
        this.load();
      },
    },
  };
</script>

<style scoped lang="scss">

  .v-viewed-products {
    width: 100%;
    max-width: 100%;
    margin-top: 2rem;
  }

</style>
