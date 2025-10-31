class Task:
    def __init__(self, period, exec_time, deadline=None):
        self.period = period
        self.exec_time = exec_time
        self.deadline = deadline if deadline else period
        assert(self.deadline <= self.period, "Deadline can't be more than period")
        assert(self.deadline>self.exec_time, "Deadline can't be less than execution time")
        assert(self.period>0 and self.exec_time>0 and self.deadline>0, "Values can't be 0")
        self.next_release = 0

    def release(self, t):
        self.next_release += self.period
        return Job(self.exec_time, t+self.deadline)
    
    def __repr__(self):
        return f"<Period: {self.period}, Execution time: {self.exec_time}, Deadline: {self.deadline}>"

    

class Job:
    def __init__(self, exec_time, deadline):
        self.exec_remain = exec_time
        self.deadline = deadline

    def __lt__(self, other):
        return self.deadline < other.deadline
    
    def __repr__(self):
        return f"<Deadline: {self.deadline}, Execution: {self.exec_remain}>"