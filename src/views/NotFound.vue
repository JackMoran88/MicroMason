<template>
    <div class="NotFound">
        <v-drop-catalog-main
                v-if="IS_DESKTOP"
                class="static"
        />
        <div class="NotFound__body">
            <v-title
                    text="Ошибка 404"
                    class="second"
            />
            <v-title
                    text="Страница не найдена"
            />
            <v-attention
                    text="Неправильно набран адрес или такой страницы на сайте
больше не существует"
            />
            <v-attention
                    text="Перейдите на главную страницу или выберите
подходящую категорию"
            />
        </div>
        <v-viewed-products/>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import vDropCatalogMain from '@/components/app/catalog/v-drop-catalog-main.vue';

export default {
  name: 'NotFound',
  components: {
    vDropCatalogMain,
  },
  computed: {
    ...mapGetters(['IS_DESKTOP']),
  },
  methods: {

  },
};
</script>

<style scoped lang="scss">

    .NotFound {
        width: 100%;
        height: 100%;
        display: flex;
        flex-wrap: wrap;

        &__body{
            margin: .5rem 0;
            >*{
                white-space: pre;
            }
            .second {
                color: var(--link-hover) !important;
                margin: 0 !important;
                font-size: 18px;
            }
            .attention{
                font-size: 16px;
            }
        }
        .v-viewed-products{
            width: 100%;
        }
    }

</style>
