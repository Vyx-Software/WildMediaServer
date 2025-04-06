// @ts-check
/** @type {import('prettier').Options} */
module.exports = {
    // Core formatting rules
    printWidth: 100,
    singleQuote: true,
    trailingComma: 'es5',
    tabWidth: 2,
    semi: true,
    arrowParens: 'avoid',
    bracketSpacing: true,
    endOfLine: 'lf',
  
    // Framework-specific formatting
    overrides: [
      {
        files: '*.{ts,tsx}',
        options: {
          parser: 'typescript',
        },
      },
      {
        files: '*.scss',
        options: {
          singleQuote: false,
        },
      },
      {
        files: '*.vue',
        options: {
          parser: 'vue',
          htmlWhitespaceSensitivity: 'ignore',
          vueIndentScriptAndStyle: false,
          singleAttributePerLine: true,
        },
      },
    ],
  
    // Plugin configurations
    plugins: [
      '@trivago/prettier-plugin-sort-imports',
      'prettier-plugin-tailwindcss',
    ],
  
    // Import sorting rules
    importOrder: [
      '^vue$',
      '^@?\\w',
      '^@/(.*)$',
      '^[./]',
    ],
    importOrderSeparation: true,
    importOrderSortSpecifiers: true,
  
    // Tailwind CSS sorting
    tailwindConfig: './tailwind.config.js',
    tailwindFunctions: ['clsx', 'cn'],
  };