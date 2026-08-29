# Calling Services

There are DSL-style interfaces available through the ServiceFacade (ec.**getService**(), or in Groovy ec.service) that have options applicable to the various ways of calling a service. All of these service call interfaces have **name**() methods to specify the service name, and **parameter**() and **parameters**() methods to specify the input parameters for the service. These and other methods on the various interfaces return an instance of themselves so that calls can be chained. Most have some variation of a **call**() method to actually call the service.

For example:
```
Map ahp = [visitId:ec.user.visitId, artifactType:artifactType, ...]
ec.service.async().name("create", "moqui.server.ArtifactHit").parameters(ahp).call()
Map result = ec.service.sync().name("org.moqui.impl.UserServices.create#UserAccount").parameters(params).call()
```

The first service call is to an implicitly defined entity CrUD service to create an ArtifactHit record asynchronously. Note that for **async**() the **call**() method returns nothing and in this case the service call results are ignored. The second is a synchronous call to a defined service with a params input parameter Map, and because it is a **sync**() call the **call**() method returns a Map with the results of the service call.

Beyond these basic methods each interface for different ways of calling a service has methods for applicable options, including:

-   **sync**(): Call the service synchronously and return the results.
    -   **requireNewTransaction**(boolean requireNewTransaction): If true suspend/resume the current transaction (if a transaction is active) and begin a new transaction for the scope of this service call.
    -   **multi**(boolean mlt): If true expect multiple sets of parameters passed in a single map, each set with a suffix of an underscore and the row of the number, i.e. something like "userId\_8" for the userId parameter in the 8th row.
    -   **disableAuthz**(): Disable authorization for the current thread during this service call.

-   **async**(): Call the service asynchronously. Use **call**() to ignore the results, or **callFuture**() to get a `java.util.concurrent.Future` to wait for and receive the results when the service is complete. You can also get a **Runnable** or **Callable** with **getRunnable**() and **getCallable**() to run the call through an executor of your choice.
       -  **distribute**(boolean dist): If true the service call will be run distributed and may run on a different member of the cluster. Parameter entries MUST be java.io.Serializable (or java.io.Externalizable). If false it will be run local only (default).

-   **special**(): Register the current service to be called when the current transaction is either committed (use **registerOnCommit**()) or rolled back (use **registerOnRollback**()). This interface does not have a **call**() method.

- **[Service Jobs](/docs/framework/Logic+and+Services/Service+Jobs)**
  - Configure ad-hoc (explicitly executed) or scheduled jobs using `moqui.service.job.ServiceJob` and `moqui.service.job.ServiceJobParameter` entities.
    Here is an example of a scheduled job from the *MoquiSetupData.xml* file, which is in place by default in Moqui
 ```
    <moqui.service.job.ServiceJob jobName="clean_ArtifactData_daily" description="Clean Artifact Data: ArtifactHit, ArtifactHitBin"
            serviceName="org.moqui.impl.ServerServices.clean#ArtifactData" cronExpression="0 0 2 * * ?" paused="N">
        <parameters parameterName="daysToKeep" parameterValue="90"/>
    </moqui.service.job.ServiceJob>
```
-  - Tracks execution of jobs using `moqui.service.job.ServiceJobRun` records
   - Run a service job through the *ServiceCallJob* interface, ec.service.**job**()
       - **run**(): Run a service job
 ```
 ec.service.job("ImportEntityDataSnapshot").parameters(context).run()
 ```

Remote JSON-RPC and REST calls are also available on ServiceFacade as **callJsonRpc**() and **rest**() (a `RestClient`). See the [Web Service](/docs/framework/System+Interfaces/Web+Service) section for remote interfaces.
