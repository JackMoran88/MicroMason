<template>
    <div class="v-product-description" v-if="Product.description">
        <v-title
                text="Описание"
                type="second"
        >
            <span class="second">{{Product.name}}</span>
        </v-title>

        <read-more
                v-if="Product.description.length"
                :text="Product.description"
                :maxChars="500"
                moreStr="Читать дальше"
                lessStr="Свернуть"
        ></read-more>
    </div>
</template>

<script>
export default {
  name: 'v-product-description',
  props: {
    Product: {
      // type: Object
    },
  },
};
</script>

<style lang="scss">
    .v-product-description {
        margin: 1rem 0;
        max-width: 100%;
        > div {
            max-width: 100%;
            overflow: auto;
            *{
                max-width: 100%;
            }
        }
    }
</style>
