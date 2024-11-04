/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution');

module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    'plugin:vue/vue3-recommended',
    'eslint:recommended'
    // '**prettier**'
  ],
  env: {
    node: true
  },
  plugins: ['vue', 'prettier', '@typescript-eslint'],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'comma-dangle': 'off',
    'prefer-const': 'off',
    'no-unused-vars': 'warn',
    'vue/script-setup-uses-vars': 'off',
    'vue/multi-word-component-names': 'off',
    'vue/no-reserved-component-names': 'off',
    // 'vue/component-name-in-template-casing': ['error', 'kebab-case', { ignores: [] }],
    // 'vue/multi-word-component-names': ['error', { ignores: [] }],
    '@typescript-eslint/comma-dangle': 'off',
    'javascript.validate.enable': 0,
    'prettier/prettier': [
      'error',
      {
        semi: true,
        tabWidth: 2,
        printWidth: 150,
        endOfLine: 'auto'
      }
    ]
  }
};
