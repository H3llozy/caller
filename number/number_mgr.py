
class NumberMgr(object):

    def __init__(self):
        self.__index = 0
        self.__numbers = ('+18507903580', '+18507249075')

    def get(self)->str:
        num = self.__numbers[self.__index]
        self.__index += 1
        self.__index = self.__index % len(self.__numbers)

        return num
