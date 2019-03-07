#
#
#
# Version History
# 15/12/06  v1f11r1a GUI Version update. Bugfixes.
#                    Added green/amber/red lights to entity tabs
#                    Added ability to execute FC scripts on alert_pass and alert_fail
#                       * in defined scripts the sub ~ALERT_ENTITY can be
#                       used. This wil be defined as a substitution when an alert
#                       script is fired.
#                    Added alert status colour change for shell bar
#                    collectors now correctly datestamp file lines
#
# 07/12/06  v1f9r1a GUI version first release.
#                   changes to handle paned notebook output style.
#                   Added [[1..10,15,16]] notation to genreate lsits of commands.
#
# 21/09/05  v1f8r3a Enhanced alerting mechanism.
#                   repackage new file structure. (migrate away from monlith)
#           minor version string issue fixed
#
# 15/09/05  v1f8r2a packaging fixup
#
# 14/09/05  v1f8r1s Added ENTITYGROUP entity type
#               removed GUI code
#
# 28/05/05  v1f7r1a Bought under GNU public license.
#           DaemonManager class incorporated and code updated.
#
# 09/02/05  v1f6r1a Woo! up to version1 - the GUI.. or what there is of it!
#                   featureset still v6
#                   release 1 alpha
#
# 08/02/05  v0f6r2a fixed load IOErrors
# 08/02/05  v0f6r1a Switched Versioning Scheme to
#                   version()featureset()release()a/b/-
#                   Added new entity LOCAL, execs local cmds
#
# 02/02/05  v0.1.5a Added new options;
#                       FATCONTROLLER   VERBOSE yes/no
#                       TSM             DATAONLY yes/no
#                       FATCONTROLLER   DEVELOPER yes/no
#                       FATCONTROLLER   DEVELOPERPATH {path}
#
# 28/01/05  v0.1.4a Added scripting capability commands
#                       addline
#                       insline
#                       delline
#                       run
#
#v0.1.3a    Collectors now write data to file if filename!=�none�
#       collectors work with un-rooted filenames. IE; 
#           a filename will have �/opt/yab/FatController/data/� or �c:\� 
#           pre-pended to them depending on the type of system being used.
#       schedules are now shown in local-times rather than seconds-since-the-epoch. 
#       now+x notation now works for schedule start and end times.
#       Updated manual with entity reference.
#
#v0.1.2a    Now it really does work under unix!
#       fixed #dbg() trace bug.
#       fixed shell escaping issues. escaped substitutions will have 
#       the �\�s removed when executing from non-posix 
#       environment.
#
#v0.1.1 a   Now runs under unix and windows!
#       installers for unix and windows included!
#
#v0.1.0 a   Implementation of daemon framework
#
#v0.0.1a � v0.0.9a
#       Base implementation. (CLI / ENTITES / Commands)
#M.Warren
#
###########
