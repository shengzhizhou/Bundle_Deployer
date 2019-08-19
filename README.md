# Bundle_Deployer
# Instruction
zip structure
	src/  
		old_text.txt
	build/
		deployer.py
		manifest.py
~~~
Required Arguments:
  -h, --help       	show this help message and exit
  -sp, --srcpath    	Input src Repo Local Path
  -zp, --zippath    	Input root Path for bundle zip file
  -sb, --srcbranch  	Input src branch
  -db, --destbranch 	Input destination branch
~~~

~~~
python.exe bundle_packager.py -sp C:\Users\szhou\Desktop\Test\BundleTest -zp C:\Users\szhou\Desktop\copyfile -sb prestage -db master
~~~