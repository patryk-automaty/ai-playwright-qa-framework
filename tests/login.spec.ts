import {test, expect} from '@playwright/test'
import { LoginPage } from '../pages/login.page';
import { OverviewPage } from '../pages/overview.page';

test.describe("Module: Customer Login", () => {

  let loginPage: LoginPage;
  let overviewPage: OverviewPage;

  test.beforeEach(async ({page}) => {

    await page.goto('http://localhost:8080/parabank/index.htm');
    loginPage = new LoginPage(page);
    overviewPage = new OverviewPage (page);
  });

  test('Successful Login (Happy Path)', async({page}) => {

    await loginPage.login("admin", "admin")
    await expect(overviewPage.accountsOverviewHeader).toHaveText("Accounts Overview");
  });

  test('Unsuccessful Login with Invalid Username', async({page}) => {

    await loginPage.login("admin", "admin123")
    await expect(loginPage.loginErrorMessage).toHaveText("The username and password could not be verified.");
});
});