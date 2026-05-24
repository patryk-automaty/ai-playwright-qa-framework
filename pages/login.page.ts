import { Locator, Page } from "@playwright/test";

export class LoginPage {
    readonly usernameInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;
    readonly loginErrorMessage: Locator;

    constructor(page: Page) {

    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.loginButton = page.getByRole('button', { name: 'Log In' });
    this.loginErrorMessage = page.getByText('The username and password');
    }

    async login(userName: string, userPassword: string): Promise <void> {
      await this.usernameInput.fill(userName);
      await this.passwordInput.fill(userPassword);
      await this.loginButton.click();
    }
}