import minescript as ms
from typing import overload

def _self_job():
    return [job for job in ms.job_info() if job.self][0]

class self:
    job = _self_job()
    job_id = job.job_id
    parent_job_id = job.parent_job_id if not job.parent_job_id is None else None
    source = job.source
    src = source
    command = job.command
    cmd = command
    # print("job:", job)
    # print("job_id:", job_id)
    # print("parent_job_id:", parent_job_id)
    # print("source:", source)
    # print("src:", src)
    # print("command:", command)
    # print("cmd:", cmd)

# FUNCTIONS!!!! :O
@overload
def filter_parent_jobs():
    """
    Filters jobs if the current script's job id matches `job.parent_job_id`.
    """
    ...
@overload
def filter_parent_jobs(by: tuple[int]):
    """
    Filters jobs if ANY of job ids in the tuple matches `job.parent_job_id`.
    """
    ...
@overload
def filter_parent_jobs(by: int):
    """
    Filters jobs if the `by` argument matches `job.parent_job_id`.
    """
    ...
def filter_parent_jobs(by: int|tuple[int]=self.job_id):
    jobs = ms.job_info()
    result = []
    for job in jobs:
        if isinstance(by, int):
            if job.parent_job_id == self.job_id:
                result.append(job)
        elif isinstance(by, tuple):
            if any(job.parent_job_id == b for b in by):
                result.append(job)
    return result

@overload
def stop(): 
    """
    Stops the script using `killjob` (alternative to exit())
    """
    ...
@overload
def stop(job: ms.JobInfo|int): 
    """
    Stops a job using `killjob`
    """
    ...
def stop(job: ms.JobInfo|int=self.job_id):
    if isinstance(job, ms.JobInfo):
        ms.execute(f'\\killjob {job.job_id}')
    elif isinstance(job, int):
        ms.execute(f'\\killjob {job}')
def job_id_exists(n: int):
    jobs = ms.job_info()
    for job in jobs:
        if job.job_id == n:
            return True
    return False 
_IS_MAIN = __name__ == '__main__'
if _IS_MAIN:
    print([getattr(self, th) for th in dir(self)])
    stop()
