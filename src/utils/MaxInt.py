class MaxInt:

    def __init__(self, string):
        pass
        self._value = int(string)
        if len(string) > 5:
            self._value = 99999

    def get_value(self):
        return self._value