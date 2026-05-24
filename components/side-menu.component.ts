import { Page } from "@playwright/test";

export class AccountServicesSideMenuComponent {
    readonly openNewAccountLink;
    readonly logOutLink;

    constructor(page: Page) {
        this.openNewAccountLink = page.getByRole('link', { name: 'Open New Account' })
        this.logOutLink = page.getByRole('link', { name: 'Log Out' })
        
    }
}