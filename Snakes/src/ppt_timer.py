from threading import Timer, Thread, Event


class PerpetualTimer:

    # def __init__(self, t, h_func):
    #     self.t = t
    #     self.hFunction = h_func
    #     self.thread = Timer(self.t, self.handle_function)
    #
    # def handle_function(self):
    #     self.hFunction()
    #     self.thread = Timer(self.t, self.handle_function)
    #     self.thread.start()
    #
    # def start(self):
    #     self.thread.start()
    #
    # def cancel(self):
    #     self.thread.cancel()
    #
    # def callback(self):
    #     self.handle_function(*self.args, **self.kwargs)
    #     self.start()
    def __init__(self, interval, f, *args, **kwargs):
        self.interval = interval
        self.f = f
        self.args = args
        self.kwargs = kwargs

        self.timer = None

    def callback(self):
        self.f(*self.args, **self.kwargs)
        self.start()

    def cancel(self):
        self.timer.cancel()

    def start(self):
        self.timer = Timer(self.interval, self.callback)
        self.timer.start()