<template>

    <section class="catalog">
        <div class="catalog__item"
             v-for="Category in listCategories" :key="Category.id"
             @click="showModalSubCatalog(Category.id, Category.name)"
        >
            <div class="catalog__item-img">
                <img v-lazy="$store.state.backendUrl + Category.main_image.card" :alt="Category.name">
            </div>
            <div class="catalog__item-title">
                <span> {{Category.name}}</span>
            </div>
        </div>

        <b-modal
                id="subCatalogModal"
                :title="curSubTitle"
                hide-footer
                centered
                v-model="isModalSubCatalogVisible"
        >
            <div slot="default">
                <ul @click="closeModalSubCatalog">
                    <li class="active">
                        <router-link
                                :to="{name: 'Category', params:{slug: curSubCatalog.slug}}"
                        >
                            Все {{curSubCatalog.name}}
                        </router-link>
                    </li>
                    <li
                            v-for="subCategory in curSubCatalog.children" :key="subCategory.name"
                    >
                        <router-link
                                :to="{name: 'Category', params:{slug: subCategory.slug}}"
                        >
                            {{subCategory.name}}
                        </router-link>
                    </li>
                </ul>
            </div>
        </b-modal>

    </section>

</template>

<script>

export default {
  name: 'catalog',
  props: {
    listCategories: {
      type: Array,
    },
  },
  data() {
    return {
      isModalSubCatalogVisible: false,

      curSubCatalog: 0,
      curSubTitle: 'Каталог',
    };
  },
  components: {},
  methods: {
    closeModalSubCatalog() {
      this.isModalSubCatalogVisible = false;
      this.$bvModal.hide('catalogModal');
    },
    showModalSubCatalog(id, title) {
      this.isModalSubCatalogVisible = true;
      this.curSubTitle = title;
      this.curSubCatalog = this.listCategories[this.listCategories.findIndex((category) => category.id === id)];
    },
  },
};
</script>

<style scoped lang="scss">
    @include list-style-off;

    .catalog {
        display: flex;
        flex-wrap: wrap;
        width: 100%;
        height: fit-content;
        padding: 1rem 0;
        background: var(--background-light);

        &__item {
            height: auto;
            padding: .25rem;
            border: 1px solid var(--background-content);

            &-img {
                display: flex;
                justify-content: center;

                img {
                    max-width: 90%;
                    max-height: 90%;
                }
            }

            &-title {
                @include link();
                @include fz(16);
                text-align: center;
                padding: .25rem 0;
            }

        }
    }

    @media (min-width: 1200px) {
        .catalog__item {
            max-width: 182px;
            min-width: 182px;
        }
    }

    @media (max-width: 1200px) {
        .catalog__item {
            max-width: 25%;
            min-width: 25%;
        }
    }

    @media (max-width: 1200px) and (min-width: 768px) {
        .catalog__item {
            max-width: 33.3%;
            min-width: 33.3%;
        }
    }

    @media (max-width: 768px) {
        .catalog__item {
            max-width: 50%;
            min-width: 50%;
        }
    }

    @media (max-width: 360px) {
        .catalog__item {
            max-width: 100%;
            min-width: 100%;
        }
    }

    ul {
        padding: 0;

        li {
            @include fz(18);
            @include link;
            border-bottom: 1px solid var(--background-content);
            border-top: 1px solid var(--background-content);
            padding: .5rem .25rem;

            &.active {
                //border-color: var(--accent);
                @include link($color: var(--accent));
                margin: .25rem 0;
            }
        }
    }

</style>
