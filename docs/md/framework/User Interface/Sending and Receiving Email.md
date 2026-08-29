# Sending and Receiving Email

The first step to sending and receiving email is to set up an EmailServer with something like this record loaded:

```
<moqui.basic.email.EmailServer emailServerId="SYSTEM"
   smtpHost="mail.test.com" smtpPort="25" smtpStartTls="N" smtpSsl="N"
   storeHost="mail.test.com" storePort="143" storeProtocol="imap"
   storeDelete="N" mailUsername="TestUser" mailPassword="TestPassword"/>
```

Note that these are all example values and should be changed to real values, especially for the **smtpHost**, **storeHost**, **mailUsername** and **mailPassword** fields. The **store\*** fields are for the remote mail store for incoming email. Here are some other common values for the port fields:

-   **smtpPort**: 25 (SMTP), 465 (SSMTP), 587 (SSMTP)
-   **storePort** for **storeProtocol**=imap: 143 (IMAP), 585 (IMAP4-SSL), 993 (IMAPS)
-   **storePort** for **storeProtocol**=pop3: 110 (POP3), 995 (SSL-POP)

If you need to work with multiple email servers, just add *EmailServer* records with the settings for each. When sending an email using an email template the *EmailServer* to use is specified on the *EmailTemplate* record with the **emailServerId** field.

Speaking of EmailTemplate, the next step for sending an email is to create one. Here is an example from HiveMind PM for sending a task update notification email:

```
<moqui.basic.email.EmailTemplate emailTemplateId="HM_TASK_UPDATE"
   description="HiveMind Task Update Notification"
   emailServerId="SYSTEM" webappName="webroot"
   bodyScreenLocation="component://HiveMind/screen/TaskUpdateNotification.xml"
   fromAddress="test@test.com" ccAddresses="" bccAddresses=""
   subject="Task Updated: ${document._id} - ${document.name}"/>
```

The general idea is to define a screen that will be rendered for the body when the email is sent (**bodyScreenLocation**). The email body screen is a little bit different from normal UI screens because there is no Web Facade available when it is rendered as it is not part of a web request. The URL prefixes (domain name, port, etc) are generated based on webapp settings in the Moqui Conf XML file, which is why it is necessary to specify a **webappName** which is matched against the *moqui-conf.webapp-list.webapp*.**name** attribute.

The **subject** is also a simple template of sorts, it is a Groovy String that is expanded when the email is sent using the same context as rendering the body. The **fromAddress** field is required, and you can optionally specify **ccAddresses** and **bccAddresses**.

Attachments to an *EmailTemplate* can be added with the *EmailTemplateAttachment* entity. The filename to use on the email must be specified using the **fileName** field. The attachment itself comes from rendering a screen specified with the **attachmentLocation** field (or **screenPath** from the webroot). The **screenRenderMode** field is passed to the *ScreenRender* to specify the type of output to get from the screen. It is also used to determine the MIME/content type. If empty the content at **attachmentLocation** will be sent over without screen rendering and its MIME type will be based on its extension. This can be used to generate XSL-FO that is transformed to a PDF and attached to the email by setting **screenRenderMode** to *xsl-fo*.

Once the *EmailServer* and *EmailTemplate* are defined you can send email using the *org.moqui.impl.EmailServices*.**send\#EmailTemplate** service. When calling this service pass in the **emailTemplateId** parameter to identify the EmailTemplate. As mentioned above the *EmailServer* will be determined based on the *EmailTemplate*.**emailServerId** field. Sending uses Apache Commons Email 2 (`org.apache.commons.mail2.jakarta`) on **jakarta.mail**.

The email addresses to send the message to are passed in the **toAddresses** parameter which is a plain *String* and can have multiple comma-separated addresses. The parameters used to render the email screen are separate from the context of the service and are passed to it in the **bodyParameters** input parameter. By default the **send\#EmailTemplate** service saves details about the outgoing message in a record of the *EmailMessage* entity. To disable this pass in false in the **createEmailMessage** parameter. The output parameters are **messageId** which is the value put in the Message-ID email header field, and **emailMessageId** if an EmailMessage record is created.

The *EmailMessage* entity is used for both outgoing and incoming email messages. For outgoing messages sent using the **send\#EmailTemplate** service the status (**statusId**) starts out as Draft (`ES_DRAFT`), is set to Ready (`ES_READY`) after the body is rendered, then to Sent (`ES_SENT`) after the message is actually sent. It may be changed to Viewed if there is open message tracking based on an image request (usually with the **emailMessageId** as a parameter or path element). If the message is returned undeliverable the status may be changed to Bounced.

An EmailMessage may also be sent manually instead of from a template and in that case the status would start out as Draft. Once the user is done with the message they would change the status to Ready, and then when it is actually sent the status would change to Sent. Incoming messages start in the Received status and can be changed to the Viewed status after they are initially opened.

For email threads the *EmailMessage* entity has **rootEmailMessageId** for the original messages that all messages in the thread are grouped under, and **parentEmailMessageId** for the message the current message was an immediate reply to.

Receiving email follows a very different path. The *org.moqui.impl.EmailServices*.**poll\#EmailServer** service polls an IMAP or POP3 mailbox based on the settings on the EmailServer entity. It takes a single input parameter, the **emailServerId**. Generally this will be run as a scheduled Service Job (the OOTB job is paused by default).

For each message found in the mailbox and not yet marked as seen this service calls the Email ECA (EMECA) rules for it (`.emecas.xml` files, schema `email-eca-3.xsd`). These are similar to the Entity and Service ECA rules but there is no special trigger, just the receiving of an email. The conditions can be used to only run the actions for a particular to-address or tag in the subject or any other criteria desired.

The context for the condition and actions includes:

-   **headers**: a *Map* with all of the email headers (either *String*, or *List* of *String* if there is more than one of the header; names are lower-cased)
-   **fields**: a *Map* with **toList**, **ccList**, **bccList**, **from**, **subject**, **sentDate**, **receivedDate** (the date fields are `java.sql.Timestamp`)
-   **flags**: a *Map* of boolean IMAP/POP flags (**answered**, **deleted**, **draft**, **flagged**, **recent**, **seen**)
-   **bodyPartList**: a *List* of *Map* with info for each body part (**contentType**, **filename**, **disposition**, **contentText**, **contentBytes**)
-   **message**: the `jakarta.mail.internet.MimeMessage`
-   **emailServerId**

For a service that is called directly with this context you can implement the *org.moqui.EmailServices*.**process\#EmailEca** interface.

The actions and services they call can do anything with the incoming email. To save the incoming message you can use the *org.moqui.impl.EmailServices*.**save#EcaEmailMessage** service. The example component includes a simple EMECA rule in `Example.emecas.xml` that does exactly that when the message has a subject.
