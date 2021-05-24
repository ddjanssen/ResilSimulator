class Link:
    def __init__(self,device1,device2):
        self.device1 = device1
        self.device2 = device2
        pass

    def __str__(self):
        return "Link between {} and {}".format(self.device1,self.device2)