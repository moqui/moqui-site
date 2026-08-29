# Performance

[TOC levels={2-3}]

## Performance Metrics

### Artifact Hit Statistics

Moqui keeps statistics about use (hits) and timing for artifacts according to the configuration in the *server-stats.artifact-stats* elements in the Moqui Conf XML file. Here is the default configuration (in MoquiDefaultConf.xml) that you can override in the runtime conf file. The default development runtime conf file (MoquiDevConf.xml) has settings that record even more than this.
```
<server-stats bin-length-seconds="900" visit-enabled="true" visit-ip-info-on-login="true" visitor-enabled="true">
        <artifact-stats type="AT_XML_SCREEN" persist-bin="true" persist-hit="true"/>
        <artifact-stats type="AT_XML_SCREEN_CONTENT" persist-bin="true" persist-hit="false"/>
        <artifact-stats type="AT_XML_SCREEN_TRANS" persist-bin="true" persist-hit="true"/>
        <artifact-stats type="AT_SERVICE" persist-bin="true" persist-hit="false"/>
        <artifact-stats type="AT_ENTITY" persist-bin="false"/>
</server-stats>
```

These settings create a ArtifactHit record for each hit to a screen, screen-content (content under a screen), and screen transition. They also create *ArtifactHitBin* records for those plus service calls.

Here are a couple of examples of ArtifactHit records, the first for a hit to the *FindExample.xml* screen and the second for a hit to the *EntityExport.xml* transition in the *DataExport.xml* screen in the tools application. The hit to the *EntityExport.xml* transition has parameters which are recorded in the **parameterString** attribute.
```
<moqui.server.ArtifactHit lastUpdatedStamp="1519659626210" artifactType="AT_XML_SCREEN" hitId="120531" artifactSubType="text/html" runningTimeMillis="893.634543" userId="EX_JOHN_DOE" serverHostName="DEJCMBA3.local" startDateTime="1519659623359" visitId="100000" isSlowHit="N" artifactName="component://example/screen/ExampleApp/Example/FindExample.xml" requestUrl="http://localhost:8080/qapps/example/Example/FindExample" wasError="N" serverIpAddress="172.16.7.38"/>
```

```
<moqui.server.ArtifactHit  "visitId"="100001" "userId"="EX_JOHN_DOE" "artifactType"="transition" "artifactName"="component://tools/screen/Tools/Entity/DataExport.xml#EntityExport.xml" "parameterString"="moquiFormName=ExportData, output=file, filterMap=[artifactType:"screen"],entityNames=moqui.server.ArtifactHit" "startDateTime"="1519659645354" "runningTimeMillis"="45" "wasError"="N" "requestUrl"="http://localhost:8080/qapps/tools/Entity/DataExport" "serverIpAddress"="172.16.7.38" "serverHostName"="DEJCMBA3.local"
"lastUpdatedStamp"="1519659655367"/>
```

In a web application there is a Visit record for each session that has details about the session and ties together *ArtifactHit* records by the **visitId**. The Visit will keep track of the logged in **userId** once a user is logged in, but even before that visits are tied together using a **visitorId** that is tracked on the service in a Visitor record and in a browser/client with a cookie to tie sessions together, even if no user is logged in during a session.
```
<moqui.server.Visit serverHostName="DEJCMBA3.local" visitId="100000" serverIpAddress="172.16.7.38" initialLocale="en_US" clientHostName="0:0:0:0:0:0:0:1" clientIpAddress="0:0:0:0:0:0:0:1" lastUpdatedStamp="1518105351875" initialUserAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.39 Safari/537.36" sessionId="HZ672180F154294278BDDE614BEC24F815" userId="EX_JOHN_DOE" fromDate="1518105335387" webappName="ROOT" initialRequest="http://localhost:8080/" visitorId="100000"/>
```

