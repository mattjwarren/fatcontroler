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

