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
            t.release(0)
            priority_q.append(t)
        preemtions = 0
        priority_q.sort()
        curr_task = None

        # Add something to graph the execution for small task set cases

        for it in range(iter):
            if curr_task: 
                if curr_task.exec_remain == 0:
                    curr_task = None
                else:
                    curr_task.exec_remain -= 1
            # Check task set for new releases
            for t in self.task_list:
                if t.next_release == iter:
                    t.release(iter)
                    priority_q.append(t)
            priority_q.sort()
            if curr_task == None and len(priority_q):
                curr_task = priority_q.pop(0)
                continue
            if len(priority_q) and priority_q[0] < curr_task:
                # Preempt
                preemtions+=1
                priority_q.append(curr_task)
                curr_task = priority_q.pop(0)
                priority_q.sort()
            print(f"Iter: {it} Task: {'None' if not curr_task else curr_task.period}")
        
        return preemtions