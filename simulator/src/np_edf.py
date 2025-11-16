class Np_edf_sched:
    def __init__(self, task_list):
        self.task_list = task_list
    
    def check_schedulability(self):
        density = 0
        for t in self.task_list:
            density += float(t.exec_time)/t.deadline
        if density > 1:
            return False
        return True
    
    def simulate(self, iter):
        if not self.check_schedulability():
            print("The task set has density higher than 1. Not schedulable")
            return
        task_q = []
        for t in self.task_list:
            task_q.append(t.release(0))
        task_q.sort()
        deadline_misses = 0
        curr_job = None
        for it in range(iter):
            if curr_job:
                curr_job.exec_remian -= 1
                if curr_job.exec_remain == 0:
                    if curr_job.deadline > it:
                        deadline_misses += 1
                    curr_job = None
            for t in self.task_list:
                if t.next_release == it:
                    print(f"Adding job from task: {t.period}")
                    task_q.append(t.release(it))
            task_q.sort()
            if not curr_job and len(task_q):
                curr_job = task_q.pop(0)
        print(f"Number of deadline misses: {deadline_misses}")
            

            