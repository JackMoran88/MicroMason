<template>
    <div
            id="v-slider"
            class="slider"
            v-if="SLIDERS.length"
    >
        <b-carousel
                id="carousel-1"
                :interval="speed"
                controls
                indicators
                background="white"
                v-for="slider in SLIDERS"
                :key="slider.id"
                v-if="slider.place === place"
        >
            <router-link
                    v-for="slide in slider.slides" :key="slide.id"
                    :to="slide.url"
            >
                <b-carousel-slide
                        :img-src="$store.state.backendUrl + slide.image[crop]"
                        :img-alt="slide.title"
                ></b-carousel-slide>
            </router-link>
        </b-carousel>

    </div>

</template>

<script>
import { mapGetters } from 'vuex';

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

    #v-slider{
        margin: 1rem 0;
        width: 100%;
    }

</style>
