class ResponseTimeError(Exception):
    def __init__(self, message, response_time, url):
        super().__init__(message)
        self.response_time = response_time
        self.url = url

    def __str__(self):
        return f"{self.args[0]} (URL: {self.url}, Время отклика: {self.response_time:.2f} секунд)"