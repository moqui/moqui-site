# Notification and WebSocket
The Notification functionality in Moqui Framework is a user and topic based publish/subscribe tool that can be used to push notifications to server code by direct topic subscription or client applications by WebSocket. Other interfaces for client applications could be built for anything you'd like but the current OOTB implementation for this is WebSocket based and meant for notifications, screen pops, etc in web-based client applications.

## NotificationMessage (server side)

The NotificationMessage interface in the Moqui Framework API is the primary object for generating notifications for one or more users and with a specific topic. The topic for a Notification is an arbitrary string identifier to distinguish different types of messages so that listeners (server side or client side) can listen for just the topics they know how to handle.

To generate a message first use the ExecutionContext.makeNotificationMessage() method which returns a NotificationMessage object. On that object call methods as needed to set the topic, title, type (info, success, warning, danger), message (Map or JSON body), and specify the user(s) and/or user groups that should receive the notification. For example:

    ec.makeNotificationMessage().topic("TestTopic").type("info").title("Test notification message")
            .message(messageMapOrJsonString).userGroupId("ALL_USERS").send()

In this example a notification is sent to all users (via the Moqui automatic 'ALL_USERS' userGroupId) with the topic "TestTopic" and a message body in a Map or String object called 'messageMapOrJsonString'.

TODO: reference for all methods on NotificationMessage interface

### NotificationTopic Entity

TODO general description, use to configure defaults for a topic as alternative to setting options in code

TODO: reference for all fields on NotificationTopic entity

### NotificationMessageListener

TODO ec.factory.registerNotificationMessageListener()

### Code References

[ExecutionContext](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/java/org/moqui/context/ExecutionContext.java)
[NotificationMessage](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/java/org/moqui/context/NotificationMessage.java)
[NotificationMessageImpl](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/groovy/org/moqui/impl/context/NotificationMessageImpl.groovy)
[NotificationMessageListener](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/java/org/moqui/context/NotificationMessageListener.java)

## NotificationClient (JS client side)

TODO general description and how it works

TODO example JavaScript to use for displaying a growl style notification
TODO example JavaScript to use for custom client handling (screen pop, modify state, etc)

### Code References

[MoquiLib.js](https://github.com/moqui/moqui-runtime/blob/master/base-component/webroot/screen/webroot/js/MoquiLib.js)
[WebrootVue.js](https://github.com/moqui/moqui-runtime/blob/master/base-component/webroot/screen/webroot/js/WebrootVue.js)
[NotificationWebSocketListener](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/groovy/org/moqui/impl/webapp/NotificationWebSocketListener.groovy)
[NotificationEndpoint](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/groovy/org/moqui/impl/webapp/NotificationEndpoint.groovy)
