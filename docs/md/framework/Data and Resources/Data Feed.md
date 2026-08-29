# Data Feed

A Data Feed is a configurable way to push Data Documents to a service or group multiple documents for retrieval through an API call. There service to call is specified in the *feedReceiveServiceName* field and should implement the `org.moqui.EntityServices.receive#DataFeed` service interface. The main input parameter is the *documentList* which will have a List of Maps representing each DataDocument instance to process when received. See the service interface definition for more details:

[framework/service/org/moqui/EntityServices.xml](https://github.com/moqui/moqui-framework/blob/master/framework/service/org/moqui/EntityServices.xml)

The example below is a push feed (**dataFeedTypeEnumId**="DTFDTP_RT_PUSH") to send documents to the `HiveMind.SearchServices.indexAndNotify#HiveMindDocuments` service when any data in any of the documents is changed in the database through the Moqui Entity Facade. The framework automatically keeps track of push Data Feeds and the entities that are part of the Data Documents associated with them to look for changes as create, update, and delete operations are done. This is an efficient way to get updated Data Documents in real time.

Here is an example of *entity-facade-xml* for the records to configure a push Data Feed:
```
<moqui.entity.feed.DataFeed dataFeedId="HiveMindSearch" dataFeedTypeEnumId="DTFDTP_RT_PUSH" feedName="HiveMind Search" feedReceiveServiceName="HiveMind.SearchServices.indexAndNotify#HiveMindDocuments"/> 

<moqui.entity.feed.DataFeedDocument dataFeedId="HiveMindSearch" dataDocumentId="HmProject"/>

<moqui.entity.feed.DataFeedDocument dataFeedId="HiveMindSearch" dataDocumentId="HmTask"/>
```
Each *DataFeedDocument* record associates a *DataDocument* record to the *DataFeed* record to be included in the feed.

On a side note, when you have data you want to index that is loaded through a XML data file as part of the load process and it may be loaded before the Data Feed is loaded an activated, you can include an element for a *ServiceTrigger* record and the *Service Facade* will call the service during the load process to index for the feed. Here is an example of that:
```
<moqui.entity.ServiceTrigger serviceTriggerId="HM_SEARCH_INIT" statusId="SrtrNotRun" mapString="[dataFeedId:'HiveMindSearch']"
serviceName="org.moqui.impl.EntityServices.index#DataFeedDocuments"/>
```

The DataFeed example above is for a push Data Feed. To setup a feed for manual pull just set **dataFeedTypeEnumId**="DTFDTP_MAN_PULL" on the *DataFeed* record. Any type of Data Feed can be retrieved manually, but with this type the feed will not be automatically run. To get the documents for any feed through the API use a statement like this:
```
List<Map> docList = ec.entity.getDataFeedDocuments(dataFeedId, fromUpdateStamp, thruUpdatedStamp)
```
