<template>

  <div class="TechnicalProblem">
    <div>
      <h1>503</h1>
      <h2>{{header}}</h2>
      <p>{{body}}</p>
    </div>
  </div>

</template>

<script>
  import {mapGetters} from 'vuex';

  export default {
    name: 'ServerProblem',
    data() {
      return {
        header: 'Технические неполадки',
        body: 'К сожалению на сервере технические неполадки, '
          + 'мы приносим извинения и просим вас зайти позже ',
      };
    },
    methods: {},
    mounted() {},
    computed: {
      ...mapGetters(['SERVER_PROBLEM']),
    },
    watch: {},
  };
</script>

<style scoped lang="scss">
  .TechnicalProblem {
    width: 100%;
    min-height: 100vh;
    max-width: 100vw;

    padding: 2rem 1rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;


    h1 {
      font-size: 7.5em;
      margin: 15px 0px;
      font-weight: bold;
    }

    h2 {
      font-weight: bold;
    }

    > div {
      min-width: 50%;
    }
  }


</style>
