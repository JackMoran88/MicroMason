<template>
    <div class="v-loading" v-show="LOADING">
        <span></span>
    </div>
</template>

<script>
import {
  mapGetters, mapActions, mapMutations, mapState,
} from 'vuex';

export default {
  name: 'v-loading',
  data() {
    return {
      axiosInterceptor: null,
    };
  },
  methods: {
    closeAnimation() {
      setTimeout(() => {
        this.SET_LOADING(false);
      }, 300);
    },
    enableInterceptor() {
      const th = this;
      this.axiosInterceptor = this.$axios.interceptors.request.use((config) => {
        th.SET_LOADING(true);
        return config;
      }, (error) => {
        th.closeAnimation();
        return Promise.reject(error);
      });
      this.$axios.interceptors.response.use((response) => {
        th.closeAnimation();
        return response;
      }, (error) => {
        th.closeAnimation();
        return Promise.reject(error);
      });
    },

    disableInterceptor() {
      window.axios.interceptors.request.eject(this.axiosInterceptor);
    },
    ...mapMutations(['SET_LOADING']),
  },
  computed: {
    ...mapGetters(['LOADING']),
  },
  mounted() {
    this.enableInterceptor();
  },
};
</script>

<style scoped lang="scss">

    .v-loading {
        z-index: 9999999;
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        height: 5px;
        width: 100%;

    }

    .v-loading {
        > span {
            background: var(--accent);

            height: 100%;
            width: calc(100% / 5);

            bottom: 0;
            position: absolute;
            -webkit-animation: linear infinite;
            -webkit-animation-name: run;
            -webkit-animation-duration: 2s;
        }
    }

    @-webkit-keyframes run {
        0% {
            left: 0;
            border-radius: 0;
        }
        50% {
            left: calc(100% - 100% / 5);
            border-radius: 5rem;
        }
        100% {
            left: 0;
            border-radius: 0;
        }
    }

</style>