There is a performance impact for creating a record for each hit on an artifact, and on busy servers the database size can get very large. This can be mitigated by using a low-latency insert database (the optional **moqui-orientdb** component is one example; it is not enabled by default, and entity groups without their own datasource use the transactional database, H2 in a typical local runtime). If you just want statistics of performance over a time period and don’t need the individual hit records for auditing or detailed analysis the *ArtifactHitBin* records will do the trick.

These records have a summary of hits for an artifact during a time period, between **binStartDateTime** and **binEndDateTime**. The length of the bin is configured with the server-stats.**bin-length-seconds** attribute and defaults to 900 seconds (15 minutes).

Here is an example of a hit bin for the **create#moqui.entity.EntityAuditLog** service. In this example it has been hit/used 77 times with a total (cumulative) run time of 252ms which means the average run time for the artifact in the bin is 3.27ms.
```
<moqui.server.ArtifactHitBin "hitBinId "="100010" "artifactType"="service" "artifactSubType"="entity-implicit" "artifactName"="create#moqui.entity.EntityAuditLog" "serverIpAddress"="172.16.7.38" "serverHostName"="DEJCMBA3.local" "binStartDateTime"="1518022242341" "binEndDateTime"="1518023142341" "hitCount"="16" "totalTimeMillis"="0.866639" "minTimeMillis"="0.017091" totalSquaredTime="0.074119" slowHitCount="0" "maxTimeMillis"="26.408371" "lastUpdatedStamp"="1518023202408"/>
```

These can be used directly from the database and with the **Artifact Hit Bins** and **Artifact Hit Summary** screens in the System application (`http://localhost:8080/qapps/system/ArtifactHitBins` and `.../ArtifactHitSummary`). The Tools app **Artifact Stats** screen (`http://localhost:8080/qapps/tools/ArtifactStats`) shows in-memory execution stats for the current process, not the persisted hit/bin tables.

### Artifact Execution Runtime Profiling

Java profilers such as JProfiler are great tools for analyzing the performance of Java methods but know nothing about Moqui artifacts such as screens, transitions, services, and entities. The Moqui Artifact Execution Facade keeps track of performance details of artifacts in memory for each instance (each ExecutionContext, such as a web request, etc) as they run.

This data is kept in the ArtifactExecutionInfo objects that are created as each artifact runs and are pushed onto the execution stack and kept in the execution history. You can access these using the ec.artifactExecution.**getStack**(), and ec.artifactExecution.**getHistory**() methods.

From the ArtifactExecutionInfo instance you can get its own runtime (long **getRunningTime**()), the artifact that called it (ArtifactExecutionInfo **getParent**()), the artifacts it calls (List&lt;ArtifactExecutionInfo&gt; **getChildList**()), the running time of all artifacts called by this artifact (long **getChildrenRunningTime**()), and based on that the running time of just this artifact (long **getThisRunningTime**(), which is **getRunningTime**() - **getChildrenRunningTime**()). You can also print a report with these stats for the current artifact info and optionally its children recursively using the **print**(Writer writer, int level, boolean children) method.

For a complex code section like placing an order that does dozens of service calls this can be a lot of data. To make it easier to track down the parts that are taking the most time have this method on the *ArtifactExecutionInfoImpl* class to generate a list of hot spots:
```
static List<Map> hotSpotByTime(List<ArtifactExecutionInfoImpl> aeiiList, boolean ownTime, String orderBy)
```
This goes through all *ArtifactExecutionInfoImpl* instances in the execution history and sums up stats to create a Map for each artifact with the following entries: *time*, *timeMin*, *timeMax*, *count*, *name*, *actionDetail*, *artifact type*, and *artifact action*.

Another situation where you’ll have a LOT of data is when running a process many times to get better average statistics. In this case you could have hundreds or thousands of artifact execution infos in the history. To consolidate data from multiple runs into a single tree of info about the execution of each artifact and its children use this method:
```
List<Map> consolidateArtifactInfo(List<ArtifactExecutionInfoImpl> aeiiList)
```
Each Map has these entries: *time*, *thisTime*, *childrenTime*, *count*, *name*, *actionDetail*, *childInfoList*, *key* (which is: name + ":" + typeEnumId + ":" + actionEnumId + ":" + actionDetail), type, and action. With that result you can print the tree with indentation in plain text (best displayed with a fixed width font) with this method:
```
String printArtifactInfoList(List<Map> infoList)
```

