// Frontend test configuration. Run with:  npm run test:frontend
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom', // a fake browser DOM so components can render
    include: ['frontend/tests/**/*.test.{js,jsx}'],
    setupFiles: ['frontend/tests/setup.js'],
    css: false, // CSS imports resolve to nothing instead of being parsed
  },
});
