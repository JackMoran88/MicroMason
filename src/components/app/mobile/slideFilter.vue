<template>
  <div>
    <b-sidebar
      id="mobileFilter"
      shadow
      backdrop
      no-header
      no-close-on-route-change
      :right="true"
      #default="{ hide }"
    >

      <v-filter-board>
        <div slot="header" class="d-flex pb-1">
          <v-title
            text="Фильтр"
            type="second"
            class="mt-0"
          />
          <i @click="hide">close</i>
        </div>
      </v-filter-board>
      <v-btn
        BtnName="Очистить"
        BtnStyle="item"
        style="color: red; width: 100%; margin-top: 1rem"
        @click.native="clearFilters"
      />
    </b-sidebar>
  </div>
</template>

<script>
  import {eventBus} from '@/main';
  import {
    mapGetters, mapActions, mapMutations, mapState,
  } from 'vuex';
  import vFilterBoard from '@/components/app/container/v-filter-board';

  export default {
    name: 'slideFilter',
    props: {
      menu: {
        type: Function,
      },
    },
    components: {
      vFilterBoard,
    },
    methods: {
      logout() {
        this.$store.dispatch('LOGOUT');
      },
      clearFilters() {
        this.CLEAR_CHOICE_FILTER()
         this.$router.replace({query: null}).catch(() => {
        })
        this.$update_query_url()
      },
      ...mapMutations(['CLEAR_CHOICE_FILTER'])
    },
    computed: {
      ...mapGetters(['IS_LOGGED_IN']),
    },
    mounted() {

    },
  };
</script>

<style lang="scss">

  #mobileFilter {
    i {
      color: var(--modal-close);
      @extend %_material-icons;
      font-size: 24px;
    }

    z-index: 45;
    @include list-style-off;

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: .5rem 0;

      strong {
        @include fz(34px);
      }
    }

    .b-sidebar-body {
      padding: 1rem;
      background: var(--background-content);
      color: var(--text-main);
    }

  }
</style>
