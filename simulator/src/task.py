class Task:
    def __init__(self, period, exec_time, deadline=None):
        self.period = period
        self.exec_time = exec_time
        self.deadline = deadline if deadline else period
        assert(self.deadline <= self.period, "Deadline can't be more than period")
        self.next_release = 0
        self.exec_remain = 0
        self.next_deadline = 0

    def release(self, t):
        self.exec_remain = self.exec_time
        self.next_release = t+self.period
        self.next_deadline = t+self.deadline

    def __lt__(self, other):
        return self.next_deadline < other.next_deadline
