# Running and Deployment Instructions

This document explains how to run Moqui through the executable war file, or by deploying a war file in an application server.

[TOC]

## 1. Quick Start

### Required Software: Java JDK 21 (Temurin recommended) and OpenSearch

The only required software for the default configuration of Moqui Framework is the **Java SE JDK version 21** or later. The recommended distribution is **Eclipse Temurin (OpenJDK)** from the Adoptium project. **OpenSearch** is also required for certain functionality in the service library (mantle-usl) and applications including POPC ERP, HiveMind, and Marble ERP.

On Linux OpenJDK is generally the best option. For Debian based distributions the apt package is **openjdk-21-jdk**. For Fedora/CentOS/RedHat distributions the yum/dnf package is **java-21-openjdk-devel**.

On macOS and Windows the recommended OpenJDK distribution is Eclipse Temurin, which provides TCK-tested builds for Linux, macOS (including Apple ARM architecture), and Windows:

[https://adoptium.net/temurin/releases/?version=21](https://adoptium.net/temurin/releases/?version=21)

Other OpenJDK distributions such as Azul Zulu or Oracle Java SE may also be used if preferred.

Moqui Framework also includes an OpenSearch client compatible with OpenSearch and ElasticSearch 7.x APIs. The recommended version to use is OpenSearch with no bundled JDK if you are managing Java separately. If OpenSearch is available on localhost port 9200 the default configuration in Moqui will find it, otherwise see configuration environment variables and such below for more options.

[https://opensearch.org/downloads.html](https://opensearch.org/downloads.html)

NOTE: Before the **java11** branch in the moqui-framework repository was merged on 25 April 2022 Moqui required Java 8 or later. For more information see [pull request 527](https://github.com/moqui/moqui-framework/pull/527).

### Moqui Binary Release Quick Start

1. Download a binary distribution like the **.war** file in the latest release
  - https://github.com/moqui/moqui-framework/releases/latest
1. Load the seed and demo data (will create H2 database and tables automatically):
  - `$ java -jar moqui.war load`
1. Run the framework (with embedded Servlet Container, Transaction Manager, Database):
  - `$ java -jar moqui.war`
1. In your browser (on the same machine) go to:
  - `http://localhost:8080/`
1. With the demo data loaded you can login with username "john.doe" and password "moqui"

### From Source Quick Start with OpenSearch

Use the following steps to do a local install from source and run with the default embedded database (H2) and OpenSearch installed in the runtime/opensearch directory.

1. Clone the moqui-framework repository
  - `$ git clone https://github.com/moqui/moqui-framework.git moqui`
  - `$ cd moqui`
1. Get desired components, for example PopCommerce and/or HiveMind
  - `$ ./gradlew getComponent -Pcomponent=PopCommerce`
  - `$ ./gradlew getComponent -Pcomponent=HiveMind`
  1. Alternatively just get the default runtime directory (if you don't want any components)
    - `$ ./gradlew getRuntime`
1. Download OpenSearch (Linux/Mac/Windows, OSS no-JDK version)
  - `$ ./gradlew downloadOpenSearch`
1. Build then load seed and demo data (the load task depends on the build task)
  - `$ ./gradlew load`
1. Start Moqui with run OpenSearch (add 'no-run-es' to not run OpenSearch)
  - `$ java -jar moqui.war`
1. In your browser go to `http://localhost:8080`

### From Source Quick Start with Docker Compose

Use the following steps to do a local install from source and run with a database and OpenSearch in Docker containers separate from Moqui. This works best on Linux but can be used with some variations on MacOS and Windows.

1. Install Docker (docker-ce) and Docker Compose (docker-compose), make sure your user is in the 'docker' group, etc
  - [https://docs.docker.com/install/](https://docs.docker.com/install/)
  - [https://docs.docker.com/install/linux/linux-postinstall/](https://docs.docker.com/install/linux/linux-postinstall/)
1. Clone the moqui-framework repository
  - `$ git clone https://github.com/moqui/moqui-framework.git moqui`
  - `$ cd moqui`
1. Get desired components, for example PopCommerce and/or HiveMind
  - `$ ./gradlew getComponent -Pcomponent=PopCommerce`
  - `$ ./gradlew getComponent -Pcomponent=HiveMind`
  1. Alternatively just get the default runtime directory (if you don't want any components)
    - `$ ./gradlew getRuntime`
1. Build Moqui and create the moqui-plus-runtime.war file
  - `$ ./gradlew addRuntime`
1. Build a local Docker image using the default name **moqui** (see the Docker section below for using a different group/name, pushing to a Docker repository, etc)
  - `$ cd docker/simple`
  - `$ ./docker-build.sh`
1. Got back to the **docker** directory
  - `$ cd ..`
1. Create a Docker Compose YML file, you can start with one of the files in the docker directory
1. Start the configured containers using the compose-up.sh script (replace the filename with your preferred compose file)
  - `$ ./compose-up.sh moqui-ng-my-compose.yml`
  - When Moqui starts for the first time it will see the database is empty (no records in the table for the Enumeration entity) and will automatically load the configured data sets; with the default MoquiProductionConf.xml file that includes all **seed**, **seed-initial**, and **install** data files
1. If you use one of these default files with the VIRTUAL_HOST for nginx-proxy set to **moqui.local** add a line for it in /etc/hosts like:
  - `127.0.0.1	moqui.local`
1. Access Moqui in your browser
  - In your browser go to `https://moqui.local` or whichever host you configured
  - If you use moqui.local and the included self-signed certificate you'll get a warning about that in your browser and will need to follow the links to go there regardless of the certificate
  - When you access Moqui for the first time and there are no users in the database (no demo, etc data loaded) the Login screen will show a form to create an admin user
1. Stop the configured containers (make sure to use the same YML file you used to start)
  - `$ ./compose-down.sh moqui-ng-my-compose.yml`
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
| no-run-es | Don't Try starting and stopping ElasticSearch or OpenSearch in runtime/elasticsearch |

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
| no-run-es | Don't try starting and stopping ElasticSearch or OpenSearch in runtime/elasticsearch |

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
1. Create a derived WAR file based on the moqui.war file and with your runtime directory contents and MoquiInit.properties file with: `"./gradlew addRuntime"` or `"ant add-runtime"`
1. Copy the created WAR file (moqui-plus-runtime.war) to deployment target
1. Run server (or restart to deploy live WAR)

## 5. Component Management

The best way to manage source repositories for components is to have one repository (on GitHub or elsewhere) per component that contains only the component directory.

Following this pattern the Gradle build scripts in Moqui have tasks to download components and their dependencies from a git repository, or from current or release archives.

Known open source components are already configured in the `addons.xml` file. To add private and other components or override settings for components in the addons.xml file, create a file called `myaddons.xml` and put it in the moqui directory.

Here is a summary of the Gradle tasks for component management (using the HiveMind component for example). All of the get tasks get the specified component plus all components it depends on (as specified in its component.xml file).

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

The examples above use the Gradle Wrapper (gradlew) included with Moqui. You can also install Gradle (2.0 or later) The load and run tasks depend on the build task, so the easiest to get a new development system running with a populated database is:

|   |   |
| --- | --- |
| Linux/Mac Gradle Wrapper | `$ ./gradlew load run` |
| Windows Gradle Wrapper | `> gradlew.bat load run` |
| Installed Gradle | `$ gradle load run` |

This will build the war file, run the data loader, then run the server. To stop it just press <ctrl-c> (or your preferred alternative).

## 7. ElasticSearch Configuration and Install

### External ElasticSearch

Note that we recommend using OpenSearch now as a default. The configuration is essentially the same. If you have questions, you can ask on the forum.

In production it is more common to have an external ElasticSearch cluster running separate from the Moqui server or cluster. This can also be used for local development where you start, stop, clear data, etc separate from Moqui or the Moqui Gradle tasks. This will work with any variation of ElasticSearch version 7.0.0 or later (OSS or not, with or without JDK, hosted by Elastic or AWS, etc). If you are installing ElasticSearch the recommended variation is the OSS with no JDK:

[https://www.elastic.co/downloads/elasticsearch-oss-no-jdk](https://www.elastic.co/downloads/elasticsearch-oss-no-jdk)

The configuration for ElasticSearch clusters is in the Moqui Conf XML file with a 'default' cluster in the MoquiDefaultConf.xml file that uses environment variables (or Java system properties) for easier configuration. See the section below for ElasticSearch and other environment variables available. Unless you are using an ElasticSearch install that requires HTTP Basic Authentication the only env var (property) you need to configure is `elasticsearch_url` which defaults to `http://localhost:9200`.

### ElasticSearch Installed in Runtime

ElasticSearch may be installed in the `runtime/elasticsearch` directory and run by Moqui when it starts (through MoquiStart only) as well as started, stopped, and data cleaned through various Gradle tasks. In local development environments it is more common to run a local instance of ElasticSearch and clear the data in it along with the H2 database data. This can also be used for production environments where you do not need or want a separate ElasticSearch cluster.

Note that the current support for ElasticSearch installed in runtime/elasticsearch in MoquiStart and Gradle tasks is limited to Unix variants only (ie Linux, MacOS) and uses the OSS no-JDK build for Linux (with no JDK it also works on MacOS). This will not currently work on Windows machines, so if you're doing development on Windows you get to install and manage ElasticSearch separately, just make sure it's available at `http://localhost:9200` (or configure `elasticsearch_url` to point elsewhere).

Make sure that the `JAVA_HOME` environment variable is set so ElasticSearch knows where to find the Java JDK.

To install ElasticSearch in runtime/elasticsearch the easiest way is to use the Gradle task. This will download the OSS no-JDK Linux, Mac, or Windows build of ElasticSearch and expand the archive in runtime/elasticsearch.

`$ ./gradlew downloadElasticSearch`

In Gradle there are also `startElasticSearch` and `stopElasticSearch` tasks. Note that Gradle supports partial task names as long as they match a single task so you can use shorter task names like `downloadel`, `startel`, and `stopel`.

`$ ./gradlew startel`
`$ ./gradlew stopel`

These report a message when trying to start or stop, and do nothing if they don't find an ElasticSearch install (if the `runtime/elasticsearch/bin` directory does not exist) or they find that ES is already running or not running (is running if the `runtime/elasticsearch/pid` file exists). Because of this if you aren't sure of ElasticSearch is running or not you can run `startel` to make sure it's running or `stopel` to make sure it's not running.

The `cleanDb`, `load`, `loadSave`, `reloadSave`, and `test` tasks all respect the runtime/elasticsearch install. If ES is running (pid file exists) cleanDb will stop ES, delete the data directory, then start ES. Note that the `test` task automatically starts ES if the `bin` directory exists (detect ES install) and the `pid` file does not, but it does not currently stop ES after running all tests.

The `MoquiStart` class will try to start ElasticSearch installed in runtime/elasticsearch if it finds a 'bin' directory there. To disable this behavior use the `no-run-es` argument. To use this just run Moqui with:

`$ java -jar moqui.war`

This also works with along with the load argument, ie:

`$ java -jar moqui.war load`

This will start and stop ElasticSearch along with Moqui, running it in a forked process using `Runtime.exec()`. Note that the MoquiStart class is used when running the executable WAR with `java -jar` as in the examples above, and when running from the root directory of the expanded WAR file as the Procfile does, like:

`java -cp . MoquiStart port=5000 conf=conf/MoquiProductionConf.xml`

The MoquiStart class is NOT used when you drop the embedded WAR file in an external Servlet Container like Tomcat or Jetty. If you deploy Moqui that way you must use an external ElasticSearch server or cluster.

For a local development instance of Moqui a common development cycle is to clean then load data, run tests, reload data from saved archives and run tests, etc. To do a full test run make sure ElasticSearch is installed in `runtime/elasticsearch` and preferably is not already running, then do:

`$ ./gradlew loadsave test stopel`

After running that to reload the data saved just after the initial data load (including H2 and ElasticSearch data) and run a specific component's tests (like mantle-usl), just run:

`$ ./gradlew reloadsave startel runtime:component:mantle-usl:test stopel`

After running a build, load, etc through whatever approach you prefer just start Moqui and it starts and stops ElasticSearch:

`$ java -jar moqui.war`

Those are examples of common things to do in local development and can vary depending on your preferred process and Gradle tasks.

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
| entity_add_missing_startup | true | Defaults to true for MySQL, set to 'false' to not add missing tables, columns, etc on startup |

To configure the ElasticSearch client built into Moqui Framework use the following environment variables:

| Env Var or Property | Example | Description |
| --- | --- | --- |
| elasticsearch_url | http://localhost:9200 | The base URL for the ElasticSearch server |
| elasticsearch_user |  | The user for HTTP Basic Authentication on the ES server |
| elasticsearch_password |  | The password for HTTP Basic Authentication on the ES server |

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

### Moqui Conf XML File

Database (or datasource) setup is done in the Moqui Conf XML file with `moqui-conf.entity-facade.datasource` elements. There is one element for each entity group and the `datasource.@group-name` attribute matches against `entity.@group-name` attribute in entity definitions. By default in Moqui there are 4 entity groups: `transactional, nontransactional, configuration, and analytical`. If you only configure a `datasource` for the `transactional` group it will also be used for the other groups.

Here is the default configuration for the H2 database:

```xml
<datasource group-name="transactional" database-conf-name="h2" schema-name=""
        start-server-args="-tcpPort 9092 -ifExists -baseDir ${moqui.runtime}/db/h2">
    <!-- with this setup you can connect remotely using "jdbc:h2:tcp://localhost:9092/MoquiDEFAULT" -->
    <inline-jdbc pool-minsize="5" pool-maxsize="50">
        <xa-properties url="jdbc:h2:${moqui.runtime}/db/h2/MoquiDEFAULT" user="sa" password="sa"/>
    </inline-jdbc>
</datasource>
```

The database-conf-name attribute points to a database configuration and matches against a `database-list.database.@name` attribute to identify which. Database configurations specify things like SQL types to use, SQL syntax options, and JDBC driver details.

This example uses a xa-properties element to use the XA (transaction aware) interfaces in the JDBC driver. The attribute on the element are specific to each JDBC driver. Some examples for reference are included in the MoquiDefaultConf.xml file, but for a full list of options look at the documentation for the JDBC driver.

The JDBC driver must be in the Java classpath. The easiest way get it there, regardless of deployment approach, is to put it in the `runtime/lib` directory.

Here is an example of a XA configuration for MySQL:

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
| `$ gradle addRuntime` | Build then create the moqui-plus-runtime.war file |
| `$ cd docker/simple` |  |
| `$ ./docker-build.sh ../.. mygroup/myrepo` | Build Docker image using Dockerfile, tagged latest by default |
| `$ docker tag mygroup/myrepo:latest mygroup/myrepo:1.0.0` | Add a tag for the version of the image |
| `$ docker login -u <username> -p <password>` | Login to Docker Hub (or other image repo) if not already logged in |
| `$ docker push mygroup/myrepo` | Push to Docker Hub (or elsewhere) |

On the server where the image will run make sure Docker (docker-ce) and Docker Compose (docker-compose) are installed and then pull the image created above.  There are various Docker Compose examples in the moqui/docker directory:

[https://github.com/moqui/moqui-framework/tree/master/docker](https://github.com/moqui/moqui-framework/tree/master/docker)

You'll need to create a custom compose YAML file based on one of these. This is where you put database, host, and other settings and is where you specify the image to use (like mygroup/myrepo above). To pull your image and start it up along with other Docker images for other needed applications (nginx, mysql or postgres, etc) do something like:

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
web: java -cp . MoquiStart port=5000 conf=conf/MoquiProductionConf.xml run-es
```

Note that it does not contain memory options so that they may be set with the JAVA_TOOL_OPTIONS environment variable. For example set it to "-Xmx1024m -Xms1024m" for a 1024 MB Java heap. The heap size on a dedicated instance should be about 1/2 the total system memory (leaving room for off-heap Java memory usage and operating system memory usage). 

The 'run-es' argument tells the MoquiStart class to run ElasticSearch if installed in runtime/elasticsearch. To install the Linux, Mac, or Windows no-JDK version of ElasticSearch download and expand the archive manually in runtime/elasticsearch or use the Gradle download task:

```
$ ./gradlew downloadElasticSearch
```

The archive to deploy is basically just the moqui-plus-runtime.war file. The WAR file must be renamed from .war to .zip so that the AWS Java SE environment treats it like a plain archive and not an executable jar. To build a file to upload to AWS ElasticBeanstalk do something like:

|   |   |
| --- | --- |
| `$ gradle addRuntime` | Build then create the moqui-plus-runtime.war file |
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
    - elasticsearch  : Optional ElasticSearch install directory
    - opensearch  : Optional OpenSearch install directory
    - lib            : JAR files to add to the runtime classpath
    - log            : Log files will go here
    - template       : General Templates
    - tmp            : Temporary files
    - txlog          : Transaction log files will go here (Atomikos or Bitronix files)
```

The main place to put your components is in the runtime/component directory. When you use the Gradle get component tasks this is where they will go.

Components with declared dependencies (in a component.xml file in the component directory) will be loaded after the component(s) they depend on.
