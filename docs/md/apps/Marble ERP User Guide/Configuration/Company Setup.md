# Company Setup

## Internal Organizations (Companies)

The first setup that needs to be done is to setup your company as the main POP Commerce company.  This is done using the **Parties** link on the POPC main dashboard to go to the **[Find Party](https://demo.moqui.org/vapps/PopcAdmin/Party/FindParty)** screen. 

Click the **New Organization** button to open its dialog, then enter the name of the company and create.

This next step is to highlight that this is an organization that is being operated with the system which is called an **Internal** organization. This is done by adding the role **Internal**  in the *Roles* section on the **Party** screen which you'll see after creating the organization.

## Accounting Settings

Once you have added the **Internal** role to the company's Party it will be listed on the [Accounting Dashboard](https://demo.moqui.org/vapps/PopcAdmin/Accounting/dashboard) screen. Click on the **Settings** link shown in the right column of the table showing Internal Organizations.

That will take you to the **Accounting Preferences** tab and when there are no preferences for an internal organization it shows a form to add them by specifying a *Base Currency* and a *Source Party*. The *Source Party* is another Party in the system with accounting preferences that you can copy from. The base data that comes with POPC ERP includes a Party named **Default Accounting, etc Settings** [DefaultSettings] the includes the default and recommend GL mappings for the default chart of accounts.

Note that if you want to use a custom chart of accounts it is best to not load the default chart of accounts data files. You can enter custom GL accounts and mappings for them in the application from the Settings screens but it is usually easier to create a data file to import, like the [XML data file for the default chart of accounts](https://github.com/moqui/mantle-udm/blob/master/data/ZaaGlAccountsInstallData.xml).

