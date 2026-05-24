import {test, expect} from '@playwright/test'
import { LoginPage } from '../pages/login.page';

test('Successful Login (Happy Path)', async({page}) => {
  const loginPage = new LoginPage(page);
  await page.goto('http://localhost:8080/parabank/index.htm');
  await loginPage.usernameInput.fill("admin");
  await loginPage.passwordInput.fill("admin");
  await loginPage.loginButton.click();
});