One example of using these methods is the *TestOrders.xml* screen in the POP Commerce application. It is used with a URL like this and displays a screen with the performance profile results of the code that places and ships the specified number of orders (POP Commerce is mounted at `/popc` under webroot, not under `/qapps`):

http://localhost:8080/popc/TestOrders?numOrders=10

Here is a snippet from the screen actions script that runs the test code and gets the performance statistics using the methods described above:
```
def artifactHistory = ec.artifactExecution.history ownHotSpotList = ArtifactExecutionInfoImpl.hotSpotByTime(artifactHistory, true, "-time")
totalHotSpotList = ArtifactExecutionInfoImpl.hotSpotByTime(artifactHistory, false, "-time")

List<Map> consolidatedList = ArtifactExecutionInfoImpl.consolidateArtifactInfo(artifactHistory)
String printedArtifactInfo = ArtifactExecutionInfoImpl.printArtifactInfoList(consolidatedList)
```

Here is an example of the top few rows in the **Artifacts by Own Time** section of the output on that screen for the placing and shipping of 25 orders:
  
|    Time  |   Time Min |   Time Avg    |  Time Max   |   Count  |       Name                        |       Type  |    Action    |    Action Detail  |
|------|-----|-------|-----|-----|-------------------------------|---------|--------|------|
| 1838 | 0   | 2.29  | 25  | 801 | mantle.order.OrderItem        | Entity  | View   | list |
| 1093 | 0   | 1.32  | 26  | 825 | mantle.ledger.account.GlAccountOrgTimePeriod         | Entity  | Update |      |
| 1025 | 0   | 1.08  | 10  | 950 | moqui.entity.EntityAuditLog   | Entity  | Create |      |
| 844  | 7   | 11.25 | 33  | 75  | mantle.product.PriceServices.get#ProductPrice              | Service | All    |      |
| 686  | 0   | 3.43  | 12  | 200 | mantle.order.OrderPart        | Entity  | Update |      |

From these results we can see that the most time is spent doing an Entity View (find) list operation on the OrderItem entity. In this run the transaction cache for the **place#Order** and **ship#OrderPart** services was disabled, and the OrderItem entity is not cached using the entity cache so it is doing that query 801 times during this run. The transaction cache is a write-through cache that will cache written records and reads like this. With that enabled overall the orders per second goes from around 0.8 to 1.4 (historical numbers from a laptop with an embedded SQL database) and the output for **Artifacts by Own Time** looks very different:

|    Time  |   Time Min |   Time Avg    |  Time Max   |   Count  |       Name                        |       Type  |    Action    |    Action Detail  |
|------|-----|--------|-----|-----|-------------------------------|---------|------|------|
| 3449 | 72  | 137.96 | 222 | 25  | mantle.shipment.ShipmentServices.ship#OrderPart                | Service | All  |      |
| 1284 | 0   | 1.60   | 10  | 801 | mantle.order.OrderItem        | Entity  | View | list |
| 679  | 6   | 9.05   | 14  | 75  | mantle.product.PriceServices.get#ProductPrice              | Service | All  |      |
| 614  | 14  | 24.56  | 51  | 25  | mantle.order.OrderServices.place#Order                   | Service | All  |      |
| 561  | 0   | 0.68   | 5   | 825 | mantle.ledger.account.GlAccountOrgTimePeriod         | Entity  | View | one  |

Below is some sample output from the **Consolidated Artifacts Tree** section. It shows the hierarchy of artifacts consolidated across runs and within each run to show the data for each artifact in the context of parent and child artifacts. When interpreting these results note that the total counts and times for each artifact are not just the values for that artifact running as a child of the parent artifact shown, but all runs of that artifact. The main value is tracking down where the busiest artifacts are used, and understanding exactly what is actually done at runtime, especially for specific services.

