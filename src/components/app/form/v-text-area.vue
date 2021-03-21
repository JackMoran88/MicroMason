<template>
  <label class="w-100"> {{AreaTitle ? AreaTitle : ''}}
    <textarea
      class="form-control"
      name=""
      id=""
      :rows="AreaCols"
      @input="fAreaUpdate($event.target.value)"
      @blur="areaBlur"
      :placeholder="AreaPlaceholder"
    ></textarea>
  </label>
</template>

<script>
  export default {
    name: 'v-text-area',
    props: {
      AreaTitle: {
        type: String,
      },
      AreaModel: {
        type: String,
      },
      AreaId: {
        type: String,
      },
      AreaCols: {
        type: String,
      },
      AreaPlaceholder: {
        type: String,
        default: 'Введите текст',
      },
    },
    methods: {
      fAreaUpdate(value) {
        this.$emit('area', value);
        this.$emit('input', value);
      },
      areaBlur(){
        this.$emit('blur')
      }
    },
  };
</script>

<style scoped lang="scss">

  label {
    display: flex;
    flex-direction: column;

  }

  textarea {
    max-width: 100%;
    min-width: 100%;
    min-height: 32px;

    color: var(--text-main);
    background: var(--input-background);

    border: none;
    border-bottom: 1px solid var(--input-border);
    border-radius: 0;
    transition: none;

    &:focus {
      box-shadow: none !important;
      border-radius: 0;
      border-color: #e5e5e5;
    }

    &:hover {

    }

    &:focus {
      outline: none;
      color: var(--text-main);
      background: var(--background-content);
    }
  }

</style>
