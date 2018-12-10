import re,time
###########
# START OF CLASS daemonschedule
#
class daemonschedule:
    '''Data structure holding information on the schedule for the daemon.

	Every daemon has a daemonschedule. The daemon runs according
	to this schedule, each time executing each task it owns
	against the entites for that task, and processing the output
	from that execution by all collectors attatched to the task.'''
    
    def __init__(self,start='now+0',end='now+3600',period='600'):
        '''Implements the 'now+' method of specifying times.'''
        if re.match('^now.*',start):
            start=time.time()+int(start[4:])
        self.starttime=start
        if re.match('^now.*',end):
            end=time.time()+int(end[4:])
        self.endtime=end
        self.period=int(period)


    def updateschedule(self,start='now',end='now+3600',period='600'):
        '''Implements the 'now+' method of specifying times.'''
        if re.match('^now.*',start):
            start=time.time()+int(start[4:])
        self.starttime=start
        if re.match('^now.*',end):
            end=time.time()+int(end[4:])
        self.endtime=end
        self.period=int(period)

    def getperiod(self):
        return self.period

    def getstart(self):
        return self.starttime

    def getend(self):
        return self.endtime

    def tostring(self):
        return str(self.starttime)+' '+str(self.endtime)+' '+str(self.period)

    def todatestring(self):
        return 'START::'+time.ctime(float(self.starttime))+'\t\tEND::'+time.ctime(float(self.endtime))+'\t\tPERIOD::'+str(self.period)
#
# END OF CLASS daemonschedule
###########
