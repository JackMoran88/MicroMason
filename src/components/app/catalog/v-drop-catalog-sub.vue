<template>
    <div class="catalog__container">
        <div class="catalog__sub"
             v-for="Category in CATEGORIES.queryset" :key="Category.slug"
             v-show="currentCategory === Category.id"
             v-if="Category.children.length"
        >
            <ul class="catalog__sub-row catalog__sub-row__1">
                <ul class="catalog__sub-row-inner"
                    v-for="subCategory in Category.children" :key="subCategory.id"
                    v-if="subCategory.row === 1"
                >
                    <li class="catalog__sub-item">
                        <router-link
                                :to="{name: 'Category', params:{slug: subCategory.slug}}"
                        >
                            {{subCategory.name}}
                        </router-link>
                    </li>
                    <ul class="catalog__sub__sub">
                        <li
                                v-for="ssubCategory in subCategory.children" :key="ssubCategory.id"
                                class="catalog__sub__sub-item"
                        >
                            <router-link
                                    :to="{name: 'Category', params:{slug: ssubCategory.slug}}"
                            >
                                {{ssubCategory.name}}
                            </router-link>
                        </li>
                    </ul>
                </ul>
            </ul>

            <ul class="catalog__sub-row catalog__sub-row__2">
                <ul class="catalog__sub-row-inner"
                    v-for="subCategory in Category.children" :key="subCategory.id"
                    v-if="subCategory.row === 2"
                >
                    <li class="catalog__sub-item">
                        <router-link
                                :to="{name: 'Category', params:{slug: subCategory.slug}}"
                        >
                            {{subCategory.name}}
                        </router-link>
                    </li>
                    <ul class="catalog__sub__sub">
                        <li class="catalog__sub__sub-item"
                            v-for="ssubCategory in subCategory.children" :key="ssubCategory.id"
                        >
                            <router-link
                                    :to="{name: 'Category', params:{slug: ssubCategory.slug}}"
                            >
                                {{ssubCategory.name}}
                            </router-link>
                        </li>
                    </ul>
                </ul>
            </ul>

            <ul class="catalog__sub-row catalog__sub-row__3">
                <ul class="catalog__sub-row-inner"
                    v-for="subCategory in Category.children" :key="subCategory.id"
                    v-if="subCategory.row === 3"
                >
                    <li class="catalog__sub-item">
                        <router-link
                                :to="{name: 'Category', params:{slug: subCategory.slug}}"
                        >
                            {{subCategory.name}}
                        </router-link>
                    </li>
                    <ul class="catalog__sub__sub">
                        <li
                                class="catalog__sub__sub-item"
                                v-for="ssubCategory in subCategory.children" :key="ssubCategory.id"
                        >
                            <router-link
                                    :to="{name: 'Category', params:{slug: ssubCategory.slug}}"
                            >
                                {{ssubCategory.name}}
                            </router-link>
                        </li>
                    </ul>
                </ul>
            </ul>

        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { eventBus } from '@/main';

export default {
  name: 'v-drop-catalog-sub',
  data: () => ({
    Category: false,
    currentCategory: 1,
  }),
  methods: {},
  computed: {
    ...mapGetters(['CATEGORIES']),
  },
  mounted() {
    eventBus.$on('drop-category__current-category', (data) => {
      this.currentCategory = data;
    });
  },
};
</script>

<style scoped lang="scss">
    .catalog__sub {
        @include list-style-off;
        overflow-y: auto;
        z-index: 99;
        padding: 1rem .5rem;
        background: var(--background-light);
        width: 100%;
        height: 100%;
        display: flex;

        border-radius: 0 5px 5px 0;

        &-item {
            @include link;
            padding-top: .25rem;
        }

        &-row {
            width: calc(100% / 3);

            &-inner {
                padding: 0 .5rem !important;
            }
        }

        &__sub {
            display: flex;
            flex-direction: column;

            &-item {
                @include link($color: var(--text-main));
                font-size: 14px;
            }
        }
    }

</style>
