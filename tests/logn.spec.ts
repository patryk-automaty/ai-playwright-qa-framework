import {test, expect} from '@playwright/test'

test('Successful Login (Happy Path)', async({page}) => {
  await page.goto('http://localhost:8080/parabank/index.htm');
  await page.locator('input[name="username"]').fill("admin");
  await page.locator('input[name="password"]').fill("admin");
  await page.getByRole('button', { name: 'Log In' }).click();
});