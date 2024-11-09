
def convertDatetimeToString(o):
    DATE_FORMAT = "%d-%m-%Y"
    TIME_FORMAT = "%H:%M:%S"
    return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
