# IntelliJ IDEA Setup

## Create Project from Gradle Files

While you can create a project from VCS sources in IntelliJ this is not recommended, it is better to use the Gradle tasks from the command line to do all the git cloning for the framework, runtime, and all the components you want. For instructions on this see the **Source Management Guide** and the **Run and Deploy** document. With the source all cloned:

- Create a Project from Existing Sources (File => New => Project from Existing Sources)
- select the **moqui** root directory (whatever you named it, *moqui-framework* by default from the git repository name) then click on **OK**
- select *Import project from external model* and under it select **Gradle**, then click on **Next**
- verify the *Gradle project* location, the directory containing the moqui root build.gradle file
- for other options on this dialog do what you prefer, I usually leave all checkboxes un-checked, set *Group modules* to *using explicit module groups*, and because I have gradle setup locally I choose the *Use local gradle distribution* option and specify the directory where it is (generally ~/gradle, may be elsewhere)
- make sure you have a JVM already setup in IntelliJ and select a Java 11 JDK for *Gradle JVM*
- for project format I prefer *.idea (directory based)*
- you may specify other advanced options
- click on **Finish** and let it do the initial gradle build

Once the window comes up you should see a message that says *Unregistered VCS roots detected*. Click on that, or go to the **Version Control** pane in the Settings dialog (File => Settings). There is will list the directories for all git repositories under *Unregistered roots*. Click on each and then on the green plus sign on the right.

This will give you the basic setup. As you update moqui-framework and others getting new build.gradle files IntelliJ will tell you its Gradle configuration is out of date. Click on the notification or the Gradle button (usually on the far right), then click on the blue circle/arrows button on the left to *Refresh all Gradle projects*.

## XML Schemas

IntelliJ requires some configuration to tell it which local file has the XSD for a given schema location. 

The easiest and best way to set up the XML Schemas is to run the following in a moqui-framework repo:
```
./gradlew setupIntellij
```
Thanks to [Taher's PR here](https://github.com/moqui/moqui-framework/pull/481).

To do this manually, open an existing Entity Definition, Service Definition, XML Screen, Service REST API, or other XML file and copy the value of the `xsi:noNamespaceSchemaLocation` attribute on the root element. Once you have the schema location copied, open the Settings dialog (File => Settings) and type in 'schema' in the search box to quickly get to the *Languages & Frameworks* => *Schemas and DTDs* pane. Once there:

- click on the green plus on the right
- paste in the schema location in the *URI* field
- double-click on the matching file under the **framework** folder
- the dialog will close and you'll see the XSD added to the list
- click on OK to close the Settings window and give it a second to process the XML file you had open now that it knows about the schema

## Language Injection for Groovy in XML

In the Settings dialog (File => Settings) go to the Editor => Language Injections section. You will want one for at least the `script` element and nice to have them for attributes like `from`, `condition`, and `in-map`.

For the `script` and other elements:

- click on the green plus on the right
- select **XML Tag Injection**
- specify a name ('script groovy' or something)
- select **Groovy** for *Language => ID*
- type in **script** for *XML Tag => Local Name*
- leave everything else blank or as-is

For attributes it is the same except use **XML Attribute Injection** and specify the *XML Attribute => Local Name*. You can limit this to the attribute on specific elements, but that extra work is probably only worth it if you run into issues when editing other (non-Moqui) XML files with the same attribute names.
