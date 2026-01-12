import math

def ptb2(a, b, c):
    delta = b*b - 4*a*c
    if (delta > 0):
        x1 = (-b - math.sqrt(delta)/(2*a))
        x2 = (-b + math.sqrt(delta)/(2*a))
        return x1, x2
    else:
        if (delta == 0):
            x = -b/(2*a)
            return x
        else:
            return 'false'