In this output each line is formatted as follows:
```
[${time}:${thisTime}:${childrenTime}][${count}] ${type} ${action} ${actionDetail} ${name}
```
Here is the sample output, note that certain artifact names have been shortened with ellipses for better formatting:
```
[ 16: 3: 13][ 2] Screen View component://webroot/screen/webroot.xml
| [ 13:-41: 54][ 3] Screen View component://PopCommerce/…/PopCommerceRoot.xml
| | [ 165:165: 0][126] Entity View one mantle.product.store.ProductStore
| | [ 0:-31263:31263][ 3] Screen View component://PopCommerce/…/TestOrders.xml
| | | [ 3: 3: 0][ 3] Entity View one moqui.security.UserAccount
| | | [ 5: 5: 0][ 1] Entity View one moqui.server.Visit
| | | [ 6: 1: 5][ 1] Service Create create#moqui.security.UserLoginHistory
| | | | [ 5: 5: 0][ 1] Entity Create moqui.security.UserLoginHistory
| | | [ 4700:269:4431][ 75] Service All …OrderServices.add#OrderProductQuantity
| | | | [ 632:632: 0][300] Entity View list mantle.order.OrderPart
| | | | [ 497:497: 0][375] Entity View one mantle.order.OrderPart
| | | | [ 165:165: 0][126] Entity View one mantle.product.store.ProductStore
| | | | [ 195:195: 0][ 25] Entity View list mantle.order.OrderHeaderAndPart
| | | | [ 328: 21:307][ 25] Service Create mantle.order.OrderServices.create#Order
| | | | | [ 146: 12:134][ 25] Service Create create#mantle.order.OrderHeader
| | | | | | [ 134: 97: 37][ 25] Entity Create mantle.order.OrderHeader
| | | | | | | [ 1564:406:1158][950] Service Create create#moqui.entity.EntityAuditLog
| | | | | | | | [ 83: 83: 0][ 30] Entity View one moqui.entity.SequenceValueItem
| | | | | | | | [ 90: 90: 0][ 30] Entity Update moqui.entity.SequenceValueItem
| | | | | | | | [ 1025:1025: 0][950] Entity Create moqui.entity.EntityAuditLog
| | | | | [ 161: 11:150][ 25] Service Create create#mantle.order.OrderPart
| | | | | | [ 632:632: 0][300] Entity View list mantle.order.OrderPart
| | | | | | [ 134: 99: 35][ 25] Entity Create mantle.order.OrderPart
| | | | | | | [ 1564:406:1158][950] Service Create create#moqui.entity.EntityAuditLog
| | | | | | | | [ 83: 83: 0][ 30] Entity View one moqui.entity.SequenceValueItem
| | | | | | | | [ 90: 90: 0][ 30] Entity Update moqui.entity.SequenceValueItem
| | | | | | | | [ 1025:1025: 0][950] Entity Create moqui.entity.EntityAuditLog
| | | | [ 1838:1838: 0][801] Entity View list mantle.order.OrderItem
| | | | [ 882:844: 38][ 75] Service All …PriceServices.get#ProductPrice
| | | | | [ 38: 38: 0][150] Entity View list mantle.product.ProductPrice
| | | | [ 2324: 83:2241][ 75] Service Create …OrderServices.create#OrderItem
| | | | | [ 430:430: 0][575] Entity View one mantle.product.Product
| | | | | [ 2747: 64:2683][100] Service Create create#mantle.order.OrderItem
| | | | | | [ 1838:1838: 0][801] Entity View list mantle.order.OrderItem
| | | | | | [ 2482:384:2098][100] Entity Create mantle.order.OrderItem
| | | | | | | [ 1564:406:1158][950] Service Create create#moqui.entity.EntityAuditLog
| | | | | | | | [ 83: 83: 0][ 30] Entity View one moqui.entity.SequenceValueItem
| | | | | | | | [ 90: 90: 0][ 30] Entity Update moqui.entity.SequenceValueItem
| | | | | | | | [ 1025:1025: 0][950] Entity Create moqui.entity.EntityAuditLog
| | | | | | | [ 1784: 89:1695][100] Service Update …OrderServices.update#OrderPartTotal
| | | | | | | | [ 1838:1838: 0][801] Entity View list mantle.order.OrderItem
| | | | | | | | [ 322:127:195][250] Service All …OrderServices.get#OrderItemTotal
| | | | | | | | | [ 1838:1838: 0][801] Entity View list mantle.order.OrderItem
| | | | | | | | [ 497:497: 0][375] Entity View one mantle.order.OrderPart
| | | | | | | | [ 1204:686:518][200] Entity Update mantle.order.OrderPart
| | | | | | | | | [ 224:224: 0][200] Entity View refresh mantle.order.OrderPart
| | | | | | | | | [ 1564:406:1158][950] Service Create create#…EntityAuditLog
| | | | | | | | | | [ 83: 83: 0][ 30] Entity View one moqui.entity.SequenceValueItem
| | | | | | | | | | [ 90: 90: 0][ 30] Entity Update moqui.entity.SequenceValueItem
| | | | | | | | | | [ 1025:1025: 0][950] Entity Create moqui.entity.EntityAuditLog
| | | | | | | | [ 629: 56:573][100] Service Update …update#OrderHeaderTotal
| | | | | | | | | [ 632:632: 0][300] Entity View list mantle.order.OrderPart
| | | | | | | | | [ 349:349: 0][450] Entity View one mantle.order.OrderHeader
| | | | | | | | | [ 884:592:292][175] Entity Update mantle.order.OrderHeader
| | | | | | | | | | [ 181:181: 0][175] Entity View refresh mantle.order.OrderHeader
| | | | | | | | | | [ 1564:406:1158][950] Service Create create#…EntityAuditLog
| | | | | | | | | | | [ 83: 83: 0][ 30] Entity View one …SequenceValueItem
| | | | | | | | | | | [ 90: 90: 0][ 30] Entity Update …SequenceValueItem
| | | | | | | | | | | [ 1025:1025: 0][950] Entity Create moqui.entity.EntityAuditLog
```

