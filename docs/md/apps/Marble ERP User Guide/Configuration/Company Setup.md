# Company Setup

## Internal Organizations (Companies)

The first setup that needs to be done is to set up your company as the main Marble ERP company. This is done using the **Internal** or **All Parties** link on the Marble ERP dashboard to go to the **[Find Party](https://demo.moqui.org/qapps/marble/Party/FindParty)** screen.

Click the **New Organization** button to open its dialog, then enter the name of the company and create.

The next step is to mark this as an organization that is operated with the system, called an **Internal** organization. This is done by adding the **Internal Organization** role in the *Roles* section on the **Party** screen which you'll see after creating the organization.

## Accounting Settings

Once you have added the **Internal** role to the company's Party it will be listed on the [Accounting Dashboard](https://demo.moqui.org/qapps/marble/Accounting/dashboard) screen. Click on the **Settings** link shown in the right column of the table showing Internal Organizations.

That will take you to the **Accounting Preferences** tab and when there are no preferences for an internal organization it shows a form to add them by specifying a *Base Currency* and a *Source Party*. The *Source Party* is another Party in the system with accounting preferences that you can copy from. The base data that comes with Marble ERP includes a Party named **Default Accounting, etc Settings** [DefaultSettings] that includes the default and recommended GL mappings for the default chart of accounts.

Note that if you want to use a custom chart of accounts it is best to not load the default chart of accounts data files. You can enter custom GL accounts and mappings for them in the application from the Settings screens but it is usually easier to create a data file to import, like the [XML data file for the default chart of accounts](https://github.com/moqui/mantle-udm/blob/master/data/ZaaGlAccountsInstallData.xml).
