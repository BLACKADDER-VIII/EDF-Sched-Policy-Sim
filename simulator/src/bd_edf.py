# Backlogged-density EDF scheduler

class Bd_edf_sched:
    def __init__(self, task_list):
        self.task_list = task_list

    def check_schedulability(self):
        density = 0
        for t in self.task_list:
            density += float(t.exec_time)/t.deadline
        if density > 1:
            return False
        return True

    def simulate(self, iter, aggr_thresh=0):    # aggr_thresh for aggressive mode threshold
        if not self.check_schedulability():
            print("The task set has density higher than 1. Not schedulable")
            return
        priority_q = []
        preemtions = 0
        deadline_misses = 0
        task_list = self.task_list
        backlogged_q = []
        curr_job = None
        def release_backlogged():
            for b in backlogged_q:
                priority_q.append(b)
                backlogged_q.clear()
        for task in task_list:
            priority_q.append(task.release(0))
        priority_q.sort()
        for it in range(iter):
            if curr_job: 
                if curr_job.deadline < it:
                    deadline_misses += 1
                    curr_job = None
                else:
                    curr_job.exec_remain -= 1
                    if curr_job.exec_remain <= 0:   # Job finished, release backlogged queue into priority q if exist
                        curr_job = None
                        if len(backlogged_q):
                            release_backlogged()
                            priority_q.sort()
                if curr_job and it >= curr_job.deadline:
                    deadline_misses += 1
                    curr_job = None
                        
            # Check task set for new releases in this iter
            for t in self.task_list:
                if t.next_release == it:
                    print(f"Adding job from task: {t.period}")
                    priority_q.append(t.release(it))
            priority_q.sort()
            if curr_job == None and len(priority_q):    # Backlogged q would be empty and integrated into priority q
                curr_job = priority_q.pop(0)
            elif len(priority_q) and priority_q[0] < curr_job:
                if priority_q[0].deadline-it <= curr_job.exec_remain:
                    # Preempt
                    preemtions+=1
                    priority_q.append(curr_job)
                    if len(backlogged_q):   # Release backlogged q since preemted
                        release_backlogged()
                    priority_q.sort()
                    curr_job = priority_q.pop(0)
                else:
                    # Preemption criteria test
                    # Calculate Real density
                    while len(priority_q) and priority_q[0] < curr_job:
                        real_d = curr_job.exec_remain/(curr_job.deadline-it) if curr_job.deadline > it else 1
                        back_d = 0
                        backlogged_q.append(priority_q.pop(0))
                        for ht in backlogged_q:
                            real_d += ht.exec_remain/(ht.deadline-it)
                            back_d += ht.exec_remain/(ht.deadline-it-curr_job.exec_remain)
                        print(f"Real: {real_d} Back: {back_d}")
                        if back_d > real_d + aggr_thresh:
                            # Preempt
                            preemtions+=1
                            priority_q.append(curr_job)
                            release_backlogged()
                            priority_q.sort()
                            curr_job = priority_q.pop(0)
            print(f"Iter: {it} Task: {'None' if not curr_job else curr_job.deadline}")
        print(f"Number of preemptions: {preemtions}")
        print(f"Number of deadline misses: {deadline_misses}")
        