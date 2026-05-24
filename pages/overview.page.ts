import { Locator, Page } from "@playwright/test";

export class OverviewPage {
    readonly accountsOverviewHeader: Locator;


    constructor(page: Page) {
        this.accountsOverviewHeader = page.getByRole('heading', { name: 'Accounts Overview' });
    }
}


// await page.getByRole('heading', { name: 'Accounts Overview' }).click();