## Improving Performance

Once an artifact or code block has been identified as taking up a lot of execution time the next step is to review it and see if any part of it can be improved. Sometimes operations just take time and there isn’t much to be done about it. Even in those cases parts can be made asynchronous or other approaches used to at least minimize the impact on users or system resources.

The slowest operations typically involve database or file access and in-memory caching can help a lot with this. The Moqui Cache Facade is used by various parts of the framework and can be used directly by your code for caching as needed. By default Moqui uses **MCache** (`org.moqui.jcache.MCache`), a JCache (JSR-107, `javax.cache`) implementation. Size limits, timeouts, and eviction strategy are set on `cache-list.cache` elements in the Moqui Conf XML file. There is no ehcache.xml file. For distributed caching in a cluster set `cache-list.@distributed-factory` (the default is also MCache, which is local-only); the optional **moqui-hazelcast** component provides a distributed factory.

In the runtime configuration for development (*MoquiDevConf.xml*) the caches for artifacts such as entities, service definitions, XML Screens, scripts, and templates have a short timeout so that they are reloaded frequently for testing after changing a file. In the production configuration (*MoquiProductionConf.xml*) the caches are all used fully to get the best performance. When doing performance testing make sure you are running with the caches fully used, i.e. with production settings, so that numbers are not biased by things that are quite slow and won’t happen in production.

The Resource Facade does a lot of caching. The **getLocationText**(String location, boolean cache) method uses the *resource.text.location* cache if the cache parameter is set to true. Other caches are always used including scripts and templates in their compiled form (if possible with the script interpreter or template renderer), and even the Groovy expressions and string expansions done by the Resource Facade. As mentioned above these are never "disabled" but to facilitate runtime reloading the easiest approach is to use a timeout on the desired caches.

