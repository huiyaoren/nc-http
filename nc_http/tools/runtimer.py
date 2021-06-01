class RunTimer:
    """
    运行计时器
    :example:
        >>> timer = RunTimer()
        >>> timer.set_point()
        >>> time.sleep(1)
        >>> time_cost = timer.check_one()
        >>> print(time_cost)
        or
        >>> timer = RunTimer()
        >>> timer.set_point()
        >>> time.sleep(1)
        >>> timer.set_point()
        >>> time.sleep(2)
        >>> time_cost = timer.check()
        >>> print(time_cost)
    """
    time = None
    profile = []

    def set_point(self):
        import time
        time = time.time()
        if self.time:
            self.profile.append(time - self.time)
        self.time = time

    def check(self):
        self.set_point()
        self.time = None
        profile = self.profile.copy()
        self.profile = []
        return profile

    def check_one(self):
        profile = self.check()
        return profile[0]
