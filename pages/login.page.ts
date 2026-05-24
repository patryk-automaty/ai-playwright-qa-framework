import { Locator, Page } from "@playwright/test";
import { AccountServicesSideMenuComponent } from "../components/side-menu.component";

export class LoginPage {
    readonly usernameInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;
    readonly loginErrorMessage: Locator;
    readonly emptyLoginOrPasswordMessage: Locator;
    readonly accountSideMenu: AccountServicesSideMenuComponent;

    constructor(page: Page) {

    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.loginButton = page.getByRole('button', { name: 'Log In' });
    this.loginErrorMessage = page.getByText('The username and password');
    this.emptyLoginOrPasswordMessage = page.getByText('Please enter a username and')
    this.accountSideMenu = new AccountServicesSideMenuComponent(page);
    }

    async login(userName: string, userPassword: string): Promise <void> {
      await this.usernameInput.fill(userName);
      await this.passwordInput.fill(userPassword);
      await this.loginButton.click();
    }

     async logout(userName: string, userPassword: string): Promise <void> {

      await this.login(userName, userPassword)
      await this.accountSideMenu.logOutLink.click();

    }
}