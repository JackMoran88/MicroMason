<template>
<!--    <transition name="fade">-->
        <div id="v-drop-catalog" class="catalog" v-show="isOpen">
            <div class="catalog__backdrop"
                 @click="isOpen = false"
                 @mouseover="isOpen = false"
            ></div>
            <v-drop-catalog-main/>
            <v-drop-catalog-sub/>
        </div>
<!--    </transition>-->
</template>

<script>
import { eventBus } from '@/main';
import vDropCatalogMain from '@/components/app/catalog/v-drop-catalog-main.vue';
import vDropCatalogSub from '@/components/app/catalog/v-drop-catalog-sub.vue';

export default {
  name: 'v-drop-catalog',
  components: {
    vDropCatalogMain, vDropCatalogSub,
  },
  data: () => ({
    isOpen: false,
  }),
  methods: {
  },
  computed: {},
  mounted() {
    eventBus.$on('toggleCategory', () => {
      this.isOpen = !this.isOpen;
    });
    eventBus.$on('drop-category__open', () => {
      this.isOpen = true;
    });
    eventBus.$on('drop-category__close', () => {
      this.isOpen = false;
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth <= 992) {
        eventBus.$emit('drop-category__close');
      }
    });
  },
  watch: {
    $route() {
      eventBus.$emit('drop-category__close');
    },
  },
};
</script>

<style lang="scss" scoped>

    .catalog {
        @include list-style-off;
        padding-right: 30px;
        position: absolute;
        width: 100%;
        height: 65vh;
        max-height: 65vh;
        display: grid;
        grid-template-columns: 300px auto;
        top: -.5rem;

        > * {
            height: 100%;
        }

        &__container {
            z-index: 99;
            height: 65vh;
        }

        &__backdrop {
            position: fixed;
            top: 0;
            left: 0;
            z-index: 30;
            height: 100%;
            width: 100%;
            background: rgba(black, .5);
        }

    }

</style>
