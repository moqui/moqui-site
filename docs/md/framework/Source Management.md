
# Source Management Guide

[TOC levels=2-4]

## Moqui Ecosystem Repositories

Moqui Ecosystem is made up of dozens of repositories so you can choose the tools, business artifacts, applications, and integrations you need while not worrying about the rest. All repositories represent a component that goes in the `runtime/component` directory with the exception of the framework (`moqui-framework`) and the default runtime directory (`moqui-runtime`).

Moqui Framework and all other core Moqui Ecosystem repositories are [hosted on GitHub](https://github.com/moqui). These repositories are all configured in the `addons.xml` file (in the root of moqui-framework repository) to make it easy to do git operations such as get/clone, pull, and status for all repositories including all components of your own you might add.

The same structure of one git repository per component is recommended for your own components as well.

## Gradle Tasks for Source Management

Because each component is in its own git repository your local working directory will typically have a dozen or more git repositories to keep track of. To simplify working with multiple git repositories there are various Gradle tasks in the root `build.gradle` file in `moqui-framework`.

Note that Gradle matches task names by partial strings as long as they match a single task so the table below includes the full task name plus some recommended shortcuts.

To see a list of all available Gradle tasks: `./gradlew tasks --all`

Most of the Moqui tasks have descriptions with usage information including required properties. Passing properties to a Gradle task is somewhat cumbersome, done with `-P<name>=<value>` parameters. Prefer the Gradle wrapper (`./gradlew`, Gradle 9.2) so the version matches the project.

Gradle Task | Short | Example | Description
------------|-------|---------|------------
getComponent | | `./gradlew getComponent -Pcomponent=PopCommerce` | Get the specified component, matching a name in the addons.xml or myaddons.xml files, plus all its dependencies
getDepends | | `./gradlew getDepends` | Get dependencies for all installed components
getRuntime | | `./gradlew getRuntime` | Get the runtime directory if missing, plus default components from `myaddons.xml` (`addons.@default`)
createComponent | | `./gradlew createComponent -Pcomponent=MyComponent` | Create a new component from the `start` template
gitStatusAll | gits | `./gradlew gits` | Do a git **status** on framework, runtime, and all component repositories
gitPullAll | gitp | `./gradlew gitp` | Do a git **pull** on framework, runtime, and all components
gitUpstreamAll | gitu | `./gradlew gitu` | Do a git **upstream pull** on all repositories that have a remote called 'upstream', generally set to the original moqui repository to do upstream mergers into your forked repositories
gitCheckoutAll | | `./gradlew gitCheckoutAll -Pbranch=master` | Check out a branch (or tag) on framework, runtime, and all components

The `settings.gradle` file in moqui-framework has a script to find all components with a `build.gradle` file and automatically adds them to the top level module. Because of this all common tasks such as **build**, **test**, etc will run on components automatically.

## Add On Component Repositories and `myaddons.xml`

In general when working with Moqui you should keep all of your code and other artifacts in one or more add on components with a git repository for each.

Each component should declare other components it depends on using a `component.xml` file. This is used by the Gradle getComponent task to automatically get other needed components and it is used to make sure all dependent components are in place when Moqui starts up. Here is an example component.xml file with some dependencies:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component name="MyComponent" version="1.0.0">
    <depends-on name="mantle-udm" version=""/>
    <depends-on name="mantle-usl" version=""/>
    <depends-on name="SimpleScreens" version=""/>
</component>
```

The component name should match the directory name it lives in, which is the name of the git repository.

To tell the Gradle tasks about your component add them in a `myaddons.xml` file located in the moqui root directory, alongside `addons.xml`. This is preferred to modifying addons.xml so that your components and source repository locations and such are kept separate from the stock Moqui components and repositories.

The `myaddons.xml` file has the same structure as `addons.xml` and can be used to both add and override settings there. For example you can specify alternate repositories and components to point to your forks of any Moqui repository such as `mantle-usl` and `SimpleScreens`.

Here is a very simple example to add a single custom component:

```xml
<addons default="MyComponent">
    <component name="MyComponent" group="MyGroup" version="" branch="master" repository="github-ssh"/>
</addons>
```

This uses the **github-ssh** repository defined in `addons.xml` so that it is downloaded via SSH instead of by HTTPS. This is convenient when working with private repositories to avoid authentication issues. The Gradle tasks use a Git client written in Java which will generally pick up your SSH keys in the `~/.ssh` directory (for Mac and Linux).

Here is an example of a more complex `myaddons.xml` file that overrides the location of the runtime directory and a number of stock Moqui components, along with adding custom components:

```xml
<addons default="MyComponent,OtherComponent" default-repository="MyRepo">
    <repository name="MyRepo">
        <location type="git" url="git@github.com:${component.'@group'}/${component.'@name'}.git"/>
    </repository>

    <runtime name="moqui-runtime" group="MyGroup" version="" branch="master"/>

    <component name="mantle-udm" group="MyGroup" version="" branch="master"/>
    <component name="mantle-usl" group="MyGroup" version="" branch="master"/>
    <component name="SimpleScreens" group="MyGroup" version="" branch="master"/>

    <!-- Private Components -->
    <component name="MyComponent" group="MyGroup" version="" branch="master"/>
    <component name="OtherComponent" group="MyGroup" version="" branch="master"/>
</addons>
```

To use SSH instead of HTTPS for all components this uses the `default-repository` attribute along with a `repository` element to specify the git location for a custom repository (standard GitHub URL in this example, same as github-ssh in the stock addons.xml file).

## Forking Moqui Repositories

There are many reasons you might want to fork the stock Moqui repositories. This is necessary to create pull requests on GitHub to submit contributions. You can also use this to manage your modifications to Moqui framework, runtime, and stock components and still maintain an upstream link for periodic upstream merges.

One important best practice when using Moqui is to **avoid** changing the stock Moqui source code and other artifacts. This makes it easier to update and is made possible by dozens of framework features that allow you to register tools, add screens to the default *webroot* screen tree, trigger your own services on various business events, change look and feel, and much more.

## Command Line Examples

### Fresh Local Setup

```bash
# clone moqui-framework
$ git clone https://github.com/moqui/moqui-framework.git moqui
$ cd moqui
# optionally copy in your myaddons.xml file, such as the example above
$ cp ~/myaddons.xml .
# get MyComponent and its dependencies
$ ./gradlew getComponent -Pcomponent=MyComponent
# build, load seed/install/demo/etc data, run tests
$ ./gradlew load test
# run Moqui
$ java -jar moqui.war
```

### Configure Upstream for Forked Repository

```bash
$ cd runtime/component/mantle-usl
# view existing remotes
$ git remote -v
# add upstream remote with HTTPS URI (use git@... style for SSH access)
$ git remote add upstream https://github.com/moqui/mantle-usl.git
# use the Gradle task to merge (pull) from upstream
$ cd ../../..
$ ./gradlew gitu
```
