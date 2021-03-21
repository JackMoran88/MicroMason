<template>
    <div class="read-more">
        <div
                v-if="Html"
                class="read-more__content"
                :style="{maxHeight: MaxHeight+'px'}"
                :class="{'active': isReadMore}"
                v-html="Html"
        ></div>
        <div
                v-if="Text"
                class="read-more__content"
                :style="{maxHeight: MaxHeight+'px'}"
                :class="{'active': isReadMore}"
        >{{Text}}
        </div>
        <v-btn
                v-if="state"
                BtnStyle="secondary"
                :class="{'active': isReadMore && state}"
                :BtnName="isReadMore ? 'Свернуть' : 'Читать дальше'"
                @click.native="toggleReadMore"
        />
    </div>
</template>

<script>
export default {
  name: 'v-read-more',
  props: {
    MaxHeight: {
      type: String,
      default: '250px',
    },
    Html: {
      type: String,
    },
    Text: {
      type: String,
    },
  },
  data() {
    return {
      state: true,
      isReadMore: false,
    };
  },
  methods: {
    toggleReadMore() {
      this.isReadMore = !this.isReadMore;
    },
  },
  mounted() {
    window.addEventListener('load', () => {
      const content = document.getElementsByClassName('read-more__content');
      if (content[0] && content[0].offsetHeight < this.MaxHeight) {
        this.state = false;
      }
    });
  },
};
</script>

<style scoped lang="scss">
    .read-more {
        position: relative;

        &__content {
            overflow: hidden;

            &.active {
                max-height: max-content !important;

                button {
                    box-shadow: none;
                }
            }
        }

        button {
            position: absolute;
            top: 100%;
            left: 0;

            background: var(--background-content);
            width: 100%;
            text-align: left;
            padding: .375rem 0;
            box-shadow: 15px -20px 15px 0px rgba(var(--background-content), 1),
            -15px -20px 15px 0px rgba(--background-content, 1);

            &.active {
                padding: 0;
                box-shadow: none;
            }
        }

    }
</style>
