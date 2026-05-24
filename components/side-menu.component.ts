import { Page } from "@playwright/test";

export class AccountServicesSideMenuComponent {
    readonly openNewAccountLink;

    constructor(page: Page) {
        this.openNewAccountLink = page.getByRole('link', { name: 'Open New Account' })

    }
}