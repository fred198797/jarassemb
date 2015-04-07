Jarassemb is a tool that helps to aggeregate classes no matter from target folder or in dependency jars. The result is an archieve jar which groups these classes based on configuration.


The using scenario can be separated to three parts:

1. You need to place your sources into the folders (src/java, src/class or src/jar) or type these path in arguments. 

2. Configure the assembly job in jarassemb.json

3. run start script (intermediate classes were generated at folder 'classes' and the output archieve is in 'output 'folder )

   command : python jarassemb.py (class_path | jar_path)

   * you can also put the script in your java project and executed by maven plugin [exec-maven-plugin]
