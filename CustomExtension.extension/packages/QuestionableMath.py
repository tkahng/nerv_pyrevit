def FeettoInch(number):
    feet = int(number)
    inch = int((number - feet) * 12)

    result = str(feet) + '\' ' + str(inch) + '\"'
    return result

def FeettoInchNotRounded(number):
    feet = int(number)
    inch = (number - feet) * 12

    result = str(feet) + '\' ' + str(inch) + '\"'
    return result