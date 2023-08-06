from enum import Enum

class SpecsEndpoints(str, Enum):
    submitjob = "/submitjob"
    checkjob = "/checkjob"
    getcursolution = "/getcursolution"
    getcurlog = "/getcurlog"
    getresults = "/getresults"

class JobStatus(str, Enum):
    finished = "Finished"
    error = "Error"
    running = "Running"
    created = "Created"
    timeout = "Timeout"