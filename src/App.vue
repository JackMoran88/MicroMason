<template>
  <div id="app">
    <transition name="fade">
      <component :is="layout">
        <router-view/>
      </component>
    </transition>
  </div>
</template>

<script>
  import {mapActions, mapGetters} from 'vuex';
  import MainLayout from '@/layouts/MainLayout.vue';
  import EmptyLayout from '@/layouts/EmptyLayout.vue';


  export default {
    components: {
      MainLayout, EmptyLayout,
    },
    methods: {
      ...mapActions(['START']),
    },
    computed: {
      layout() {
        return `${this.$route.meta.layout || 'main'}-layout`;
      },
      ...mapGetters(['SETTINGS']),
    },
    mounted() {
      this.START()
    },
    watch: {
      '$route.path'() {
        this.$scrollToTop();
      },
    },
    metaInfo() {
      let data
      if (this.SETTINGS && this.SETTINGS.meta_description) {
        let description = this.SETTINGS.meta_description
        let {title} = this.SETTINGS;
        data = {
          title: 'MicroMason',
          meta: [
            {
              vmid: 'description',
              name: 'description',
              property: 'description',
              content: description
            },
            {
              vmid: 'og:description',
              name: 'description',
              property: 'og:description',
              content: description
            },
            {vmid: 'og:title', property: 'og:title', content: title},
          ],
        };
      }
      return data
    },
  };
</script>

<style lang="scss">
  $pretty--color-primary: #424e65;
  html {
    overflow-x: hidden;
  }

  #app {
    min-height: 100%;
    height: 100%;
  }

  body {
    @extend %_font;

    & {
      color: var(--text-main);
    }
  }

  .disabled {
    &, * {
      color: var(--text-second);
    }
  }

  *:focus {
    outline: none !important;
  }

</style>
