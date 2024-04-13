def toBinary(text):
    binarytext = ""
    for symbol in text:
        binarytext = binarytext + format(ord(symbol), "08b")
    return binarytext

def toString(binarytext):
    text = ""
    for byte in range(0, len(binarytext), 8):
        text = text + chr(int(binarytext[byte:byte+8], 2))
    return text