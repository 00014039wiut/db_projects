class ResponseData:
    def __init__(self,
                 data,
                 status_code=200,
                 success=True):
        self.data = data
        self.status_code = status_code
        self.success = success

    def __str__(self):
        if self.success:
            return f" {self.data} at {self.status_code}"


class BadRequest:
    def __init__(self, data, status_code=400):
        self.data = data
        self.status_code = status_code

    def __str__(self):
        return f" {self.data} at {self.status_code}"
