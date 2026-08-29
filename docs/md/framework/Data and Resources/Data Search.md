# Data Search

[TOC levels=2-4]

The Data Search feature in Moqui Framework is based on **OpenSearch** (recommended) or ElasticSearch 7.x-compatible REST APIs. This is a distributed text search tool based on *Apache Lucene*. It uses JSON documents as the artifact to search, and each named field in a JSON document is a facet for searching. The *Data Document* feature produces documents with special fields used when indexing, as described in the Data Document section (**_index**, **_type**, **_id**, and **_timestamp**).

The search engine runs as a **separate process**, not as an embedded node in the Moqui JVM. The framework HTTP client is `ec.elastic` (`org.moqui.context.ElasticFacade`). `ec.elastic.getDefault()` is the `default` cluster configured in `elastic-facade.cluster`; `ec.elastic.getClient(clusterName)` (or `ec.factory.elastic.getClient(clusterName)`) selects a named cluster. The default cluster URL is the `elasticsearch_url` property (`http://127.0.0.1:9200`).

> **NOTE:** Older examples used `ec.elasticSearchClient.prepareIndex(...)` / `prepareSearch(...)` and an ElasticSearch node in the same JVM. That client and the in-JVM node are gone.

There are two main touch points for Data Search: **indexing** and **searching**.

## Indexing

For real-time indexing, configure a push Data Feed whose **feedReceiveServiceName** implements the `org.moqui.EntityServices.receive#DataFeed` interface. If that field is empty, the framework defaults to `org.moqui.search.SearchServices.index#DataDocuments`. That service accepts the interface parameters and uses the **documentList** of Data Documents to index. It also has **verifyIndexes** (default true) and **clusterName** (default `default`). It does not return document versions or previously indexed documents.

The example in the previous section used an application-specific service to receive the push Data Feed. Here is a push Data Feed that uses the indexing service in the framework (this is the POP Commerce search feed):

```
<moqui.entity.feed.DataFeed dataFeedId="PopCommerceSearch" dataFeedTypeEnumId="DTFDTP_RT_PUSH" feedName="PopCommerce Search"
feedReceiveServiceName="org.moqui.search.SearchServices.index#DataDocuments"/>

<moqui.entity.feed.DataFeedDocument dataFeedId="PopCommerceSearch" dataDocumentId="PopcProduct"/>
```

To (re)index all documents associated with a feed in a date range, call `org.moqui.search.SearchServices.index#DataFeedDocuments`. That service looks up the feed’s Data Documents, creates indexes as needed, and feeds batches to **feedReceiveServiceName** (or `index#DataDocuments` if that field is empty). The `IndexDataFeedDocuments` service job calls this service.

You can also use the ElasticFacade API directly to index documents, either Data Documents produced by the Entity Facade or any JSON document (as a Map) you want to search. For a single document:

```
ec.elastic.getDefault().index(index, id, document)
```

For a list of Data Documents that already have **_index**, **_type**, **_id**, and **_timestamp** entries, use:

```
ec.elastic.getDefault().bulkIndexDataDocument(documentList)
```

`index#DataDocuments` calls that method after `verifyDataDocumentIndexes(documentList)` when **verifyIndexes** is true.

`bulkIndexDataDocument` does **not** send **_index**, **_type**, **_id**, or **_timestamp** in the stored document source. ElasticSearch 7+ and OpenSearch allow one document type per index, so the actual index name is derived from **_type** (the DataDocument **dataDocumentId**, converted to a valid lowercase index name). **_index** (DataDocument **indexName**) is an alias for those per-document indexes. **_type** is kept on the Data Document Map for that legacy reason; it is not sent as an OpenSearch/ElasticSearch `_type` on current servers.

## Searching

To search Data Documents use the `org.moqui.search.SearchServices.search#DataDocuments` service, like this:

```
<service-call name="org.moqui.search.SearchServices.search#DataDocuments" out-map="context" in-map="context + [indexName:'popc']"/>
```

In this example the **queryString**, **pageIndex**, and **pageSize** parameters come from the search form and get into the context from request parameters. The parameters for this service are:

-   **indexName**: required; the DataDocument **indexName** (alias) to search, unless **documentType** is set as described below
-   **queryString**: the search query string, passed as an OpenSearch/ElasticSearch `query_string` query; see [Query string queries](https://docs.opensearch.org/latest/query-dsl/full-text/query-string/) (ElasticSearch-compatible: [query_string query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html))
-   **documentType**: the DataDocument **dataDocumentId** (the document **_type**). When set, the search uses the per-document-type index name(s) derived from it instead of **indexName**. Comma-separated values are allowed.
-   **pageIndex**, **pageSize**: the standard pagination parameters for Moqui XML list forms so this service can be used with them; only **pageSize** results are returned, starting at **pageIndex** \* **pageSize**
-   **flattenDocument**: default **true**; if true each document (a nested Map) is flattened into a single Map with name/value pairs taken from all nested Maps and Lists of Maps; later values override earlier values if the same key is found more than once (see `org.moqui.util.CollectionUtilities.flattenNestedMap()`)
-   **clusterName**: ElasticFacade cluster name, default `default`
-   **nestedQueryMap**, **orderByFields**, **highlightFields**, **pageNoLimit**: optional constraints, sort, highlighting, and “no pagination” (capped at 10,000 hits)

The service returns a **documentList** parameter, which is a List of Maps, each Map representing a Data Document (with **_index**, **_id**, **_type**, and **_version** filled from the hit). It also returns the **documentList\*** pagination parameters used by Moqui XML list forms (\*Count, \*PageIndex, \*PageSize, \*PageMaxIndex, \*PageRangeLow, and \*PageRangeHigh).

You can also search directly through ElasticFacade. Hits already include `_source`; a separate multi-get is not required:

```
Map searchMap = [query:[query_string:[query:queryString, lenient:true]], from:fromOffset, size:sizeLimit]
List hits = ec.elastic.getDefault().searchHits(index, searchMap)
for (Map hit in hits) {
    Map document = (Map) hit._source
    document._index = hit._index
    document._id = hit._id
    documentList.add(document)
}
```

To fetch one stored document by id: `ec.elastic.getDefault().getSource(index, id)`.

## Deployment

By default Moqui talks to an external OpenSearch (or ElasticSearch 7.x-compatible) process at `http://127.0.0.1:9200`. If `runtime/opensearch` exists, MoquiStart starts and stops that OpenSearch process with the app server (`runtime/elasticsearch` is the same idea for ElasticSearch). Pass `no-run-es` to skip that. Point the client at another host with the `elasticsearch_url` (or `elasticsearch_host1`) property and, if needed, `elasticsearch_user` / `elasticsearch_password`.

Application servers are HTTP clients of that cluster. They are not ElasticSearch cluster nodes and do not persist index data in the Moqui JVM.
