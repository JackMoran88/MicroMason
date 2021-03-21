<template>
    <div class="v-available product__board border-0">
         <span class="v-available__type v-available__type__0" v-if="['0'].includes(Product.status)">
            <i>close</i>
            <span>Нет в налиичии</span>
        </span>
        <span class="v-available__type v-available__type__1" v-if="['1'].includes(Product.status)">
            <i>done</i>
            <span>Есть в наличии</span>
        </span>
        <span class="v-available__type v-available__type__2" v-if="['2'].includes(Product.status)">
            <i>schedule</i>
            <span>Ожидается</span>
        </span>
        <span class="v-available__type v-available__type__3" v-if="['3'].includes(Product.status)">
            <i>schedule</i>
            <span>Предзаказ</span>
        </span>
    </div>
</template>

<script>
export default {
  name: 'v-available',
  props: {
    Product: {
      // type: Object
    },
  },
  methods: {},
};
</script>

<style scoped lang="scss">

    i {
        @extend %_material-icons;
        font-size: 20px;

        margin-right: 5px;
    }

    .v-available {
        width: fit-content;
        display: inline-flex;
        flex-wrap: wrap;
        font-size: 14px;
        white-space: nowrap;

        margin-bottom: 0;

        &__type {
            padding: .25rem .5rem;
            border-radius: 6px;
            user-select: none;
            display: inline-flex;
            align-items: center;

            margin: .25rem 1rem;
            margin-left: 0;

            border: 1px solid;

            &__0 {
                color: gray;
                border-color: gray;
            }

            &__1 {
                color: var(--accent);
                border-color: var(--accent);
            }

            &__2 {
                color: #ffb432;
                border-color: #ffb432;
            }

            &__3 {
                color: #8400dc;
                border-color: #8400dc;
            }
        }
    }
</style>
