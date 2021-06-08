<template>
  <div
    id="v-slider"
    class="slider"

  >
    <skeleton-loading
      v-if="!SLIDERS.load"
    >
      <square-skeleton
        :count="1"
        :boxProperties="{height: '400px'}"
      >
      </square-skeleton>
    </skeleton-loading>

    <b-carousel
      v-for="slider in SLIDERS.queryset"
      v-if="SLIDERS.load && slider.place === place"
      id="carousel-1"
      :interval="speed"
      controls
      background="white"
      :key="slider.id"
      :img-width="slider.width"
      :img-height="slider.height"
    >
      <router-link
        v-for="slide in slider.slides" :key="slide.id"
        :to="slide.url"
        class="link"
        role="listitem"
      >
        {{slider.place }}
        <b-carousel-slide
          :img-src="$store.state.backendUrl + slide.image[crop]"
          :img-alt="slide.title"
        ></b-carousel-slide>
      </router-link>
    </b-carousel>

  </div>

</template>

<script>
  import {mapGetters} from 'vuex';

  export default {
    name: 'v-slider',
    components: {},
    props: {
      place: {
        type: String,
        default: 'home',
      },
      speed: {
        type: Number,
        default: 5000,
      },
      crop: {
        type: String,
        default: 'full',
      },

    },
    data() {
      return {
        value: 0,
      };
    },
    methods: {},
    computed: {
      ...mapGetters(['SLIDERS']),
    },
    created() {
    },
    mounted() {

    },
  };
</script>

<style scoped lang="scss">

  #v-slider {
    margin: 1rem 0;
    width: 100%;

    a.link {
      color: transparent;
    }
  }

</style>
