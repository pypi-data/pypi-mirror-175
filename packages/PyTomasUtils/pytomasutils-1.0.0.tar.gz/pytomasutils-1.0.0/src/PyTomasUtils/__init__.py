def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False

def isstring(x):
    try:
        str(x)
        return True
    except:
        return False

def isint(x):
    try:
        int(x)
        return True
    except:
        return False

def radice(x):
    return x**.5