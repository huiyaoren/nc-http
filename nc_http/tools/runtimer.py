class RunTimer:
    """
    运行计时器
    :example:
        >>> RunTimer.set_point()
        >>> for i in range(1000):
        >>>     print(i)
        >>> RunTimer.set_point()
        >>> RunTimer.check()
    """
    time = None
    profile = []

    @classmethod
    def set_point(cls):
        import time
        time = time.time()
        if cls.time:
            cls.profile.append(time - cls.time)
        cls.time = time

    @classmethod
    def check(cls):
        print(cls.profile)
        cls.time = None
        profile = cls.profile.copy()
        cls.profile = []
        return profile
