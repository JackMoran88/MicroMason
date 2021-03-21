<template>
  <section class="footer">
    <div class="footer__inner conteiner">


      <ul class="footer__row" v-if="SETTINGS.footer && SETTINGS.footer.length">
        <li class="footer__item-header">Информация</li>
        <li class="footer__item"
            v-for="item in SETTINGS.footer" :key="item.id"
            @click="showInfo(item.name, item.description)"
        >
          <a>{{item.name}}</a>
        </li>
      </ul>
      <ul class="footer__row">
        <li class="footer__item-header">Помощь</li>
        <li class="footer__item"><a href="">Мои заказы</a></li>
        <li class="footer__item"><a href="">Рассылка</a></li>
        <li class="footer__item"></li>
        <li class="footer__item"><a href="">Мои отзывы</a></li>
      </ul>
      <ul class="footer__row">
        <li class="footer__item-header">Наши соцсети</li>
        <li class="footer__item">
          <a :href="SETTINGS.instagram">
            <font-awesome-icon :icon="['fab', 'instagram']" :style="{ color: '#A42A9E' }"/>
            Instagram</a>
        </li>
        <li class="footer__item">
          <a :href="SETTINGS.youtube">
            <font-awesome-icon :icon="['fab', 'youtube']" :style="{ color: '#FF0000' }"/>
            YouTube</a>
        </li>
        <li class="footer__item">
          <a :href="SETTINGS.telegram">
            <font-awesome-icon :icon="['fab', 'telegram']" :style="{ color: '#2CA3E0' }"/>
            Telegram</a>
        </li>
      </ul>
    </div>
    <b-modal
      id="infoModal"
      :title="infoModal.name"
      hide-footer
      centered
    >
      <div
        slot="default"
        v-html="infoModal.description"></div>
    </b-modal>
  </section>

</template>

<script>
  import {mapGetters} from 'vuex';

  export default {
    name: 'v-footer',
    data() {
      return {
        infoModal: {
          name: null,
          description: null,

        },
      };
    },
    methods: {
      showInfo(name, description) {
        this.infoModal.name = name;
        this.infoModal.description = description;
        this.$bvModal.show('infoModal');
      },
    },
    computed: {
      ...mapGetters(['SETTINGS']),
    },
  };
</script>

<style lang="scss">
  html, body {
    height: 100%;
  }

  body {
    height: 100%;
    min-height: 100%;
    overflow-x: initial;
  }

  .page {
    min-height: 100%;
    display: grid;
    grid-template-columns: 100%;
    grid-template-rows: min-content auto min-content;

    &__wrapper {
      padding: 1rem 0;
      display: grid;
      grid-template-rows: auto;
      justify-self: center;
    }
  }

  //Footer
  .footer {
    &__inner {
      display: flex;
      justify-content: space-around;
      flex-wrap: wrap;

      background: var(--background-dark);
      color: white;
      padding: 1.25rem;
      margin-top: 7rem;
    }

    @include list-style-off;

    &__row {
      margin: 0;
      padding: .4rem 0 !important;
      flex-direction: column;
      width: calc(100vh / 3);
    }

    &__item {
      &-header {
        width: 100%;
      }

      &-brand {
        @include fz(30);
      }

      @include link($color: var(--text-second));
    }

  }

  //!Footer!
</style>
