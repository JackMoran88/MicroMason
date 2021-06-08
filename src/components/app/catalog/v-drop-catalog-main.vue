<template>
  <div class="catalog__container catalog__main" :class="{'full-border': fullBorder}">
    <ul>

      <skeleton-loading
        v-if="!CATEGORIES.load"
      >
        <square-skeleton
          :count="10"
          :boxProperties="{height: '24px',bottom: '8px',}"
          class="catalog__main-item"
        >
        </square-skeleton>
      </skeleton-loading>


      <li
        class="catalog__main-item"
        v-for="Category in CATEGORIES.queryset" :key="Category.slug"
      >
        <router-link
          :to="{name: 'Category', params:{slug: Category.slug}}"
          @mouseover.native="timerOn(Category.id, Category.children)"
          @mouseout.native="timerOff()"
        >
          {{Category.name}}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
  import {mapActions, mapGetters} from 'vuex';
  import {eventBus} from '@/main';

  let timer = 0;

  export default {
    name: 'v-drop-catalog-main',
    data: () => ({
      fullBorder: false,
    }),
    methods: {
      load() {
        // if (this.CATEGORIES.length){
        //   this.$debug_log('Категория не пуста')
        //   return
        // }
        //
        // this.$debug_log('Категория ПУСТА')
        // this.$debug_log(this.CATEGORIES.length)
        // this.GET_CATEGORY_LIST().then(() => {
        //   this.curCategory(this.CATEGORIES[0].id, 0);
        // });
      },
      timerOn(id, children) {
        if (children.length === 0) {
          this.fullBorder = true;
        } else {
          this.fullBorder = false;
        }
        timer = window.setTimeout(this.curShow, 400);
        this.curCategory(id, children);
      },
      timerOff() {
        if (timer) window.clearTimeout(timer);
      },

      curShow() {
        eventBus.$emit('drop-category__open');
      },
      curCategory(id) {
        eventBus.$emit('drop-category__current-category', id);
      },

      ...mapActions(['GET_CATEGORY_LIST']),
    },
    computed: {
      ...mapGetters(['CATEGORIES']),
    },
    mounted() {
      this.load()
    },
    beforeDestroy() {
      this.timerOff();
    },
    watch: {
      $route() {
        this.isOpen = false;
      },
      'CATEGORIES.queryset'() {
        this.curCategory(this.CATEGORIES.queryset[0].id, 0)
      }
    },
  };
</script>

<style scoped lang="scss">

  .catalog__main {
    @include list-style-off;
    background: var(--background-light-second);
    min-width: 300px;
    position: relative;
    border-radius: 5px 0 0 5px;

    padding: 1rem 0;

    &.full-border {
      border-radius: 5px;
    }

    &.static {
      height: 65vh;
      margin-right: 1rem;
      background: none;
      padding: 0;

      &:before {
        display: none;
      }
    }

    &:before {
      display: inline-block;
      position: absolute;
      top: -10px;
      right: 0px;
      z-index: 99;
      width: 0;
      height: 0;
      border-style: solid;
      border-width: 0 20px 20px;
      border-color: transparent transparent var(--background-light-second);
      -webkit-transition: opacity .5s ease-in-out;
      -o-transition: opacity .5s ease-in-out;
      transition: opacity .5s ease-in-out;
      content: "";
    }

    ul {
      padding: 0 1rem;

      li {
        @include link;
        margin: .5rem .25rem;
        white-space: nowrap;

        a {

        }
      }
    }
  }

</style>
