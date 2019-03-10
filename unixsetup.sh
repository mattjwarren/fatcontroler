echo
echo "Creating dir strutures..."
if [ ! -d /opt ];
then
	mkdir /opt
else
	echo "/opt found."
fi
if [ ! -d /opt/yab ];
then
	mkdir /opt/yab
else
	echo "/opt/yab found."
fi
if [ ! -d /opt/yab/FatController ];
then
	mkdir /opt/yab/FatController
else
	echo "/opt/yab/FatController found."
	echo "This install will overwrite existing files."
fi
if [ ! -d /opt/yab/FatController/data ];
then
	mkdir /opt/yab/FatController/data
else
	echo "/opt/yab/FatController/data found. I will leave your data files intact."
fi
echo
echo "Copying files..."
for file in $(ls)
do
	cp "${file}" /opt/yab/FatController
done
cd /opt/yab/FatController
chmod 775 *

