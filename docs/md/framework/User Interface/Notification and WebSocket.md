# Notification and WebSocket

The Notification functionality in Moqui Framework is a user- and topic-based publish/subscribe tool that can be used to push notifications to server code by direct topic subscription or to client applications by WebSocket. Other interfaces for client applications could be built for anything you'd like, but the current OOTB implementation for this is WebSocket based and meant for notifications, screen pops, etc. in web-based client applications.

The WebSocket endpoint is configured in `MoquiDefaultConf.xml` as **path="/notws"** (`org.moqui.impl.webapp.NotificationEndpoint`). The implementation uses **Jakarta WebSocket** (`jakarta.websocket`), not `javax.websocket`.

## NotificationMessage (server side)

The NotificationMessage interface in the Moqui Framework API is the primary object for generating notifications for one or more users and with a specific topic. The topic for a Notification is an arbitrary string identifier to distinguish different types of messages so that listeners (server side or client side) can listen for just the topics they know how to handle.

To generate a message first use the ExecutionContext.makeNotificationMessage() method which returns a NotificationMessage object. On that object call methods as needed to set the topic, title, type (info, success, warning, danger), message (Map or JSON body), and specify the user(s) and/or user groups that should receive the notification. For example:

    ec.makeNotificationMessage().topic("TestTopic").type("info").title("Test notification message")
            .message(messageMapOrJsonString).userGroupId("ALL_USERS").send()

In this example a notification is sent to all users (via the Moqui automatic 'ALL_USERS' userGroupId) with the topic "TestTopic" and a message body in a Map or String object called 'messageMapOrJsonString'.

Useful methods on *NotificationMessage* (all return the same object for chaining unless noted):

-   **userId** / **userIds** / **userGroupId** — who should receive it
-   **topic** / **subTopic** — topic strings
-   **message** — JSON String or Map body
-   **title** / **link** — GString templates expanded from the message Map; fall back to *NotificationTopic* if empty
-   **type** — `info`, `success`, `warning`, or `danger`
-   **showAlert** / **alertNoAutoHide** — whether the client should show an alert
-   **persistOnSend** — persist and track received if true
-   **emailTemplateId** / **emailMessageSave** — optional email for users with emailNotifications=Y
-   **send()** or **send(boolean persist)** — publish
-   **getNotifyUserIds()** — users who will actually be notified (honors *NotificationTopicUser.receiveNotifications*)
-   **markSent** / **markViewed** — per-user tracking
-   **getWrappedMessageMap** / **getWrappedMessageJson** — payload sent to listeners (topic, sentDate, notificationMessageId, message, title, link, type, showAlert)

### NotificationTopic Entity

*moqui.security.user.NotificationTopic* configures defaults for a topic as an alternative to setting every option in code. Key fields: **topic** (PK), **description**, **titleTemplate**, **errorTitleTemplate** (used when type=danger), **linkTemplate**, **typeString**, **showAlert**, **alertNoAutoHide**, **persistOnSend**, **isPrivate**, **receiveNotifications**, **emailNotifications**, **emailTemplateId**, **emailMessageSave**.

Per-user overrides are *NotificationTopicUser* (**topic**, **userId**, **receiveNotifications**, **allNotifications**, **emailNotifications**). If a user has no *NotificationTopicUser.receiveNotifications* value, the topic's **receiveNotifications** is used; if that is also empty, the user is notified.

### NotificationMessageListener

Register a server-side listener with **ec.factory.registerNotificationMessageListener()**. The listener implements *org.moqui.context.NotificationMessageListener* (`init`, `destroy`, `onMessage`). The OOTB WebSocket bridge is *NotificationWebSocketListener*, which sends **getWrappedMessageJson()** to open sessions whose user is in **getNotifyUserIds()** and whose subscribed topics include the message topic or `ALL`.

### Code References

[ExecutionContext](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/java/org/moqui/context/ExecutionContext.java)
[NotificationMessage](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/java/org/moqui/context/NotificationMessage.java)
[NotificationMessageImpl](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/groovy/org/moqui/impl/context/NotificationMessageImpl.groovy)
[NotificationMessageListener](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/java/org/moqui/context/NotificationMessageListener.java)

## NotificationClient (JS client side)

*moqui.NotificationClient* in `MoquiLib.js` is a thin WebSocket client. It does not connect until **registerListener()** is called the first time. The `/apps` wrapper constructs it in HTML; `/vapps` and `/qapps` construct it on the Vue root (`WebrootVue.js` / `WebrootVue.qvt.js`) as:

    (location.protocol === 'https:' ? 'wss://' : 'ws://') + host + appRootPath + "/notws"

On open it sends `subscribe:` plus the registered topic names. Incoming JSON is dispatched to callbacks for that topic and for `ALL`. The default callback is **displayNotify**, which shows a growl-style alert when **title** is set and **showAlert** is true (`moqui.notifyNotification`). Both Vue roots register `ALL` on mount so topic alerts appear without extra screen code.

Example registration (from the comment in `MoquiLib.js`):

```
notificationClient.registerListener("ALL");
notificationClient.registerListener("MantleEvent", notificationClient.displayNotify);
```

For custom client handling (screen pop, modify state, and so on) pass your own function as the second argument to **registerListener**; it receives the wrapped message object (`topic`, `message`, `title`, `link`, `type`, `showAlert`, ...).

### Code References

[MoquiLib.js](https://github.com/moqui/moqui-runtime/blob/master/base-component/webroot/screen/webroot/js/MoquiLib.js)
[WebrootVue.js](https://github.com/moqui/moqui-runtime/blob/master/base-component/webroot/screen/webroot/js/WebrootVue.js)
[WebrootVue.qvt.js](https://github.com/moqui/moqui-runtime/blob/master/base-component/webroot/screen/webroot/js/WebrootVue.qvt.js)
[NotificationWebSocketListener](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/groovy/org/moqui/impl/webapp/NotificationWebSocketListener.groovy)
[NotificationEndpoint](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/groovy/org/moqui/impl/webapp/NotificationEndpoint.groovy)
