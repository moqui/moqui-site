# Data and Logic Level Interfaces

System interfaces can generally be divided into two main categories: supporting a step in a process, and transferring data (often to keep data updated in another system). For most system integrations a process-level interface is more flexible and also more focused on a specific part of the system, as opposed to transferring all data. Sometimes keeping data consistent between systems is the nature of the integration requirement or the only option available, and then a data-level integration is the way to go. Moqui has tools for both logic/process and data-level system interfaces.

The best way to trigger outgoing messages is through ECA (event-condition-action) rules, either Service ECA (SECA) rules for a logic-level interface or Entity ECA (EECA) rules for a data-level interface. See the **Service ECA Rules** and **Entity ECA Rules** sections for details on how to define these.

All ECA rules call actions, typically one or more *service-call* actions, and those actions will call out to whatever system interface is needed. This may be custom code or simply calling an already existing local or remote service. The following sections describe specific tools available in Moqui, and with custom code you can implement any interface and use any additional libraries needed.
