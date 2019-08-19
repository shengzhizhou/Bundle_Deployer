# Bundle_Deployer

# Instruction
# 
zip structure
	
~~~
src/
		
	old_text.txt
	
build/
				
	manifest.py

~~~
#Bundle_Packager
~~~

Required Arguments:
  
-h, --help       	show this help message and exit
  
-sp, --srcpath    	Input src Repo Local Path
  
-zp, --zippath    	Input root Path for bundle zip file
  
-sb, --srcbranch  	Input src branch
  
-db, --destbranch 	Input destination branch

~~~


#Bundle_Deployer
~~~
Required Arguments:

-h, --help            show this help message and exit
-dp, --destpath       Input destination Repo Local Path
-rp, --rootpath       Input Unzipped Folder Root Path

~~~
#cmd Sample
~~~

python.exe bundle_packager.py -sp C:\Users\szhou\Desktop\Test\BundleTest -zp C:\Users\szhou\Desktop\copyfile -sb prestage -db master


python.exe C:\Users\szhou\PycharmProjects\BundleProject\sample\bundle_deployer.py -dp C:\Users\szhou\Desktop\master -rp C:\Users\szhou\Desktop\copyfile
~~~