<template>
  <div class="v-filter-container">
    <div class="v-filter-container-header"
         @click="toggle"
    >
      <v-title-small
        :text="name"
      />
      <i>{{isOpen ? 'keyboard_arrow_up':'keyboard_arrow_down'}}</i>
    </div>
    <div class="v-filter-container-body" v-show="isOpen">
      <slot name="default"></slot>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'v-filter-container',
    props: {
      name: {
        type: String,
        default: 'Фильтр',
      },
      length: {
        type: Number,
        default: 0,
      },
    },
    data() {
      return {
        isOpen: true,
      };
    },
    methods: {
      open() {
        this.isOpen = true;
      },
      close() {
        this.isOpen = false;
      },
      toggle() {
        this.isOpen = !this.isOpen;
      },
    },
    mounted() {
      if (this.length > 10) {
        this.close();
      }
    },
  };
</script>

<style lang="scss">

  .v-filter-container {
    i {
      @extend %_material-icons;
      font-size: 24px;
    }

    &-header {
      display: flex;
      align-items: center;
      cursor: pointer;
    }

    &-body {
      .v-filter-multiply {
        max-height: 500px;
        overflow-y: auto;
      }
    }

    .v-title-small {
      color: var(--text-main);
      @include link($hover: none);
    }

    label.v-input {
      color: var(--text-second);
    }
  }

</style>
