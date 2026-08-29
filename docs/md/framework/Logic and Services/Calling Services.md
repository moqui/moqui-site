# Calling Services

There are DSL-style interfaces available through the ServiceFacade (ec.**getService**(), or in Groovy ec.service) that have options applicable to the various ways of calling a service. All of these service call interfaces have **name**() methods to specify the service name, and **parameter**() and **parameters**() methods to specify the input parameters for the service. These and other methods on the various interfaces return an instance of themselves so that calls can be chained. Most have some variation of a **call**() method to actually call the service.

For example:
```
Map ahp = [visitId:ec.user.visitId, artifactType:artifactType, ...]
ec.service.async().name("create", "moqui.server.ArtifactHit").parameters(ahp).call()
Map result = ec.service.sync().name("org.moqui.impl.UserServices.create#UserAccount").parameters(params).call()
```

The first service call is to an implicitly defined entity CrUD service to create a ArtifactHit record asynchronously. Note that for **async**() the **call**() method returns nothing and in this case the service call results are ignored. The second is a synchronous call to a defined service with a params input parameter Map, and because it is a **sync**() call the **call**() method returns a Map with the results of the service call.

Beyond these basic methods each interface for different ways of calling a service has methods for applicable options, including:

-   **sync**(): Call the service synchronously and return the results.
    -   **requireNewTransaction**(boolean requireNewTransaction): If true suspend/resume the current transaction (if a transaction is active) and begin a new transaction for the scope of this service call.
    -   **multi**(boolean mlt): If true expect multiple sets of parameters passed in a single map, each set with a suffix of an underscore and the row of the number, i.e. something like "userId\_8" for the userId parameter in the 8th row.
    -   **disableAuthz**(): Disable authorization for the current thread during this service call.

-   **async**(): Call the service asynchronously and ignore the results, get back a ServiceResultWaiter object to wait for the results, or pass in an implementation of the ServiceResultReceiver interface to receive the results when the service is complete.
       -   **callFuture**(): Calls the service (like **call**()) and returns a `java.util.concurrent.Future` instance used to wait for and receive the service results.
       -  **distribute**(boolean dist): If true the service call will be run distributed and may run on a different member of the cluster. Parameter entries MUST be java.io.Serializable (or java.io.Externalizable).
             If false it will be run local only (default).
             
-   **special**(): Register the current service to be called when the current transaction is either committed (use **registerOnCommit**()) or rolled back (use **registerOnRollback**()). This interface does not have a **call**() method.

- **Service Jobs**
  - Configure ad-hoc (explicitly executed) or schedule jobs using `moqui.service.job.ServiceJob` and `moqui.service.job.ServiceJobParameter` entities.
    Here is an example of a schedule job from *MoquiInstallData.xml* file, which is in place by default in Moqui
 ```
    <moqui.service.job.ServiceJob jobName="clean_ArtifactData_daily" description="Clean Artifact Data: ArtifactHit, ArtifactHitBin"
            serviceName="org.moqui.impl.ServerServices.clean#ArtifactData" cronExpression="0 0 2 * * ?" paused="N">
        <parameters parameterName="daysToKeep" parameterValue="90"/>
    </moqui.service.job.ServiceJob>
```
-  - Tracks execution of Jobs using `moqui.service.job.ServiceJobRun` records
   - Run service job through *ServiceCallJob* interface, ec.service.**job**()
       - **run**(): Run a service job
 ```
 ec.service.job("ImportEntityDataSnapshot").parameters(context).run()
 ```

