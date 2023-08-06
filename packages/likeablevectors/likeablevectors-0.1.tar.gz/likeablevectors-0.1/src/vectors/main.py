class Vector: # Create dummy class with necessary class variables to have correct code highlighting/coloring in actual class definition
    def __init__(self):
        self.pos = []
        self.dimensions = 0

class Vector:
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == list: # If a list containing a list of coordinates is submitted, get the coordinates from that list.
            self.pos = args[0]
        else:
            self.pos = args
        self.dimensions = len(self.pos)

    # Its assumed for r to be a Vector class too to have correct code highlighting/coloring, a case for "type(r) == int" is defined though
    def __add__(self, r : Vector):
        result = None
        if type(r) == int:
            result = Vector([self.pos[i]+r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.pos[i]+r.pos[i] for i in range(self.dimensions)])
        return result
    
    def __sub__(self, r : Vector):
        result = None
        if type(r) == int:
            result = Vector([self.pos[i]-r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.pos[i]-r.pos[i] for i in range(self.dimensions)])
        return result
    
    def __mul__(self, r : Vector):
        result = None
        if type(r) == int:
            result = Vector([self.pos[i]*r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.pos[i]*r.pos[i] for i in range(self.dimensions)])
        return result
    
    def __truediv__(self, r : Vector):
        result = None
        if type(r) == int:
            result = Vector([self.pos[i]/r for i in range(self.dimensions)])
        elif type(r) == Vector:
            if self.dimensions != r.dimensions:
                raise ValueError("Vector dimensions do not match.")
            result = Vector([self.pos[i]/r.pos[i] for i in range(self.dimensions)])
        return result


def dotProduct(v1 : Vector, v2 : Vector):
    if v1.dimensions != v2.dimensions:
        raise ValueError("Vector Dimensions do not match.")
    return sum([v1.pos[i]*v2.pos[i] for i in range(v1.dimensions)])


if __name__ == "__main__":
    x = Vector(2, 3, 4)
    y = Vector(1, 2, 6)
    print(dotProduct(x, y))