# Running and Deployment Instructions

This document explains how to run Moqui through the executable war file, or by deploying a war file in an application server.

[TOC]

## 1. Quick Start

### Required Software: Java JDK 21 (Temurin recommended) and OpenSearch

The only required software for the default configuration of Moqui Framework is the **Java SE JDK version 21** or later. The recommended distribution is **Eclipse Temurin (OpenJDK)** from the Adoptium project. **OpenSearch** is also required for certain functionality in the service library (mantle-usl) and applications including Marble ERP, POP Commerce, and HiveMind.

On Linux OpenJDK is generally the best option. For Debian based distributions the apt package is **openjdk-21-jdk**. For Fedora/CentOS/RedHat distributions the yum/dnf package is **java-21-openjdk-devel**.

On macOS and Windows the recommended OpenJDK distribution is Eclipse Temurin, which provides TCK-tested builds for Linux, macOS (including Apple ARM architecture), and Windows:

[https://adoptium.net/temurin/releases/?version=21](https://adoptium.net/temurin/releases/?version=21)

Other OpenJDK distributions such as Azul Zulu or Oracle Java SE may also be used if preferred.

Moqui Framework also includes an OpenSearch client compatible with OpenSearch and ElasticSearch 7.x APIs. The recommended version to use is OpenSearch with no bundled JDK if you are managing Java separately. If OpenSearch is available on localhost port 9200 the default configuration in Moqui will find it, otherwise see configuration environment variables and such below for more options.

[https://opensearch.org/downloads.html](https://opensearch.org/downloads.html)

NOTE: Moqui 3.x required Java 11. Moqui 4.0 requires Java 21. The older **java11** branch discussion is in [pull request 527](https://github.com/moqui/moqui-framework/pull/527).

### Moqui Binary Release Quick Start

1. Download a binary distribution like the **.war** file in the latest release
  - https://github.com/moqui/moqui-framework/releases/latest
1. Load the seed and demo data (will create H2 database and tables automatically):
  - `$ java -jar moqui.war load`
1. Run the framework (with embedded Servlet Container, Transaction Manager, Database):
  - `$ java -jar moqui.war`
1. In your browser (on the same machine) go to:
  - `http://localhost:8080/` (the default UI is Quasar under `/qapps`)
1. With the demo data loaded you can login with username "john.doe" and password "moqui"

### From Source Quick Start with OpenSearch

Use the following steps to do a local install from source and run with the default embedded database (H2) and OpenSearch installed in the runtime/opensearch directory.

1. Clone the moqui-framework repository
  - `$ git clone https://github.com/moqui/moqui-framework.git moqui`
  - `$ cd moqui`
1. Get desired components, for example MarbleERP, PopCommerce, and/or HiveMind
  - `$ ./gradlew getComponent -Pcomponent=MarbleERP`
  - `$ ./gradlew getComponent -Pcomponent=PopCommerce`
  - `$ ./gradlew getComponent -Pcomponent=HiveMind`
  1. Alternatively just get the default runtime directory (if you don't want any components)
    - `$ ./gradlew getRuntime`
1. Download OpenSearch into `runtime/opensearch` (Linux x64 tarball; on macOS or Windows install OpenSearch yourself or run it separately)
  - `$ ./gradlew downloadOpenSearch`
1. Build then load seed and demo data (the load task depends on the build task)
  - `$ ./gradlew load`
1. Start Moqui (it starts OpenSearch in `runtime/opensearch` if present; add `no-run-es` to skip)
  - `$ java -jar moqui.war`
1. In your browser go to `http://localhost:8080` (default UI: `http://localhost:8080/qapps`)

### From Source Quick Start with Docker Compose

Use the following steps to do a local install from source and run with a database and OpenSearch in Docker containers separate from Moqui. This works best on Linux but can be used with some variations on MacOS and Windows.

1. Install Docker Engine and the Docker Compose plugin, make sure your user is in the 'docker' group, etc
  - [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
  - [https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)
1. Clone the moqui-framework repository
  - `$ git clone https://github.com/moqui/moqui-framework.git moqui`
  - `$ cd moqui`
1. Get desired components, for example MarbleERP, PopCommerce, and/or HiveMind
  - `$ ./gradlew getComponent -Pcomponent=MarbleERP`
  - `$ ./gradlew getComponent -Pcomponent=PopCommerce`
  - `$ ./gradlew getComponent -Pcomponent=HiveMind`
  1. Alternatively just get the default runtime directory (if you don't want any components)
    - `$ ./gradlew getRuntime`
1. Put a JDBC driver JAR for the target database in `runtime/lib` (or use `./gradlew getPostgresJdbc` / `./gradlew getMySqlJdbc`)
1. Build Moqui and create the moqui-plus-runtime.war file
  - `$ ./gradlew addRuntime`
1. Build a local Docker image using the default name **moqui** (see the Docker section below for using a different group/name, pushing to a Docker repository, etc)
  - `$ cd docker/simple`
  - `$ ./docker-build.sh`
1. Go back to the **docker** directory
  - `$ cd ..`
1. Choose a Compose file in `docker/` (see `docker/README.md`). Current examples include `moqui-postgres-compose.yml`, `moqui-mysql-compose.yml`, and `moqui-acme-postgres.yml`
1. Build the image if needed and start the configured containers (replace the filename with your preferred compose file)
  - `$ ./build-compose-up.sh moqui-postgres-compose.yml`
  - When Moqui starts for the first time it will see the database is empty (no records in the table for the Enumeration entity) and will automatically load the configured data sets; with the default MoquiProductionConf.xml file that includes all **seed**, **seed-initial**, and **install** data files
1. If you use one of these default files with the VIRTUAL_HOST for nginx-proxy set to **moqui.local** add a line for it in /etc/hosts like:
  - `127.0.0.1	moqui.local`
1. Access Moqui in your browser
  - In your browser go to `https://moqui.local` or whichever host you configured
  - If you use moqui.local and the included self-signed certificate you'll get a warning about that in your browser and will need to follow the links to go there regardless of the certificate
  - When you access Moqui for the first time and there are no users in the database (no demo, etc data loaded) the Login screen will show a form to create an admin user
1. Stop the configured containers (make sure to use the same YML file you used to start)
  - `$ ./compose-down.sh moqui-postgres-compose.yml`
1. Clean up mapped directories (IF you want to remove the database, etc to start fresh; note that this requires root access because the database and other folders mapped to the host file system will be owned by root)
  - `$ sudo ./clean.sh`

### Really Quick Start

1. Download the MoquiDemo-<version>.war file (or similar HiveMind/PopCommerce war files)
  - [https://github.com/moqui/moqui-framework/releases](https://github.com/moqui/moqui-framework/releases)
1. Drop the WAR file into Java Servlet Container (Jetty, Apache Tomcat, AWS ElasticBeanstalk, etc)

## 2. Runtime Directory and Moqui Configuration XML File

Moqui Framework has two main parts to deploy:

1. Executable WAR File (see below; from moqui-framework repository)
1. Runtime Directory with Configuration File (from moqui-runtime repository, or your own)

However you use the executable WAR file, you must have a runtime directory and you may override default settings with a XML configuration file.

All configuration for Moqui Framework lives in the Moqui Conf XML file. The actual configuration XML file used at runtime is built by merging various XML files in this order:

1. **MoquiDefaultConf.xml** that ships with the framework as is included in the built WAR file
1. **MoquiConf.xml** from each component
1. specified runtime Moqui Conf XML file such as **MoquiDevConf.xml** or **MoquiProductionConf.xml**

The runtime directory is the main place to put components you want to load, the root files (root screen, etc) for the web application, and configuration files. It is also where the framework will put log files, H2 database files (if you are using H2), JCR repo files, etc. You may eventually want to create your own runtime directory and keep it in your own source repository (fork the moqui-runtime repository) but you can use the default one to get started and for most deployments with add-on applications everything in moqui-runtime you will commonly want to override or extend can be done within your add-on components.

Specify these two properties:

|   |   |
| --- | --- |
| `moqui.runtime` | Runtime directory (defaults to "./runtime") |
| `moqui.conf` | Moqui Conf XML file (URL or path relative to moqui.runtime) |

There are two ways to specify these two properties:

1. `MoquiInit.properties` file on the classpath
1. System properties specified on the command line (with java -D arguments)

See below for examples.

## 3. Executable WAR File

Yep, that's right: an executable WAR file.

If the first argument is **load** it will load data. If the first argument is **help** it will show the help text. If there are no arguments or the first argument is anything else it will run the embedded web server (the Jetty Servlet Container). The MoquiStart class can also be run directly if the WAR file has been unzipped into a directory.

|   |   |
| --- | --- |
| Load Data | `$ java -jar moqui.war load` |
| Run Embedded Web Server | `$ java -jar moqui.war` |
| Deploy as WAR, for Tomcat | `$ cp moqui.war ../tomcat/webapps/ROOT.war` |
| Show Help Text | `$ java -jar moqui.war help` |
| Unzipped WAR Load Data | `$ java -cp . MoquiStart load` |
| Unzipped WAR Run Web Server | `$ java -cp . MoquiStart` |

### Web Server Arguments

|   |   |
| --- | --- |
| port=<port> | The http listening port. Default is 8080 |
| threads=<max threads> | Maximum number of threads. Default is 100 |
| conf=<moqui.conf> | The Moqui Conf XML file to use, overrides other ways of specifying it |
| no-run-es | Don't try starting and stopping OpenSearch in runtime/opensearch or ElasticSearch in runtime/elasticsearch |

### Load Data Arguments

If no **types** or **location** argument is used all found data files of all types will be loaded.

|   |   |
| --- | --- |
| types=<type>[,<type>](/docs/framework/,<type>) | Data types to load (can be anything, common are: seed, seed-initial, install, demo, ...) |
| components=<name>[,<name>](/docs/framework/,<name>) | Component names to load for data types; if none specified loads from all |
| location=<location> | Location of data file to load |
| timeout=<seconds> | Transaction timeout for each file, defaults to 600 seconds (10 minutes) |
| no-fk-create | Don't create foreign-keys, for empty database to avoid referential integrity errors |
| dummy-fks | Use dummy foreign-keys to avoid referential integrity errors |
| use-try-insert | Try insert and update on error instead of checking for record first |
| disable-eeca | Disable Entity ECA rules |
| disable-audit-log | Disable Entity Audit Log |
| disable-data-feed | Disable Entity DataFeed |
| raw | For raw data load to an empty database; short for no-fk-create, use-try-insert, disable-eeca, disable-audit-log, disable-data-feed |
| conf=<moqui.conf> | The Moqui Conf XML file to use, overrides other ways of specifying it |
| no-run-es | Don't try starting and stopping OpenSearch in runtime/opensearch or ElasticSearch in runtime/elasticsearch |

## 4. Examples and Common Approaches

### Easy Way - Default Settings

The easiest way to run is to have a moqui directory with the moqui.war file and the runtime directory in it. With the binary distribution of Moqui when you unzip the archive this is what you'll have.

To use the default settings:

- moqui.runtime = runtime
- moqui.conf = conf/MoquiDevConf.xml (relative to runtime)

Run these commands:

|   |   |
| --- | --- |
| Load Data | `$ java -jar moqui.war load` |
| Run Server | `$ java -jar moqui.war` |

### Common Alternate - Specify a Configuration File on Command Line

|   |   |
| --- | --- |
| Load Data | `$ java -jar moqui.war load conf=conf/MoquiProductionConf.xml` |
| Run Server | `$ java -jar moqui.war conf=conf/MoquiProductionConf.xml` |

### Create a Custom WAR File with Settings Inside

1. Add components and other resources as needed to the runtime directory
1. Change ${moqui.home}/MoquiInit.properties with desired settings
1. Change Moqui conf file (runtime/conf/Moqui*Conf.xml) as needed
1. Create a derived WAR file based on the moqui.war file and with your runtime directory contents and MoquiInit.properties file with: `./gradlew addRuntime` (or `ant add-runtime`)
1. Copy the created WAR file (moqui-plus-runtime.war) to deployment target
1. Run server (or restart to deploy live WAR)

## 5. Component Management

The best way to manage source repositories for components is to have one repository (on GitHub or elsewhere) per component that contains only the component directory.

Following this pattern the Gradle build scripts in Moqui have tasks to download components and their dependencies from a git repository, or from current or release archives.

Known open source components are already configured in the `addons.xml` file. To add private and other components or override settings for components in the addons.xml file, create a file called `myaddons.xml` and put it in the moqui directory.

Here is a summary of the Gradle tasks for component management (using the HiveMind component for example). Prefer the Gradle wrapper (`./gradlew`). All of the get tasks get the specified component plus all components it depends on (as specified in its component.xml file).

|   |   |   |
| --- | --- | --- |
| Get runtime directory | `$ ./gradlew getRuntime -PlocationType=(git,current,release)` | Called automatically if runtime directory does not exist. Location type defaults to git if .git directory exists, otherwise to current. |
| Get component | `$ ./gradlew getComponent -Pcomponent=HiveMind -PlocationType=(git,current,release)` | Location type defaults to git if .git directory exists, otherwise to current |
| Get from Git repository | `$ ./gradlew getGit -Pcomponent=HiveMind` |  |
| Get current archive | `$ ./gradlew getCurrent -Pcomponent=HiveMind` |  |
| Get release archive | `$ ./gradlew getRelease -Pcomponent=HiveMind` |  |
| Get dependencies for all components | `$ ./gradlew getDepends -PlocationType=(git,current,release)` | Location type defaults to git if .git directory exists, otherwise to current |

There are also Gradle tasks to help you manage your components from git. Each of these commands does git operations if a .git directory exists for the moqui (root) repository, the runtime repository, and all components.

|   |   |
| --- | --- |
| Git pull all | `$ ./gradlew gitPullAll` |
| Git status on all | `$ ./gradlew gitStatusAll` |
| Git pull upstream on all | `$ ./gradlew gitUpstreamAll` |
| Clean all, pull all, load data | `$ ./gradlew cleanPullLoad` |
| Clean all, pull all, load data, all tests | `$ ./gradlew cleanPullTest` |
| Clean all, pull all, load data, only component tests | `$ ./gradlew cleanPullCompTest` |

## 6. Build From Source

Moqui Framework uses Gradle for building from source. There are various custom tasks to automate frequent things, but most work is done with the built-in tasks from Gradle. There is also an Ant build file for a few common tasks, but not for building from source.

|   |   |   |
| --- | --- | --- |
| Get Component and Dependencies (for example: HiveMind) | `$ ./gradlew getComponent -Pcomponent=HiveMind` |  |
| Build JAR, WAR | `$ ./gradlew build` |  |
| Load All Data | `$ ./gradlew load` | `$ ant load` |
| Create WAR with embedded runtime | `$ ./gradlew addRuntime` | `$ ant add-runtime` |
| Clean up JARs, WAR | `$ ./gradlew clean` |  |
| Clean up ALL built and runtime files (logs, dbs, etc) | `$ ./gradlew cleanAll` |  |

The examples above use the Gradle Wrapper (`gradlew`) included with Moqui (Gradle **9.2**). You can also install Gradle locally, but the wrapper is preferred so the version matches the project. The load and run tasks depend on the build task, so the easiest way to get a new development system running with a populated database is:

|   |   |
| --- | --- |
| Linux/Mac Gradle Wrapper | `$ ./gradlew load run` |
| Windows Gradle Wrapper | `> gradlew.bat load run` |
| Installed Gradle | `$ gradle load run` |

This will build the war file, run the data loader, then run the server. To stop it just press <ctrl-c> (or your preferred alternative).

## 7. OpenSearch Configuration and Install

**OpenSearch** is the recommended search engine. The built-in ElasticFacade client (`ec.elastic`) also works with ElasticSearch 7.x-compatible HTTP APIs. There is no embedded-in-JVM search node. Install OpenSearch under `runtime/opensearch` (or ElasticSearch under `runtime/elasticsearch`) and run it as a separate process, or point `elasticsearch_url` at an external cluster.

### External OpenSearch or ElasticSearch

In production it is more common to have an external OpenSearch (or ElasticSearch) cluster running separate from the Moqui server or cluster. This can also be used for local development where you start, stop, and clear data separately from Moqui or the Moqui Gradle tasks.

The recommended install is OpenSearch:

[https://opensearch.org/downloads.html](https://opensearch.org/downloads.html)

ElasticSearch 7.x (last Apache 2.0 OSS release: 7.10.2) is still usable if you need it.

Cluster configuration is in the Moqui Conf XML file. The `default` cluster in MoquiDefaultConf.xml uses environment variables (or Java system properties). Unless you are using a server that requires HTTP Basic Authentication, the only property you typically need is `elasticsearch_url`, which defaults to `http://127.0.0.1:9200`.

### OpenSearch Installed in Runtime

OpenSearch may be installed in the `runtime/opensearch` directory (or ElasticSearch in `runtime/elasticsearch`) and started by Moqui when it starts (through MoquiStart only), as well as started, stopped, and data-cleaned through Gradle tasks. In local development it is common to run a local instance and clear its data along with the H2 database. This can also be used in production when you do not need a separate search cluster.

If both directories exist, OpenSearch is preferred. Make sure `JAVA_HOME` is set so the search process can find a JDK.

To install OpenSearch in `runtime/opensearch` use:

`$ ./gradlew downloadOpenSearch`

That task downloads the OpenSearch min (no bundled JDK) **Linux x64** tarball. On macOS or Windows, install OpenSearch yourself into `runtime/opensearch`, run an external instance, or use Docker.

The older `downloadElasticSearch` task still exists and downloads ElasticSearch OSS 7.10.2 (no JDK) for Linux, macOS, or Windows into `runtime/elasticsearch`. Prefer OpenSearch.

Gradle also has `startElasticSearch` and `stopElasticSearch` tasks. They operate on `runtime/opensearch` if present, otherwise `runtime/elasticsearch`. Gradle matches partial task names as long as they match a single task, so you can use shorter names like `downloadop`, `startel`, and `stopel`.

`$ ./gradlew startel`
`$ ./gradlew stopel`

These report a message when trying to start or stop, and do nothing if they don't find an install (`bin` directory) or if a `pid` file already exists (already running). If you aren't sure whether search is running, `startel` starts it if needed and `stopel` stops it if a pid file is present.

The `cleanDb`, `load`, `loadSave`, `reloadSave`, and `test` tasks respect a runtime OpenSearch or ElasticSearch install. If it is running (pid file exists) `cleanDb` will stop it, delete the data directory, then start it again. The `test` task starts search if `bin` exists and `pid` does not, but it does not currently stop search after tests.

The `MoquiStart` class starts OpenSearch in `runtime/opensearch` (or ElasticSearch in `runtime/elasticsearch`) if it finds a `bin` directory there. To disable this use the `no-run-es` argument:

`$ java -jar moqui.war`

This also works with the load argument:

`$ java -jar moqui.war load`

Search is started in a forked process. MoquiStart is used when running the executable WAR with `java -jar`, and when running from the root of an expanded WAR as the Procfile does, like:

`java -cp . MoquiStart port=5000 conf=conf/MoquiProductionConf.xml`

MoquiStart is **not** used when you drop the WAR file in an external Servlet Container like Tomcat or Jetty. If you deploy that way you must use an external OpenSearch or ElasticSearch server or cluster.

For a local development instance a common cycle is to clean then load data, run tests, reload saved data and run tests, and so on. To do a full test run make sure OpenSearch is installed in `runtime/opensearch` and preferably is not already running, then:

`$ ./gradlew loadSave test stopel`

To reload the data saved just after the initial data load (including H2 and search data) and run a specific component's tests (like mantle-usl):

`$ ./gradlew reloadSave startel runtime:component:mantle-usl:test stopel`

After a build and load, start Moqui and it starts and stops search with the process:

`$ java -jar moqui.war`

## 8. Database and Other Configuration

### Environment Variables

Support for single database configuration was added for easier Docker, etc deployment and can be used in any environment. This is an alternative to adding database configuration in the runtime Moqui Conf XML file as described in the next section.

Each of these can be system environment variables (with underscores) or Java properties (with underscores or dots) using the -D command-line argument.

The JDBC driver for the desired database must be on the classpath. The jar file can be added to the runtime/lib directory (within the moqui-plus-runtime.war file if used) or on the command line. In Docker images the runtime/lib directory within the container can be mapped to a directory on the host for convenience (along with runtime/conf and many other directories).

Note that the 'mysql' database configuration also works with MariaDB and Percona.

Environment variables are a convenient way to configure the database when using pre-built WAR files with runtime included or Docker images.

| Env Var or Property | MySQL Example | Description |
| --- | --- | --- |
| entity_ds_db_conf | mysql | Database configuration from MoquiDefaultConf.xml or one you add |
| entity_ds_host | localhost | Host name of database server |
| entity_ds_port | 3306 | Port the database is running on |
| entity_ds_database | moqui | Name of the database on the server |
| entity_ds_schema |  | Schema within the database to use (note: leave empty by default for MySQL) |
| entity_ds_user | moqui | Database user |
| entity_ds_password | CHANGEME | Password for database user |
| entity_ds_crypt_pass | CHANGEME | The key used for encrypted fields, should be protected just like a password |
| entity_add_missing_startup | true | Defaults to true; set to 'false' to not add missing tables, columns, etc on startup |

To configure the ElasticFacade client (OpenSearch or ElasticSearch) use the following environment variables:

| Env Var or Property | Example | Description |
| --- | --- | --- |
| elasticsearch_url | http://127.0.0.1:9200 | The base URL for the OpenSearch or ElasticSearch server |
| elasticsearch_user |  | The user for HTTP Basic Authentication |
| elasticsearch_password |  | The password for HTTP Basic Authentication |
| elasticsearch_index_prefix |  | Optional prefix for index names |

Another set of common environment variables to use is for URL writing, locale, time zone, etc:

| Env Var or Property | Example | Description |
| --- | --- | --- |
| instance_purpose | production | A purpose for the instance, 'production' has special meaning as do 'test' and 'dev' |
| webapp_http_host | moqui.org | The hostname to use, defaults to host name or IP address used for the request |
| webapp_http_port | 80 | The port for building insecure URLs; this is for building URLs, it is not the port the Servlet Container is listening to (that is configured in the Servlet Container and may be different from this external port if a load balancer or reverse proxy is used) |
| webapp_https_port | 443 | The port for building secure URLs; this is for building URLs, it is not the port the Servlet Container is listening to (that is configured in the Servlet Container and may be different from this external port if a load balancer or reverse proxy is used) |
| webapp_https_enabled | true | Set to true to enable secure URLs. Defaults to false with all URLs generated for insecure port. |
| default_locale | en_US | The Java default Locale |
| default_time_zone | US/Pacific | The Java default TimeZone |
| database_time_zone | US/Pacific | The time zone to use in the database, defaults to default_time_zone |
| scheduled_job_check_time | 60 | How often (in seconds) to check for scheduled jobs to run, set to 0 to not run scheduled jobs |

### Production security

Moqui Framework is designed to run **behind** a web application firewall and typically a reverse proxy or load balancer. It is not a WAF and is not the right place in the stack for WAF functionality.

The framework has some overlapping knobs (artifact tarpit / velocity limits, login failure lockout, HTML allow-lists, CSRF session tokens, default response headers). Those are for **application and business-risk mitigation** inside the app. They are not intended to cover volumetric and protocol attacks, bot scoring, geo/IP reputation, TLS/HTTP normalization, virtual patching, or similar **edge** concerns. Put a WAF (or a proxy that includes WAF features) in front of Moqui. The Docker nginx-proxy and ACME compose files under `moqui/docker/` are examples of **TLS at the proxy**, not a WAF.

`webapp_https_enabled`, `webapp_https_port`, and `webapp_http_host` (table above) are for **URL generation** when Moqui is behind that edge. They are not the port the Servlet container listens on, and they do not terminate TLS or filter attacks.

Checklist for a production instance:

- **Edge**: TLS at the proxy; WAF in front of Moqui; do not expose the Servlet port as the public hostname.
- **Secrets**: change every `CHANGEME` default, including `entity_ds_password` and `entity_ds_crypt_pass`. Treat the entity crypt pass like a password (encrypted entity fields).
- **Data**: do not load demo data; do not leave `john.doe` / `moqui`. Set `instance_purpose=production`.
- **Network**: the database and OpenSearch listen on a private network, not the public internet.
- **Identity**: username/password is the default. Built-in [MFA](/docs/framework/Security#second-factor-mfa) can be required per user or UserGroup. Optional [SSO](/docs/framework/Single+Sign-On) (`moqui-sso`) for OIDC, OAuth, or SAML. MFA is not SSO; neither is a WAF.
- **Admin surface**: Groovy Shell, SQL Runner, Auto Screens, and Entity Data Import are high privilege. Restrict them with artifact authz and do not put them on the public internet.
- **Reporting**: see [Security](/docs/framework/Security) and the [Community Guide](/docs/moqui/Community+Guide). Send undisclosed issues to **moqui-board@googlegroups.com**.

### Moqui Conf XML File

Database (or datasource) setup is done in the Moqui Conf XML file with `moqui-conf.entity-facade.datasource` elements. There is one element for each entity group and the `datasource.@group-name` attribute matches against `entity.@group-name` attribute in entity definitions. By default in Moqui there are 4 entity groups: `transactional, nontransactional, configuration, and analytical`. If you only configure a `datasource` for the `transactional` group it will also be used for the other groups.

The default transactional datasource uses `entity_ds_*` environment variables (or Java properties) and the `h2` database configuration. An explicit H2 datasource looks like:

```xml
<datasource group-name="transactional" database-conf-name="h2" schema-name="">
    <!-- with this setup you can connect remotely using "jdbc:h2:tcp://localhost:9092/moqui" -->
    <inline-jdbc>
        <xa-properties url="jdbc:h2:${moqui_runtime}/db/h2/moqui;lock_timeout=30000" user="sa" password=""/>
    </inline-jdbc>
</datasource>
```

The database-conf-name attribute points to a database configuration and matches against a `database-list.database.@name` attribute to identify which. Database configurations specify things like SQL types to use, SQL syntax options, and JDBC driver details.

This example uses an xa-properties element to use the XA (transaction aware) interfaces in the JDBC driver. The attributes on the element are specific to each JDBC driver. Some examples for reference are included in the MoquiDefaultConf.xml file, but for a full list of options look at the documentation for the JDBC driver.

The JDBC driver must be in the Java classpath. The easiest way to get it there, regardless of deployment approach, is to put it in the `runtime/lib` directory.

Here is an example of a XA configuration for MySQL (use `database-conf-name="mysql8"` for MySQL 8 / 9, as the Docker compose files do):

```xml
<datasource group-name="transactional" database-conf-name="mysql" schema-name="">
    <inline-jdbc pool-minsize="5" pool-maxsize="50">
        <xa-properties user="moqui" password="CHANGEME" pinGlobalTxToPhysicalConnection="true"
                serverName="127.0.0.1" port="3306" databaseName="moqui" autoReconnectForPools="true"
                useUnicode="true" encoding="UTF-8"/>
    </inline-jdbc>
</datasource>
```

To use something like this put the `datasource` element under the `entity-facade` element in the runtime Moqui Conf XML file (like the `MoquiProductionConf.xml` file).

For more examples and details about recommended configuration for different databases see the comments in the MoquiDefaultConf.xml file:

[https://github.com/moqui/moqui-framework/blob/master/framework/src/main/resources/MoquiDefaultConf.xml](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/resources/MoquiDefaultConf.xml)

## 9. Production Recommendations

### Docker and Docker Compose

The default Dockerfile and a script to build a Docker image based on the moqui-plus-runtime.war file are in the moqui/docker/simple directory which you can see on GitHub here:

[https://github.com/moqui/moqui-framework/tree/master/docker/simple](https://github.com/moqui/moqui-framework/tree/master/docker/simple)

For example after adding all components, JDBC drivers, and anything else you want in your runtime directory do something like:

|   |   |
| --- | --- |
| `$ ./gradlew addRuntime` | Build then create the moqui-plus-runtime.war file |
| `$ cd docker/simple` |  |
| `$ ./docker-build.sh ../.. mygroup/myrepo` | Build Docker image using Dockerfile, tagged latest by default (Eclipse Temurin 21) |
| `$ docker tag mygroup/myrepo:latest mygroup/myrepo:1.0.0` | Add a tag for the version of the image |
| `$ docker login -u <username> -p <password>` | Login to Docker Hub (or other image repo) if not already logged in |
| `$ docker push mygroup/myrepo` | Push to Docker Hub (or elsewhere) |

On the server where the image will run make sure Docker Engine and the Docker Compose plugin are installed and then pull the image created above. There are various Compose examples in the moqui/docker directory:

[https://github.com/moqui/moqui-framework/tree/master/docker](https://github.com/moqui/moqui-framework/tree/master/docker)

You'll need to create a custom compose YAML file based on one of these (`moqui-postgres-compose.yml`, `moqui-mysql-compose.yml`, `moqui-acme-postgres.yml`, and others). This is where you put database, host, and other settings and is where you specify the image to use (like mygroup/myrepo above). Compose files do not use a `version` key. To pull your image and start it up along with other Docker images for other needed applications (nginx-proxy, mysql or postgres, OpenSearch, etc) do something like:

|   |   |
| --- | --- |
| `$ docker login -u <username> -p <password>` | Login to Docker Hub (or other image repo) if not already logged in |
| `$ docker pull mygroup/myrepo` | Pull image from Docker Hub (or elsewhere) |
| `$ ./compose-up.sh my-compose.yml` | Bring up containers as defined in the Docker Compose YAML file |

There is also a `compose-down.sh` script to bring down an instance. For updates after running `docker pull` you can run `compose-up.sh` without running `compose-down.sh` first and Docker Compose will simply update the containers with new images versions.

You may want to modify the `compose-up.sh` script and others to fit your specific deployment, including configuration and other Moqui runtime files you want to live on the Docker host instead of in a container (to survive updates, use configuration, etc). Generally when setting up a new Docker server it is recommended to create a private git repository to use as a shell for your Docker deployment. This would contain your compose up/down scripts, your compose YML file(s), and a runtime directory with any additional configuration files, components, JDBC jars, etc.

### AWS Elastic Beanstalk and RDS

The recommended approach for deployment with AWS ElasticBeanstalk is to use a 'Java SE' environment. A Tomcat environment can be used by simply uploading a moqui-plus-runtime.war file but there are issues with this approach in that it is less flexible, Tomcat settings need to be adjusted for capacity, various changes are needed to support websocket, and so on. Using a Java SE environment with the embedded Jetty web server generally runs better and has various defaults already in place that are recommended for Moqui, plus full control of the command line to start the server to adjust servlet threads, port, Moqui XML Conf file to use, etc.

In a AWS EB Java SE environment you'll have a nginx proxy already in place that by default expects the application to be running on port 5000. The Java SE environment is used by uploading an application archive containing files for the application(s) and to tell the Java SE environment what to do. Since Moqui Framework 2.1.1 there is a Procfile included that will be added to the moqui-plus-runtime.war file. By default it contains:

```
web: java -cp . MoquiStart port=5000 conf=conf/MoquiProductionConf.xml
```

Note that it does not contain memory options so that they may be set with the JAVA_TOOL_OPTIONS environment variable. For example set it to "-Xmx1024m -Xms1024m" for a 1024 MB Java heap. The heap size on a dedicated instance should be about 1/2 the total system memory (leaving room for off-heap Java memory usage and operating system memory usage).

MoquiStart starts OpenSearch in `runtime/opensearch` (or ElasticSearch in `runtime/elasticsearch`) automatically if a `bin` directory is present. There is no `run-es` argument; use `no-run-es` if you do **not** want that. To install OpenSearch in the runtime directory:

```
$ ./gradlew downloadOpenSearch
```

That Gradle task currently downloads the Linux x64 OpenSearch distribution. On other platforms, install OpenSearch into `runtime/opensearch` yourself, or run an external cluster and set `elasticsearch_url`.

The archive to deploy is basically just the moqui-plus-runtime.war file. The WAR file must be renamed from .war to .zip so that the AWS Java SE environment treats it like a plain archive and not an executable jar. To build a file to upload to AWS ElasticBeanstalk do something like:

|   |   |
| --- | --- |
| `$ ./gradlew addRuntime` | Build then create the moqui-plus-runtime.war file |
| `$ mv moqui-plus-runtime.war ../myapp-1.0.0.zip` | Rename the WAR file and move to parent directory to keep separate |

Then upload the ZIP file in the Elastic Beanstalk section of the AWS Console when you create your Java SE environment.

You'll also need to set various environment variables in your Elastic Beanstalk settings (under Configuration => Software Configuration) for database, host, and other settings. See the Environment Variables section above for a list of which to set.

Typically these settings will include host and other database information for a RDS instance running MySQL, Postgres, or other. Make sure the VPC Security Group for the RDS instance (automatically created when you create the DB instance) has an inbound rule with a VPC Security Group that your Elastic Beanstalk configuration is in (specified in Configuration => Instance). This is done in the VPC section of the AWS Console under Security Groups.

The smallest recommended servers to use are t2.small for the EC2 instance and t2.micro for the RDS instance for a total cost generally under $40/mo depending whether a reserved instance is used, how much disk space is used, etc. Note that for larger EC2 instances make sure to adjust the Procfile so that the maximum heap size is higher, usually roughly half of total memory for the instance if there is nothing else running on it.

## 10. Project Directory Structure

```
- moqui (from https://github.com/moqui/moqui)
  - framework
    - build          : Results of framework build go here (classes, jars, etc)
    - data           : Seed data
    - entity         : Framework entity definitions
    - lib            : Libraries (JAR files) used in Moqui
    - screen         : Framework screens
    - service        : Framework services
    - src            : Java API, standard entities, services, data, XSDs, etc
      - api          : Java source for the Moqui Framework API
      - main         : Main implement source
        - groovy     : Groovy source (bulk of the implementation)
        - java       : Java source (a few special classes)
        - resources  : Classpath resources, placed in JAR as-is
        - webapp     : Base webapp, mostly just a WEB-INF/web.xml file
      - start        : Java source for MoquiStart, used for executable WAR
    - template       : Framework templates (screen/form, xml-actions FTLs)
    - xsd            : Framework XML Schema files
  - runtime
    - base-component : Base/framework components to deploy
      - tools        : System administration and maintenance tools
      - webroot      : Root Screen and supporting content
    - classes        : Resources to add to the runtime classpath
    - component      : Application/etc components to deploy
    - conf           : Configuration files separated by dev, staging, prod, etc
    - db             : Database files for H2, Derby, OrientDB, etc will go here
    - opensearch     : Optional OpenSearch install directory (recommended)
    - elasticsearch  : Optional ElasticSearch install directory
    - lib            : JAR files to add to the runtime classpath (JDBC drivers, etc)
    - log            : Log files will go here
    - template       : General Templates
    - tmp            : Temporary files
    - txlog          : Transaction log files will go here (Bitronix files)
```

The main place to put your components is in the runtime/component directory. When you use the Gradle get component tasks this is where they will go.

Components with declared dependencies (in a component.xml file in the component directory) will be loaded after the component(s) they depend on.
