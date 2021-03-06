#!/bin/bash
echo
system_install_root='/home/matt/'
install_root='yab/'
install_name='FatController/'
data_name='data/'
echo "Creating dir strutures..."
if [ ! -d ${system_install_root}${install_root} ];
then
	mkdir ${system_install_root}${install_root}
else
	echo "${system_install_root}${install_root} found."
fi
if [ ! -d ${system_install_root}${install_root}${install_name} ];
then
	mkdir ${system_install_root}${install_root}${install_name}
else
	echo "${system_install_root}${install_root}${install_name} found."
	echo "This install will overwrite existing files."
fi
if [ ! -d ${system_install_root}${install_root}${install_name}${data_name} ];
then
	mkdir ${system_install_root}${install_root}${install_name}${data_name}
else
	echo "${system_install_root}${install_root}${install_name}${data_name} found. I will leave your data files intact."
fi
echo
echo "Copying files..."
for file in $(ls) 
do
	cp -r "${file}" ${system_install_root}${install_root}${install_name}
done




