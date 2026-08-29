# Bank Accounts

[TOC levels=2]

## Setup Bank Account

TODO

## Generate NACHA File

After setting up a Bank Account you can create ACH Payments for that account and generate NACHA files for those payments. The Party each ACH payment will be sent to must also have a Bank Account setup with routing and account numbers.

For a Payment to be included in a generated NACHA file it must have the following:

1. **From**: Organization that the Bank Account is for
2. **From Payment Method**: the Bank Account the ACH should be sent from
3. **To**: Party with a Bank Account to send the ACH payment to
4. **To Payment Method**: the Bank Account to send the ACH to
5. **Payment Instrument**: must be '**ACH Direct**'
6. **Status**: must be set to '**Authorized**'; only Authorized payments are included when generating NACHA files; when the system generates a NACHA file it will record which file the payment is in and it will update the payment Status to Delivered

Other fields on the Payment will depend on what the payment is for. ACH payments may be used for Invoice payments, owner distributions, and so on.

To create a new outgoing Payment:

1. start on the Accounting Dashboard screen [(demo)](https://demo.moqui.org/vapps/PopcAdmin/Accounting/dashboard)
2. click on the **Payments** button under the Invoices and Payments section
3. use the **New Outgoing Payment** dialog to create a Payment
    1. select the desired **From** and **To** parties
    2. select '**ACH Direct**' for the **Instrument**
    3. select the appropriate **Payment Type** and specify the **Amount** and **Effective Date**
    4. submit the form with the **Create Payment** button
4. now on the Payment Detail screen
    1. select the desired **From Payment Method** and **To Payment Method**; if either party has no Bank Account setup add those and then go back to the Payment screen to select the new Bank Account
    2. (optional) set other Payment data as needed
    3. submit the form with the **Update** button
    4. change the payment status to '**Authorized**' using the **Authorize (Authorized)** button in the status section of the screen

There are other ways to create payments, including from orders and invoices. If a Payment already exists just go through the 6 point check list to above to make sure the fields required for ACH payments are set.

Once there is at least one such Payment you can go to the 'Files' tab for the Bank Account and use the dialog there to create a NACHA file. If a transport is configured you can send it to your bank directly from the application, otherwise you can download the NACHA file and upload it to your bank through their web site or by whatever other means are available.

1. start on the Accounting Dashboard screen [(demo)](https://demo.moqui.org/vapps/PopcAdmin/Accounting/dashboard)
2. click on the link for desired Bank Account in the list of Internal Organizations, then go to the 'Files' tab [(demo)](https://demo.moqui.org/vapps/PopcAdmin/Party/PaymentMethod/PaymentMethodFiles?paymentMethodId=ZIRET_BA&partyId=ORG_ZIZI_RETAIL)
3. use the **Generate NACHA File** dialog to generate a NACHA file, you can use the default options (no From Date or Thru Date) to include all outstanding ACH payments setup with the guidelines above
4. (optional) click on the **Payments** button for the NACHA file to see the payments included in the file
5. (optional) if there are issues with the file click on the red **Cancel** button for the file, adjust Payment or other data as needed, and generate a new NACHA file
6. when ready click on **Send to Bank** to send the NACHA file to the bank by the configured transport
7. if there is no configured transport for the system to send the file to the bank then there will be no Send to Bank button so use the **Download File {ID}** button to download the NACHA file and then upload or send it to the bank manually

## Generate Positive Pay File

TODO

## Import OFX/QFX Transactions File

This import supports OFX version 1 and QFX which is an OFX SGML file with header lines that are separate from the SGML content.

If there is no automated OFX/QFX import setup on your system you may manually import bank account transactions from an OFX or QFX file using the **Upload OFX V1 (or QFX)** dialog on the Transactions tab of the Payment Method screens.

On a technical note an automatic import service is supported using the System Message integration functionality in Moqui framework. The consume service to use is: *mantle.account.OfxServices.consume#OfxV1SystemMessage*. Using System Message based integrations different transports are supported including SFTP using the *org.moqui.sftp.SftpMessageServices.poll#SystemMessageSftp* service. For more details on configuration see the demo data for the *DemoZiretOfx* SystemMessageType and the *DemoZiretSftp_poll_OFX* ServiceJob.

## Import BAI 2 Transactions File

This import supports BAI version 2. The [BAI 2 specification PDF](https://www.sepaforcorporates.com/swift-for-corporates/bai2-format-specification/) is available from bai.org.

If there is no automated BAI 2 import setup on your system you may manually import bank account transactions from a BAI 2 file using the **Upload BAI V2** dialog on the Transactions tab of the Payment Method screens.

On a technical note an automatic import service is supported using the System Message integration functionality in Moqui framework. The consume service to use is: *mantle.account.BaiServices.consume#Bai2SystemMessage*. Using System Message based integrations different transports are supported including SFTP using the *org.moqui.sftp.SftpMessageServices.poll#SystemMessageSftp* service. For more details on configuration see the demo data for the *DemoZiretBai2* SystemMessageType and the *DemoZiretSftp_poll_BAI2* ServiceJob.

## Reconcile Transactions

Bank account transactions imported from OFX/QFX or BAI 2 files, or added manually, may be matched and reconciled with **Payment** and **GL Transaction** records on the Transactions tab of the Payment Method screens. To get to that tab start from the Accounting Dashboard and click on the link for the desired bank account.

Many transactions can be automatically matched using the **Auto Match and Reconcile** dialog on the Transactions tab. After this has run you can scan down the transaction list to check the results, making sure amounts and check or reference numbers match. For transactions that are not automatically matched you have a few options:

1. Create a Payment using the **New Payment** dialog; this will automatically populate various fields based on the data in the bank account transaction and once created the new Payment will be matched and reconciled with the bank account transaction; if the status of the new payment is set to Delivered (the default) it will automatically post to the GL and the GL Transaction will also be matched and reconciled with the bank account transaction
2. Manually reconcile with a Payment and/or GL Transaction using the **Manual Rec** dialog; note that you only need to specify a Payment ID or a GL Transaction ID and both will be matched and reconciled if the Payment and GL Transaction are associated (which is commonly the case); to look up the Payment ID use the Accounting => Payments => Find Payment screen, and similarly for the GL Transaction ID use the Accounting => Transactions => Find Transaction screen
3. Mark the bank account transaction to not reconcile using the **No Rec** button; this will flag the transaction so that Auto Match and Reconcile will not try to reconcile it, and it won't show up when searching for transactions that have not been reconciled using the **Only Not Rec** Find Option

It is generally best to review and manually reconcile bank account transactions one day or week at a time. This can be done by selecting a date range for the **Posted Date** field in the Find Options dialog. To view only transactions that have not yet been reconciled select '**Y**' for the **Only Not Rec** field in the Find Options dialog. If you're looking for a specific bank account transaction you can search by various other fields as well.

If a bank account transaction was incorrectly matched or was flagged as No Rec you may clear that using the **Unrec** button. This will clear match and reconcile data and allow you to use any of the options listed above for the bank account transaction.
