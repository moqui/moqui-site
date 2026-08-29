# The Tools Application

The Tools and System applications are both part of the default Moqui runtime and live in the base-component at `runtime/base-component/tools`. They are two separate apps under the default UI:

- Tools: `http://localhost:8080/qapps/tools/...`
- System: `http://localhost:8080/qapps/system/...`

**Tools** is for development and data work: viewing and editing entity data, running services, an interactive Groovy shell, and local performance/stats screens.

- [Auto Screen](/docs/framework/The+Tools+Application/Auto+Screen)
- [Data View](/docs/framework/The+Tools+Application/Data+View)
- [Entity Tools](/docs/framework/The+Tools+Application/Entity+Tools) (Data Edit, Import, Export, Snapshots, SQL Runner, Speed Test, Query Stats, Table Stats)
- Service (run, reference, load runner)
- Groovy Shell (xterm.js UI over a `GroovyShell` WebSocket; requires the `GROOVY_SHELL_WEB` permission)
- Artifact Stats (in-memory execution stats for this process)
- Status Flows

**System** is for administration: security, jobs, cache, localization, documents, visits, and persisted artifact hits.

- Cache
- Localization
- Service Jobs
- Instance
- Security (users, groups, artifact groups; TOTP, email, SMS, and backup-code factors)
- Data Document
- Artifact Hit Summary / Artifact Hit Bins, Audit Log, Visits
- System Messages, Entity Sync, Resource Finder
- System Information (dashboard: runtime version, heap, datasources, Elastic/OpenSearch clients)

This section documents Auto Screen, Data View, and Entity Tools. Other Tools and System screens are available in the running apps; they are not each given a full page here.
