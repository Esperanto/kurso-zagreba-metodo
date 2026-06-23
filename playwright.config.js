const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: 'tests/ui',
  timeout: 30000,
  reporter: [['list']],
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
  webServer: {
    command: 'make serve HOST=127.0.0.1 PORT=4173',
    url: 'http://127.0.0.1:4173/en/01/',
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
