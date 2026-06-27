import {test, expect} from '@playwright/test'
import { LoginPage } from '../pages/login.page';
import { OverviewPage } from '../pages/overview.page';

test.describe("Module: Customer Login", () => {

  let loginPage: LoginPage;
  let overviewPage: OverviewPage;
  let correctUserName: string;
  let incorrectUserName: string;
  let correctPassword: string;
  let incorrectPassword: string;
  let longUsername: string;
  let longPassword: string;
  let boundaryUsername: string;
  let boundaryPassword: string;

  test.beforeEach(async ({page}) => {

    await page.goto('/parabank/index.htm');
    loginPage = new LoginPage(page);
    overviewPage = new OverviewPage (page);
    correctUserName = "john";
    incorrectUserName = "admin123";
    correctPassword = "demo";
    incorrectPassword = "admin123";
    longUsername = 'a'.repeat(256);
    longPassword = 'a'.repeat(256);
    boundaryUsername = 'a'.repeat(50);
    boundaryPassword = 'a'.repeat(50);


  });

  test('TC-001 - Successful Login (Happy Path) ',{tag: ['@smoke', '@positive', '@login']}, async({page}) => {

    await loginPage.login(correctUserName, correctPassword)
    await expect(overviewPage.accountsOverviewHeader).toHaveText("Accounts Overview");
  });

  test('TC-002 - Unsuccessful Login with Invalid Username', {tag: ['@negative', '@login']}, async({page}) => {

    await loginPage.login(incorrectUserName, correctPassword)
    await expect(loginPage.loginErrorMessage).toHaveText("The username and password could not be verified.");
});

  test('TC-003 - Unsuccessful Login with Invalid Password', {tag: ['@negative', '@login']}, async({page}) => {

    await loginPage.login(correctUserName, incorrectPassword);
    await expect(loginPage.loginErrorMessage).toHaveText("The username and password could not be verified.");
});
  
  test('TC-004 - Unsuccessful Login with Empty Username', {tag: ['@negative', '@validation', '@login']}, async ({page}) => {

    await loginPage.passwordInput.fill(correctPassword);
    await loginPage.loginButton.click();

    await expect(loginPage.emptyLoginOrPasswordMessage).toHaveText("Please enter a username and password.")
  });

  test('TC-005 - Unsuccessful Login with Empty Password', {tag: ['@negative', '@validation', '@login']}, async ({page}) => {

    await loginPage.usernameInput.fill(correctUserName);
    await loginPage.loginButton.click();

    await expect(loginPage.emptyLoginOrPasswordMessage).toHaveText("Please enter a username and password.")
  });  

  test('TC-006 - Unsuccessful Login with Both Fields Empty', {tag: ['@negative', '@validation', '@login']}, async ({page}) => {

    await loginPage.loginButton.click();

    await expect(loginPage.emptyLoginOrPasswordMessage).toHaveText("Please enter a username and password.")
  });
  
  test('TC-007 - Session Termination via Log Out', {tag: ['@security', '@login']}, async ({page}) => {

    await loginPage.logout(correctUserName, correctPassword);

    await expect(loginPage.loginButton).toBeVisible();
  });
    
  test('TC-010 - Login with Long Username', {tag: ['@negative', '@boundary', '@login']}, async ({page}) => {

    await loginPage.login(longUsername, correctPassword);
    await expect(loginPage.loginErrorMessage).toHaveText("The username and password could not be verified.");
  });

  test('TC-011 - Login with Long Password', {tag: ['@negative', '@boundary', '@login']}, async ({page}) => {

    await loginPage.login(correctUserName, longPassword);
    await expect(loginPage.loginErrorMessage).toHaveText("The username and password could not be verified.");
  });

  test('TC-012 - Boundary Value Test for Username Length', {tag: ['@boundary', '@login']}, async ({page}) => {

    await loginPage.login(boundaryUsername, correctPassword);
    await expect(loginPage.loginErrorMessage).toBeVisible();
  });

  test('TC-013 - Boundary Value Test for Password Length', async ({page}) => {

    await loginPage.login(correctUserName, boundaryPassword);
    await expect(loginPage.loginErrorMessage).toBeVisible();
  });




});