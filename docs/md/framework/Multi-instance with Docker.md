# Multi-instance Moqui with Docker

[TOC levels=2]

This walkthrough uses Docker Compose for nginx-proxy, MySQL, and OpenSearch, then a Moqui process on the host for Instance Management. Compose files, helper scripts, and image versions live in `moqui/docker/` (see `docker/README.md`).

nginx-proxy here is TLS and HTTP routing, not a web application firewall. Moqui is designed to run **behind** a WAF (and a reverse proxy). In production put a WAF in front, or use a proxy that includes WAF features. See [Run and Deploy](/docs/framework/Run+and+Deploy) (Production security) and [Security](/docs/framework/Security).

## Step 1: Configure Docker to listen to HTTP/TCP on localhost

The Instance Management services talk to the Docker daemon over HTTP on port 2375 (see the default `InstanceHost` seed data). The Docker daemon needs an additional `-H` argument such as this one for TCP:

```bash
$ dockerd -H unix:///var/run/docker.sock -H tcp://127.0.0.1:2375
```

For Linux systems Docker is often run with systemd. See Docker's current remote-access documentation, especially the `ExecStart` override. Add the TCP listener and leave the existing socket (`unix://` or `fd://`) as-is:

[https://docs.docker.com/engine/daemon/remote-access/](https://docs.docker.com/engine/daemon/remote-access/)

A note for Mac OS X (macOS): because of the way Docker runs on a Mac this is difficult to set up. Options include hacking around the Docker.app files, or using socat to forward HTTP requests to a Unix socket. It is much easier in general to work with Docker on Linux. Under Windows Docker often uses HTTP/TCP by default instead of a Unix socket, so additional setup may not be needed.

## Step 2: Build the moqui Docker image

```bash
# starting in the moqui directory (moqui-framework root), build moqui and create the moqui-plus-runtime.war file
$ ./gradlew cleanAll build addRuntime
# build the Docker image based on the moqui-plus-runtime.war file
$ cd docker/simple
$ ./docker-build.sh
# make sure there is an image called 'moqui'
$ docker images
```

## Step 3: Start nginx-proxy and MySQL

When this runs it will bind to ports 80 and 443 on the host (and 3306 / 9200 on localhost only), so make sure those are free first. If you change the compose file that will vary (such as setting up HTTPS on port 443).

Use `mysql-compose.yml` for nginx-proxy, MySQL, and OpenSearch **without** a Moqui container. That is the layout Instance Management expects: Moqui instances are created later as additional containers on the same Docker network.

```bash
# starting in the moqui/docker directory
$ ./compose-up.sh mysql-compose.yml
# make sure the 'nginx-proxy' and 'moqui-database' services are running
$ docker ps
# make sure the 'moqui_default' network exists
$ docker network ls
```

This will start nginx-proxy, MySQL, and OpenSearch, and with the project/app name `moqui` will create a network called `moqui_default` that other Moqui instances will use to automatically set up the virtual host reverse proxy and to connect to the database. The default InstanceImageType settings for `imageTypeId=moqui` refer to the moqui-database container running on the same Docker network for the database. To use a different database you can change the default settings, add a new InstanceImageType, or change the corresponding AppInstanceEnv values, along with a different DatabaseHost record for the admin settings of the database server.

There is a matching `postgres-compose.yml` if you prefer Postgres instead of MySQL.

## Step 4: Build and run a Moqui server for Instance Management

```bash
# starting in the moqui directory, build moqui and load data
$ ./gradlew cleanAll load
# make sure a MySQL JDBC driver jar is in runtime/lib
$ ./gradlew getMySqlJdbc
# start moqui
$ java -jar moqui.war
```

You can also download a driver and place the JAR in `runtime/lib` yourself; do not assume a particular connector version.

Note that this is **not** running in a Docker container, but on the same system as the Docker host so it can talk to the Docker host over HTTP using the settings from Step 1. Following these instructions it will run with an embedded H2 database for its own data, but will use the MySQL JDBC driver to talk to the database running in a Docker container by its exposed port (see the `mysql-compose.yml` file).

## Step 5: Use the Instance screens to create and provision an instance

1. In your browser go to Instance Mgmt in the System app: `http://localhost:8080/qapps/system/Instance`
2. Click on the "Create App Instance" button
    - leave Instance Name blank (will default to Host Name with dots replaced by underscores)
    - in Host Name enter 'moqui.local'
    - in Image select 'moqui - Docker - Moqui Framework'
    - in Instance Host select 'Docker - 127.0.0.1'
    - in Database Host select 'MySQL - 127.0.0.1'
    - submit the form (click on the Create button)
3. Check connection to the database and Docker host
    - Click on the Check DB button for the Instance, under the Database column
    - Click on the Check button under the Instance column
4. Create the Database for the Instance
    - Click on the Create DB button under the Database column
5. Initialize and start the Docker container
    - Click on the Init button under the Instance column
    - Click on the Start button under the Instance column

## Step 6: Check the moqui.local instance

You can see if the instance is running from the Instances screen using the 'Check' button in the Instance column. You can also use docker directly to see if the instance is running (with `docker ps`).

To see the logs for the instance use something like `docker logs -f moqui_local`

To resolve the moqui.local domain name add it to the system, i.e. in `/etc/hosts`.

Now in your browser you can go to `http://moqui.local` and if all worked properly you will see a fresh copy of Moqui running with production settings and a database with only seed, seed-initial, and install data loaded. Note that there are no users yet in the system so the Login screen will show you a form to create an admin user. This should be done right away after setting up a new instance so that option is disabled.
