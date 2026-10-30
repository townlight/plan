// SPDX-License-Identifier: AGPL-3.0-only
// Real-browser acceptance for Townlight Planning's public plan exploration.
//
// A real Chromium loads the public page, submits the real exploration form, and
// must see citations rendered from stored plan sources, a working filter, and an
// explicit empty state -- with no static sample text and no staff-only plan.
//
// Usage: node browser-plan-explore.cjs <base-url> <run-root>
const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/scott/Documents/Codex/2026-10-21/c/work/townlight-cleanup/repos/townlight/desktop/node_modules/playwright');

const [base, runRoot] = process.argv.slice(2);
if (!base || !runRoot) {
  console.error('usage: node browser-plan-explore.cjs <base-url> <run-root>');
  process.exit(2);
}
fs.mkdirSync(runRoot, { recursive: true });
const checks = [];
function pass(name, detail) {
  checks.push({ check: name, detail });
  console.log('PASS:', name, detail === undefined ? '' : JSON.stringify(detail));
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  const consoleErrors = [];
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  try {
    const response = await page.goto(`${base}/civicplan`, { waitUntil: 'load' });
    if (!response || !response.ok()) throw new Error(`page status ${response && response.status()}`);
    const body = await page.textContent('body');
    if (!/Fictional/i.test(body)) throw new Error('no persisted plan content on the page');
    if (/Housing proposal context/.test(body)) throw new Error('static sample text survived');
    if (/Internal draft/i.test(body)) throw new Error('staff-only plan leaked to the public page');
    const citations = await page.locator('.policy .citation').allTextContents();
    if (!citations.length) throw new Error('no cited policies rendered');
    pass('a real browser sees adopted-plan citations on the public page',
      { citations: citations.slice(0, 4) });

    // Real form interaction: choose a goal and submit.
    const goals = await page.locator('#goal option').evaluateAll(
      (nodes) => nodes.map((node) => node.value).filter(Boolean));
    if (!goals.length) throw new Error('no persisted goals offered in the filter');
    await page.selectOption('#goal', goals[0]);
    await Promise.all([page.waitForNavigation({ waitUntil: 'load' }), page.click('button[type="submit"]')]);
    const filtered = await page.textContent('body');
    if (!new RegExp(goals[0].replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i').test(filtered)) {
      throw new Error('goal filter did not take effect');
    }
    const filteredCitations = await page.locator('.policy .citation').allTextContents();
    if (!filteredCitations.length) throw new Error('goal filter produced no cited policies');
    pass('a real browser filters by a persisted goal and still sees citations',
      { goal: goals[0], count: filteredCitations.length });

    // Real keyword search: a term in persisted text, then one nothing supports.
    await page.fill('#q', 'transit');
    await Promise.all([page.waitForNavigation({ waitUntil: 'load' }), page.click('button[type="submit"]')]);
    const searched = await page.textContent('body');
    if (!/transit/i.test(searched)) throw new Error('keyword search did not reach persisted text');
    const hits = await page.locator('.policy').count();
    if (!hits) throw new Error('keyword search matched nothing');
    pass('a real browser keyword search matches persisted plan text', { hits });

    await page.fill('#q', 'heliport');
    await Promise.all([page.waitForNavigation({ waitUntil: 'load' }), page.click('button[type="submit"]')]);
    const empty = await page.textContent('body');
    if (!/Nothing to show/i.test(empty)) throw new Error('no explicit empty state');
    if (await page.locator('.policy').count()) throw new Error('empty state still rendered policies');
    if (!/heliport/i.test(empty)) throw new Error('empty state does not name the query');
    pass('a real browser sees an explicit empty state for an unsupported exploration');

    // Clear filters brings the full exploration back.
    await Promise.all([page.waitForNavigation({ waitUntil: 'load' }),
      page.click('button[name="clear"]')]);
    if (!(await page.locator('.policy').count())) throw new Error('clearing filters lost the results');
    pass('clearing filters returns to the full persisted exploration');

    // Keyboard reachability of the form controls.
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement && document.activeElement.id);
    if (!focused) throw new Error('no focusable control reached by keyboard');
    pass('the exploration form is reachable by keyboard', { firstFocus: focused });

    await page.screenshot({ path: path.join(runRoot, 'plan-explore-desktop.png'), fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    if (!(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth))) {
      throw new Error('page overflows horizontally on a narrow viewport');
    }
    await page.screenshot({ path: path.join(runRoot, 'plan-explore-mobile.png'), fullPage: true });
    pass('the public page fits a narrow viewport without horizontal overflow');
    fs.writeFileSync(path.join(runRoot, 'browser-result.json'),
      JSON.stringify({ checks, consoleErrors }, null, 2));
    console.log(JSON.stringify({ checks: checks.length }));
  } catch (error) {
    fs.writeFileSync(path.join(runRoot, 'browser-failure.json'),
      JSON.stringify({ error: String((error && error.stack) || error), checks, consoleErrors,
        body: await page.content().catch(() => '') }, null, 2));
    throw error;
  } finally {
    await context.close();
    await browser.close();
  }
})().catch((error) => {
  console.error('FAILED:', error.message);
  process.exit(1);
});