Another common cache is the entity cache managed by the Entity Facade. There are caches for individual records, list results, and count results. These caches are cleared automatically when records are created, updated, or deleted through the Entity Facade. Both simple entities that correspond to a single table and view entities can be cached, and the automatic cache clearing works for both. To make cache clearing more efficient it uses a reverse association cache by default to lookup cache entries by the entity name and PK values of a record. In other cases (such as when creating a record) it must do a scan of the conditions on cache entries to find matching entries to clear, especially on list and count caches. For more details see the **Data and Resources** chapter.

In addition to the entity read cache there is a write-through per-transaction cache that can be enabled with the service.**transaction** attribute by setting it to cache or force-cache. The implementation of this is in the *TransactionCache.groovy* file.

The basic idea is that when creating, updating, or deleting a record it just remembers that in an object that is associated with the transaction instead of actually writing it to the database. When the transaction is committed, but before the actual commit, it writes the changes to the database. When find operations are done it uses the values in cache directly or augments the query results from the database with values in the cache.

It is even smart enough to know when finding with a constraint that could only match values in the TX cache (created through it) that there is no need to go to the database at all and the query is handled fully in memory. For example if you create a OrderHeader record and then various OrderItem records and then query all OrderItem records by **orderId** it will see if the OrderHeader record was created through the transaction cache and if so it will just get the OrderItem records from the TX cache and not query the database at all for them.

For entity find operations another valuable tool is the auto-minimize of view entities. When you do a find on a large view-entity, such as the FindPartyView entity, just make sure to specify the fields to select and limit those to only the fields you need. The Entity Facade will automatically look at the fields selected, used in conditions, and used to order/sort the results and only include the aliased fields and member entities necessary for those fields. With this approach there is no need to use a dynamic view entity (EntityDynamicView) to conditionally add member entities and aliased fields. Back to the FindPartyView example, the **find#Party** service (implemented in findParty.groovy) uses this to provide a large number of options with very minimal code.

A general guideline when querying tables with a very large number of records is to not ask the database to do more than is absolutely necessary. Joining in too many member entities in a view entity is a dramatic form of this as creating large temporary tables is a very expensive operation.

Along these lines another common scenario is doing a find that may return a very large number of results and then showing those results one page (like 20 records) at a time. It is best to not select all the data you’ll display for each record in the main query as this makes the temporary table for joins much larger, and you are asking the database to get that data for all records instead of just the 20 or so you will be displaying. A better approach is to just query the field or fields sufficient to identify the records, then query the data to display for just those keys in a separate find. This is usually much faster, but in some rare cases it is not so it is still good to test these and other query variations with real data to see which performs best for your specific scenario.

In high volume production ecommerce and ERP systems another common problem is synchronization and locking delays. These can happen within the app server with Java synchronization, or in a database with locks and lock waiting. You may also find deadlocks, but that is another issue (i.e., separate from performance). The only way to really find these is with load testing, especially load testing that uses the same resources as much as possible like a bunch of orders for the same product as close to the same time as possible.

There are a few ways to improve these. On the Java synchronization level using non-blocking algorithms and data structures can make a huge difference, and many libraries are moving this way. *Java Concurrency in Practice* by Brian Goetz is a good book on this topic.

Beyond these basic things to keep in mind there are countless ways to improve performance. For really important code, especially highly used or generally performance sensitive functionality, within reasonable constraints the only limit to how much faster it can run is often a matter of how much time and effort can be put into performance testing and optimization.

Sometimes this involves significant creativity and using very different architectures and tools to handle things like a large number of users, a very large amount of data, data scattered in many places, and so on. For some of these issues distributed processing or data storage tools such as Hadoop or a dedicated NoSQL store (and really countless others these days) may be just what you need, even if using them requires significantly more effort and it only makes sense to do so for very specific functionality.

When doing Java profiling with a tool like JProfiler you are usually looking for different sorts of things that impact performance than when looking at Moqui artifact execution performance data. To optimize Java methods (and classes for memory use) there are different tools and guidelines to use than the ones above which are more for optimizing business logic at a higher level.
