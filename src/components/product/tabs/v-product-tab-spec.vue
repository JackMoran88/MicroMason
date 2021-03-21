<template>
    <div class="v-product-tab-spec product__board product__board__diff-padding">
        <div class="product__board__header">Характеристики</div>
        <table class="product__board__body table">
            <tr
                v-for="spec in ProductSpecs" :key="spec.id"
                v-if="spec.name"
            >
                <td><span>{{spec.parameter_name}}</span></td>
                <td><span>{{spec.name}}</span></td>
            </tr>
            <tr v-if="ProductSpecs.length === 0">
                <td><span>Характеристик не найдено</span></td>
            </tr>
        </table>
    </div>

</template>

<script>
export default {
  name: 'v-product-tabs-spec',
  props: {
    ProductSpecs: Array,
  },
  components: {},
};
</script>

<style scoped lang="scss">

    table{
        overflow: hidden;
        tr{
            td:first-of-type{
                font-weight: 500;
                width: 40%;
                max-width: 40%;
                min-width: 40%;
            }
            td:last-of-type{
                display: flex;
                flex-direction: column;
                width: 100%;
                max-width: 100%;
                min-width: 100%;
                span{

                }
            }
            &:nth-child(even){
                background: var(--background-content);
                border-right: 1px solid white;
                border-left: 1px solid white;
            }
        }
    }

</style>
