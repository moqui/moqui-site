# Service Jobs

Moqui provides support to configure ad-hoc (explicitly executed) or scheduled jobs using the `moqui.service.job.ServiceJob` and `moqui.service.job.ServiceJobParameter` entities.
The **ServiceCallJob** interface is used for ad-hoc (explicit) runs of configured service jobs. You can track execution of jobs using `moqui.service.job.ServiceJobRun` records.

Some important fields of *moqui.service.job*.**ServiceJob** that you should know:

  1. *jobName*: unique job name (primary key).
  2. *serviceName*: the service to call (like ${path}.${verb}#${noun}).
  3. *topic*: if set, a notification is sent on completion to the current user and to users configured using `moqui.service.job.ServiceJobUser` records.
  4. *cronExpression*: Quartz-style cron string used by the job runner (via cron-utils). A cron expression is a string of six or seven fields that describe the schedule. For syntax details see [cron-parser.com](http://cron-parser.com) and the [Quartz cron trigger tutorial](https://www.quartz-scheduler.org/documentation/quartz-2.x/tutorials/crontrigger.html).
  5. *paused*: if Y the job is inactive and will not run on its schedule. Ignored for ad-hoc/explicit runs.

 *moqui.service.job*.**ServiceJobParameter** stores parameter name/value pairs that are passed to the service when the job runs.

Methods of the *ServiceCallJob* interface:

- *parameter*(String name, Object value): Single name/value pair to put in the parameters passed to the service.
- *parameters*(Map&lt;String, Object&gt; context): Map of name/value pairs that make up the context (in parameters) passed to the service.
- *localOnly*(boolean local): If true run locally even when a distributed executor is configured (defaults to false).
- *run*():  Run a service job.
  -  Service jobs always run asynchronously.
  -  If the *ServiceJob.topic* field has a value a notification will be sent to the current user and all users configured using `moqui.service.job.ServiceJobUser` records. The *NotificationMessage*.**message** field will be the results of this service call.
  -  It returns the jobRunId for the corresponding `moqui.service.job.ServiceJobRun` record.
  -  Keep a reference to the *ServiceCallJob* (it implements `java.util.concurrent.Future`) if you need the service results without looking at *ServiceJobRun.results*.

 For example:
 ```
   ec.service.job("ImportEntityDataSnapshot").parameters(context).run()
 ```
 The *ImportEntityDataSnapshot* job is used to import Entity Data snapshots. The **job**(String jobName) method is used to get a service caller for a service job. There must be a `moqui.service.job.ServiceJob` record for this jobName.

Manage jobs in the System app at **Service Jobs** (`http://localhost:8080/qapps/system/ServiceJob`). The Jobs tab lists configured jobs; Job Detail can update settings (including **paused**), add parameters, and **Run Job** now; Job Runs is the history (`ServiceJobRun` records). The System dashboard groups these under Server Admin.

Some examples of scheduled jobs from the *MoquiSetupData.xml* file, which is in place by default in Moqui:

 1. *clean_ArtifactData_daily* cleans ArtifactHit and ArtifactHitBin data every night at 2:00 am
 ```
    <moqui.service.job.ServiceJob jobName="clean_ArtifactData_daily" description="Clean Artifact Data: ArtifactHit, ArtifactHitBin"  serviceName="org.moqui.impl.ServerServices.clean#ArtifactData" cronExpression="0 0 2 * * ?" paused="N">
        <parameters parameterName="daysToKeep" parameterValue="90"/>
    </moqui.service.job.ServiceJob>
```

2. *clean_ServiceJobRun_daily* cleans ServiceJobRun data every night at 2:00 am
```
<moqui.service.job.ServiceJob jobName="clean_ServiceJobRun_daily" description="Clean ServiceJobRun Data"  serviceName="org.moqui.impl.ServiceServices.clean#ServiceJobRun" 
cronExpression="0 0 2 * * ?" paused="N">
        <parameters parameterName="daysToKeep" parameterValue="30"/>
</moqui.service.job.ServiceJob>
```
3. *send_AllProducedSystemMessages_frequent* sends all produced system messages every 15 minutes (paused by default; set paused to N to enable)
```
<moqui.service.job.ServiceJob jobName="send_AllProducedSystemMessages_frequent" description="Send All Produced SystemMessages"           serviceName="org.moqui.impl.SystemMessageServices.send#AllProducedSystemMessages" cronExpression="0 0/15 * * * ?" paused="Y"/>
```
