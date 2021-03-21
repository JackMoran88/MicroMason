<template>
  <div class="v-select">
    <v-title-small
      v-if="text"
      :text="text"
    />
    <div class="v-select__body">
      <select @change="change(value)" v-model="value">
        <option
          v-if="options.length"
          v-for="option in options" :key="option.id" :value="option.id"
        >{{option.name}}
        </option>
        <slot></slot>
      </select>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'v-select',
    props: {
      options: {
        type: Array,
        default: () => [],
      },
      model: {
        type: Number,
      },
      current: {
        type: Number,
      },
      text: {
        type: String,
      },
    },
    data() {
      return {
        value: 0,
        isOpen: true,
      };
    },
    methods: {
      start() {
        if (this.options.length) {
          this.value = this.options[0].id;
        }
        if (this.current) {
          this.value = this.current;
        }
      },
      toggle() {
        this.isOpen = !this.isOpen;
      },
      change(value) {
        this.$emit('selected', value);
        this.$emit('input', value);
      },
      setValue(value) {
        this.value = value;
      },
    },
    created() {
      this.start();
    },
  };
</script>

<style scoped lang="scss">

  .v-select {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: auto;
    align-self: flex-end;

    color: var(--text-main);

    &__body {
      display: flex;
      align-items: center;
      position: relative;

      select {
        border-radius: 4px;
        border-color: var(--background-light-second);
        padding: .2rem .7rem;
        appearance: none;
        z-index: 2;
        background: transparent;
        padding-right: 30px;
        width: 100%;
        cursor: pointer;

        color: var(--text-main);
        option{
          background: var(--background-content);
        }
      }

      &:after {
        @extend %_material-icons;
        font-size: 26px;
        content: 'keyboard_arrow_down';
        margin: 0 .15rem;
        position: absolute;
        top: 0;
        right: 0;
        z-index: 0;
        color: var(--link);
        vertical-align: middle;
        align-self: center;
        padding-top: 3px;
      }
    }

  }

</style>
