<template>
  <section class="footer">
    <div class="footer__inner conteiner">
      <ul class="footer__row" v-for="col in FOOTER">
        <li class="footer__item-header">{{col.header}}</li>
        <li class="footer__item" v-for="item in col.items">
          <!--     Local links     -->
          <router-link :to="item.link.href" v-if="item.link && item.link.type === 'local'">
            <font-awesome-icon v-if="item.icon" :icon="item.icon.icon"
                               :style="{ color: item.icon.color }"/>
            {{item.name}}
          </router-link>
          <!--    Global links     -->
          <a :href="item.link.href" v-if="item.link && item.link.type === 'global'">
            <font-awesome-icon v-if="item.icon" :icon="item.icon.icon"
                               :style="{ color: item.icon.color }"/>
            {{item.name}}
          </a>
          <!--    Modals      -->
          <div v-else-if="item.click" @click="showInfo(item.click.name, item.click.description)">
            <font-awesome-icon v-if="item.icon" :icon="item.icon.icon"
                               :style="{ color: item.icon.color }"/>
            {{item.name}}
          </div>
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
  import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

  import {library} from "@fortawesome/fontawesome-svg-core";
  import {faInstagram, faTelegram, faYoutube} from '@fortawesome/free-brands-svg-icons';

  library.add(faInstagram, faYoutube, faTelegram);

  export default {
    name: 'v-footer',
    components: {
      FontAwesomeIcon
    },
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
      loadData() {
        if (!this.SETTINGS.footer) {
          return
        }
        this.FOOTER.col1.items = []
        this.SETTINGS.footer.forEach((value) => {
          this.FOOTER.col1.items.push({
            name: value.name,
            click: {name: value.name, description: value.description}
          },)
        })
        this.loadSocial()
      },
      loadSocial() {
        let items = this.FOOTER.col3.items
        this.$search_by(items, 'name', 'Instagram').link = {
          type: 'global',
          href: this.SETTINGS.instagram
        }
        this.$search_by(items, 'name', 'Youtube').link = {
          type: 'global',
          href: this.SETTINGS.youtube
        }
        this.$search_by(items, 'name', 'Telegram').link = {
          type: 'global',
          href: this.SETTINGS.telegram
        }
      }
    },
    computed: {
      ...mapGetters(['SETTINGS', 'FOOTER']),
    },
    mounted() {
      this.loadSocial()
    },
    watch: {
      'SETTINGS'() {
        this.loadData()
      }
    }
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
        @include fz(30px);
      }

      @include link($color: var(--text-second));
    }

  }

  //!Footer!
</style>
