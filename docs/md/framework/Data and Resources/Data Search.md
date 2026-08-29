# Data Search

The Data Search feature in Moqui Framework is based on ElasticSearch (<http://www.elasticsearch.org>). This is a distributed text search tool based on *Apache Lucene*. ElasticSearch uses JSON documents as the artifact to search, and each named field in a JSON document is a facet for searching. The *Data Document* feature produces documents with 4 special fields that ElasticSearch uses, as described in the Data Document section (**_index**, **_type**, **_id**, and **_timestamp**).

There are two main touch points for Data Search: **indexing** and **searching**. The service for indexing in the framework is `org.moqui.search.SearchServices.index#DataFeedDocuments`. This service implements the `org.moqui.EntityServices.receive#DataFeed` interface and accepts all parameters from the interface but only uses the **documentList** parameter, which is the list of Data Documents to index with ElasticSearch.

It also has one other parameter, **getOriginalDocuments**, which when set to true the service will populate and return **originalDocumentList**, a list of the previously indexed version of any matching existing documents from ElasticSearch. The service always returns a **documentVersionList** parameter with a list of the version number for each document in the original list after the index is done to show how many times each document has been updated in the index.

The example in the previous section used an application-specific service to receive the push Data Feed, so here is an example of a push Data Feed configuration that uses the indexing service that is part of the framework:

```
<moqui.entity.feed.DataFeed dataFeedId="PopCommerceSearch" dataFeedTypeEnumId="DTFDTP_RT_PUSH" feedName="PopCommerce Search"
feedReceiveServiceName="org.moqui.search.SearchServices.index#DataFeedDocuments"/> 

<moqui.entity.feed.DataFeedDocument dataFeedId="PopCommerceSearch" dataDocumentId="PopcProduct"/>
```

You can also use the ElasticSearch API directly to index documents, either Data Documents produced by the Entity Facade or any JSON document you want to search. For more complete information see the ElasticSearch documentation. Here is an example of indexing a JSON document in nested Map form with the **_index**, **_type**, and **_id** entries set:

```
IndexResponse response = ec.elasticSearchClient.prepareIndex(document._index, document._type, document._id).setSource(document).execute().actionGet()
```

To search Data Documents use the `org.moqui.search.SearchServices.search#DataDocuments` service, like this:

```
<service-call name="org.moqui.search.SearchServices.search#DataDocuments" out-map="context" in-map="context + [indexName:’popc’]"/>
```

Note that in this example the **queryString**, **pageIndex**, and **pageSize** parameters come from the search form and get into the context from request parameters. The parameters for this service are:

-   **queryString**: the search query string that will be passed to the Lucene classic query parser, for documentation see: [**http://lucene.apache.org/core/4\_8\_1/queryparser/org/apache/lucene/queryparser/classic/package-summary.html**](http://lucene.apache.org/core/4_8_1/queryparser/org/apache/lucene/queryparser/classic/package-summary.html)
-   **documentType**: the ElasticSearch document type, matches the **_type** field in the document and the DataDocument.**dataDocumentId**; examples of this from previous sections include PopcProduct and HmProject
-   **pageIndex**, **pageSize**: these are the standard pagination parameters for Moqui XML list forms so this service can be easily used with them; only **pageSize** results will be returned and starting at the **pageIndex** \* **pageSize** index in the results
-   **flattenDocument**: default false, if set to true each document in the form of a nested Map result (object form, JSON document being the text form) will be flattened into a single flat Map with name/value pairs taken from all of the nested Maps and Lists of Maps; later values in the document will override earlier values if the same Map entry key is found more than once (see the StupidUtilities.**flattenNestedMap**() method)

The service returns a **documentList** parameter, which is a List of Maps, each Map representing a Data Document. It also returns the various **documentList\*** parameters that are part of the pagination pattern for Moqui XML list forms (\*Count, \*PageIndex, \*PageSize, \*PageMaxIndex, \*PageRangeLow, and \*PageRangeHigh). These are used when rendering a list form, and can be used for other purposes where useful as well.

In addition to this service you can also retrieve results directly through the ElasticSearch API. Note that there are two main steps, the search to get back the 3 identifying fields of each document, and then a multi-get to get all of the documents. In this example we get each document as a Map (the **getSourceAsMap**() method), and the ElasticSearch API also supports getting each as a JSON document (the **getSourceAsString**() method).

```
SearchHits hits =
ec.elasticSearchClient.prepareSearch().setIndices(indexName).setTypes(documentType).setQuery(QueryBuilders.queryString(queryString)).setFrom(fromOffset).setSize(sizeLimit).execute().actionGet().getHits()
if (hits.getTotalHits() > 0) {
    MultiGetRequestBuilder mgrb = ec.elasticSearchClient.prepareMultiGet()
    for (SearchHit hit in hits) 
          mgrb.add(hit.getIndex(), hit.getType(), hit.getId())
    Iterator mgirIt = mgrb.execute().actionGet().iterator()
    while(mgirIt.hasNext()) {
        MultiGetItemResponse mgir = mgirIt.next()
        Map document = mgir.getResponse().getSourceAsMap()
        documentList.add(document)
    }
}
```
In addition to *indexing* and *searching* another aspect of *ElasticSearch* to know about is the deployment options. By default Moqui Framework has an embedded node of ElasticSearch running in the same JVM for fast, convenient access. A remote ElasticSearch server can also be used.

The easiest distributed deployment mode is to have each Moqui application server be a node in the ElasticSearch cluster, and if you have separate ES nodes with actual search data persisted on them then set the app server ES nodes to not persist any data. With that approach results may be aggregated on the app servers, but actual searches against index data will be done on the other servers in the cluster.
