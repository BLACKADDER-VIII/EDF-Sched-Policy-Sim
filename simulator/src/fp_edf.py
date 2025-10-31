class Fp_edf_sched:
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
        priority_q = []
        for t in self.task_list:
            priority_q.append(t.release(0))
        preemtions = 0
        priority_q.sort()
        curr_job = None

        # Add something to graph the execution for small task set cases

        for it in range(iter):
            print(priority_q)
            if curr_job: 
                curr_job.exec_remain -= 1
                if curr_job.exec_remain <= 0:
                    curr_job = None
                    
            # Check task set for new releases
            for t in self.task_list:
                if t.next_release == it:
                    print(f"Adding job from task: {t.period}")
                    priority_q.append(t.release(it))

            priority_q.sort()
            if curr_job == None and len(priority_q):
                curr_job = priority_q.pop(0)
            elif len(priority_q) and priority_q[0] < curr_job:
                # Preempt
                preemtions+=1
                priority_q.append(curr_job)
                curr_job = priority_q.pop(0)
                priority_q.sort()
            print(f"Iter: {it} Task: {'None' if not curr_job else curr_job.deadline}")
        
        print(f"Number of preemptions: {preemtions}")