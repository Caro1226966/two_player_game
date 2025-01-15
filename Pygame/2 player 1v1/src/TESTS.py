class A:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):
        return self.x + other.x

    def __mul__(self, other):
        return self.x * other.x

    def __len__(self):
        return 200


temp1 = A(5)
temp2 = A(7)

print(temp1 + temp2)
