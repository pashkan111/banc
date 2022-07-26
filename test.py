class A:
    w = int
    def __init__(self, w: int):
        self.w = w
    
    @classmethod
    def get_w(cls):
        return cls.w
    
    
print(A(4).get_w())