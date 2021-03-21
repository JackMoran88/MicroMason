<template>
    <paginate
            v-if="PageCount"
            :page-count="PageCount"
            :clickHandler="selectPage"
            v-model="current"
            :prev-text="'keyboard_arrow_left'"
            :next-text="'keyboard_arrow_right'"
            prev-link-class="prev"
            next-link-class="next"
            :container-class="'paginate'">
    </paginate>
</template>

<script>
export default {
  name: 'v-paginate',
  props: {
    PageCount: {
      type: Number,
    },
    Link: {
      type: String,
    },
    Data: {
      type: Object,
    },
    CurrentPage: {
      type: Number,
    },
    Current: {
      type: Number,
    },
  },
  data() {
    return {
      current: this.CurrentPage,
    };
  },
  methods: {
    selectPage(page) {
      page = parseInt(page);
      this.$router.push({ query: { ...this.$route.query, page } });
      this.current = page;
    },
  },
  mounted() {
    if (this.$route.query.page) {
      this.selectPage(this.$route.query.page);
    }
  },
  watch: {
    $router() {
      if (this.$route.query.page) {
        this.selectPage(this.$route.query.page);
      }
    },
    Current() {
      // После фильтрации, продукт может быть не найден на страничке, поэтому мы забираем страницу с реквеста
      if (this.$route.query.page && this.$route.query.page !== this.Current) {
        this.$change_query_url({ page: this.Current });
        this.current = this.Current;
      }
    },
  },
};
</script>

<style lang="scss">

    .paginate {
        padding: 0;
        margin: 1rem 0;
        list-style: none;
        display: flex;
        width: 100%;
        justify-content: center;

        li {
            color: var(--link);
            /*padding: .75rem 1rem;*/
            margin: 0 .25rem;
            border: 1px solid var(--text-muted);
            border-radius: 12px;
            cursor: pointer;
            height: 50px;
            width: 50px;

            a {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                height: 100%;
                user-select: none;
            }

            .next, .prev{
                @extend %_material-icons;
                display: flex;
                font-size: 24px;
            }

            &:hover {
                border: 1px solid var(--link);
                color: var(--link);
            }

            &.active {
                color: var(--accent);
                border: 1px solid var(--accent);
            }

            &.disabled {
                color: var(--background-light-accent) !important;

                &:hover {
                    border: 1px solid var(--text-muted);
                    color: var(--text-muted);
                }
            }
        }
    }

</style>
