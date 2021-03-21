module.exports = {
  root: true,

  env: {
    node: true,
  },

  extends: [
    'plugin:vue/essential',
    '@vue/airbnb',
  ],

  parserOptions: {
    parser: 'babel-eslint',
  },

  ignorePatterns: ['ServerProblem.vue', '**/vendor/*.js', '**/assets/*.js', '**/assets/**/*.js', 'globalComponents.js'],

  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',

    'prefer-destructuring': ['error', { object: false, array: false }],
    'no-underscore-dangle': ['error', { allow: ['_vm'] }],
    'no-empty-pattern': 0,
    'import/no-cycle)': 0,
  },
};
