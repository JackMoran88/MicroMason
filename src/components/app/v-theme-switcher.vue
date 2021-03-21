<template>
  <div>
    <toggle-button v-model="darkMode"
                   :height='18'
                   class="v-theme-switcher"
                   :margin="1"
                   :color="{checked: '#1F3044', unchecked: '#1F3044'}"
                   :switch-color="{checked: '#d5410b', unchecked: '#e95d2a'}"
                   :sync="true"
                   :labels="true"/>
  </div>
</template>

<script>
  export default {
    name: "v-theme-switcher",
    data() {
      return {
        darkMode: false,
      }
    },
    methods: {
      changeMode() {
        // add/remove class to/from html tag
        let htmlElement = document.documentElement;
        if (this.darkMode) {
          localStorage.setItem("theme", 'dark');
          htmlElement.setAttribute('theme', 'dark');
        } else {
          localStorage.setItem("theme", 'light');
          htmlElement.setAttribute('theme', 'light');
        }
      }
    },
    mounted() {
      let bodyElement = document.body;
      bodyElement.classList.add("app-background");
      if (localStorage.getItem("theme") === 'dark') {
        this.darkMode = true
      } else if (localStorage.getItem("theme") === 'light') {
        this.darkMode = false
      }
    },
    watch: {
      'darkMode'() {
        this.changeMode()
      }
    }
  }
</script>

<style scoped lang="scss">
  .v-theme-switcher {
    margin: 0;
    height: min-content;
  }
</style>
