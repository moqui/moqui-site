# System Message

## Introduction

The System Message functionality in Moqui Framework handles message queuing and processing for both incoming and outgoing messages.

- message queue for store and send for outgoing messages, and store and process for incoming messages
- failure and retry handling with automatic retry via configurable service jobs
- full history of incoming and outgoing messages for auditing, debugging, reprocessing, etc
- UI in the System app (`http://localhost:8080/qapps/system/SystemMessage`) to find, view, update, and manually retry sending and processing of messages
- configuration on *SystemMessageType* for the services to use for producing, sending, receiving, and processing messages
- configuration on *SystemMessageRemote* for remote connection parameters (usage varies by transport method)
- generic endpoint to receive incoming messages over HTTP at `/rest/sm/{systemMessageTypeId}/{systemMessageRemoteId}/{remoteMessageId}` (calls **org.moqui.impl.SystemMessageServices.receive#IncomingSystemMessage**)
- generic JSON over HTTP send and receive services
- SFTP outgoing message drop and incoming message pick up support in the optional **moqui-sftp** component

## Recommended Practices

### Incoming Messages

- always store original text from external system
- avoid interim data structures; for reusable code used for multiple incoming file formats use a service with nested parameters and transform code to nested Map+List structures for the service call (not to persist or use otherwise)
- large messages with multiple entries (transactions, etc):
    - if you can use database data to determine that an entry has already been processed, you may process the entire message at once using a check of each entry for retries until all are done
    - if there is no way to query the DB to see if done then process a large message by splitting into one *SystemMessage* record per entry so success/failure/retry is tracked for each

### Outgoing Messages

- for each integration define:
    - what needs to be sent (for example which orders)
    - which SystemMessageType and SystemMessageRemote to use (this may be configurable)
- check for existing *SystemMessage* record by the primary ID (such as orderId), *SystemMessageRemote* and/or *SystemMessageType*
    - in other words rely on data for one and only one message, don't rely on code (ECA rules, service calls, etc)
- once message text is generated, queue for sending using the **org.moqui.impl.SystemMessageServices.queue#SystemMessage** service
    - this service creates the *SystemMessage* record in a new transaction (status Produced) and by default tries to send immediately using the configured send service; set **sendNow** to false to wait for the send job
    - commit any related data the send service will read before calling **queue#SystemMessage**, because send runs in a separate transaction (and may run asynchronously)
