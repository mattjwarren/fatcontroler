print
print "Creating dir strutures..."
if [ ! -d /opt ];
then
	mkdir /opt
else
	print "/opt found."
fi
if [ ! -d /opt/yab ];
then
	mkdir /opt/yab
else
	print "/opt/yab found."
fi
if [ ! -d /opt/yab/FatController ];
then
	mkdir /opt/yab/FatController
else
	print "/opt/yab/FatController found."
	print "This install will overwrite existing files."
fi
if [ ! -d /opt/yab/FatController/data ];
then
	mkdir /opt/yab/FatController/data
else
	print "/opt/yab/FatController/data found. I will leave your data files intact."
fi
print
print "Copying files..."
for file in $(ls)
do
	cp "${file}" /opt/yab/FatController
done
cd /opt/yab/FatController
chmod 775 *

