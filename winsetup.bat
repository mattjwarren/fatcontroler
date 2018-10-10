rem 
rem Copyright 2005 MatthewWarren.
rem  Permission to copy is hereby granted so long as all actions taken
rem  remain within the terms specified by the GNU General Public License.
rem 
rem  This file is part of 'The FatController'
rem 
rem     'The FatController' is free software; you can redistribute it and/or modify
rem     it under the terms of the GNU General Public License as published by
rem     the Free Software Foundation; either version 2 of the License, or
rem     (at your option) any later version.
rem 
rem     'The FatController' is distributed in the hope that it will be useful,
rem     but WITHOUT ANY WARRANTY; without even the implied warranty of
rem     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
rem     GNU General Public License for more details.
rem 
rem     You should have received a copy of the GNU General Public License
rem     along with 'The FatController'; if not, write to the Free Software
rem     Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
rem 
mkdir "c:\program files\yab" >> c:\fcinstalllog.txt
mkdir "c:\program files\yab\FatController" >> c:\fcinstalllog.txt
set installpath="c:\program files\yab\FatController\" >> c:\fcinstalllog.txt
copy FatControllerCommands.sav %installpath% >> c:\fcinstalllog.txt
copy general.sav %installpath% >> c:\fcinstalllog.txt
copy FatController.hlp %installpath% >> c:\fcinstalllog.txt
copy FatController.* %installpath% >> c:\fcinstalllog.txt
copy "AdminGuide.doc" %installpath% >> c:\fcinstalllog.txt
copy winsetup.bat %installpath% >> c:\fcinstalllog.txt
copy unixsetup.ksh %installpath% >> c:\fcinstalllog.txt
copy COPYING %installpath% >> c:\fcinstalllog.txt
copy FC_*.* %installpath% >> c:\fcinstalllog.txt
copy *.jpg %installpath% >> c:\fcinstalllog.txt

