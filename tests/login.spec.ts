import {test, expect} from '@playwright/test'
import { LoginPage } from '../pages/login.page';
import { OverviewPage } from '../pages/overview.page';

test('Successful Login (Happy Path)', async({page}) => {
  const loginPage = new LoginPage(page);
  const overviewPage = new OverviewPage (page);

  await page.goto('http://localhost:8080/parabank/index.htm');
  await loginPage.usernameInput.fill("admin");
  await loginPage.passwordInput.fill("admin");
  await loginPage.loginButton.click();
  await expect(overviewPage.accountsOverviewHeader).toHaveText("Accounts Overview");
});

test('Unsuccessful Login with Invalid Username', async({page}) => {
  const loginPage = new LoginPage(page);

  await page.goto('http://localhost:8080/parabank/index.htm');
  await loginPage.usernameInput.fill("admin");
  await loginPage.passwordInput.fill("admin123");
  await loginPage.loginButton.click();

  await expect(loginPage.loginErrorMessage).toHaveText("The username and password could not be verified.");

});