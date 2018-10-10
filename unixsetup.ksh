#!/bin/ksh
#
#Copyright 2005 MatthewWarren.
# Permission to copy is hereby granted so long as all actions taken
# remain within the terms specified by the GNU General Public License.
#
# This file is part of 'The FatController'
#
#    'The FatController' is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    'The FatController' is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with 'The FatController'; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
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

