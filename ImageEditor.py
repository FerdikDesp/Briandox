from pixel import Pixel
import TextEditor
from PIL import Image
import math

def getBlocks(image, textLength):
    imageMap = image.load()

    blocks = []
    row, column = 0, 0
    for currentSymbol in range(textLength):
        block = []

        if (column + 8 < image.size[1]):
            column += 8
        else:
            row += 8
            column = 8

        for i in range(row, row + 8):
            for j in range(column - 8, column):
                brightness = 0.299 * imageMap[i, j][0] + 0.587 * imageMap[i, j][1] + 0.114 * imageMap[i, j][2]
                block.append(Pixel(i, j, brightness))
        blocks.append(block)
    return blocks

def maskBlock(block, mask):
    for index in range(len(block)):
        if (mask[index] == "A"):
            block[index].setMaskGroup("A")
        else:
            block[index].setMaskGroup("B")
    return block

def sortBlock(block):
    sortedBlock = sorted(block, key = lambda pixel: pixel.getBrightness())
    return sortedBlock

def groupBlock(block, limitBrightDiff):
    maxBrightDiff, maxBrightDiffIndex = 0, 0
    for index in range(len(block) - 1):
        brightDiff = block[index + 1].getBrightness() - block[index].getBrightness()
        if (maxBrightDiff > brightDiff):
            maxBrightDiff = brightDiff
            maxBrightDiffIndex = index
    if (maxBrightDiff <= limitBrightDiff):
        maxBrightDiffIndex = 31
    for index in range(len(block)):
        if (index <= maxBrightDiffIndex):
            block[index].setBrightnessGroup("1")
        else:
            block[index].setBrightnessGroup("2")
    return block

def getLensAndNs(block):
    lens = [0, 0, 0, 0]
    ns = [0, 0, 0, 0]
    for pixel in block:
        if (pixel.getBrightnessGroup() == "1"):
            if (pixel.getMaskGroup() == "A"):
                lens[0] += pixel.getBrightness()
                ns[0] += 1
            else:
                lens[1] += pixel.getBrightness()
                ns[1] += 1
        else:
            if (pixel.getMaskGroup() == "A"):
                lens[2] += pixel.getBrightness()
                ns[2] += 1
            else:
                lens[3] += pixel.getBrightness()
                ns[3] += 1
    return lens, ns

def encode(image, text, limitBrightDiff, mask, encodedSRC):
    binaryText = TextEditor.toBinary(text)
    blocks = getBlocks(image, len(binaryText))
    pixelMap = image.load()
    for index in range(len(blocks)):
        symbol = binaryText[index]
        block = blocks[index]
        maskedBlock = maskBlock(block, mask)
        sortedBlock = sortBlock(maskedBlock)
        groupedBlock = groupBlock(sortedBlock, limitBrightDiff)


        for pixel in groupedBlock:
            print(pixel.getXPos(), pixel.getYPos(), pixel.getBrightness(), pixel.getBrightnessGroup(), pixel.getMaskGroup())

        
        # ENCODE

        lens, ns = getLensAndNs(groupedBlock)
        l1 = (lens[0] + lens[1]) / (ns[0] + ns[1])
        l2 = (lens[2] + lens[3]) / (ns[2] + ns[3])
        if (symbol == "1"):
            if (ns[0] != 0 and ns[1] != 0):
                len1A = lens[0] / ns[0]
                len1B = lens[1] / ns[1]
                print(len1A, len1B)
                if (len1A < len1B):
                    deltaL = len1B - len1A
                    print(ns[0], ns[1], l1, deltaL)
                    newlen1A = ((ns[0] + ns[1]) * l1 + ns[1] * deltaL) / (ns[0] + ns[1])
                    newlen1B = ((ns[0] + ns[1]) * l1 - ns[0] * deltaL) / (ns[0] + ns[1])
                    print(newlen1A, newlen1B)
                    for pixel in groupedBlock:
                        if (pixel.getBrightnessGroup() == "1"):
                            if (pixel.getMaskGroup() == "A"):
                                diff = newlen1A - pixel.getBrightness()
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r + diff), int(g + diff), int(b + diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
                            else:
                                diff = pixel.getBrightness() - newlen1B
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r - diff), int(g - diff), int(b - diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
            if (ns[2] != 0 and ns[3] != 0):
                len2A = lens[2] / ns[2]
                len2B = lens[3] / ns[3]
                print(len2A, len2B)
                if (len2A < len2B):
                    deltaL = len2B - len2A
                    print(ns[2], ns[3], l2, deltaL)
                    newlen2A = ((ns[2] + ns[3]) * l2 + ns[3] * deltaL) / (ns[2] + ns[3])
                    newlen2B = ((ns[2] + ns[3]) * l2 - ns[2] * deltaL) / (ns[2] + ns[3])
                    print(newlen2A, newlen2B)
                    for pixel in groupedBlock:
                        if (pixel.getBrightnessGroup() == "2"):
                            if (pixel.getMaskGroup() == "A"):
                                diff = newlen2A - pixel.getBrightness()
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r + diff), int(g + diff), int(b + diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
                            else:
                                diff = pixel.getBrightness() - newlen2B
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r - diff), int(g - diff), int(b - diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
        else:
            if (ns[0] != 0 and ns[1] != 0):
                len1A = lens[0] / ns[0]
                len1B = lens[1] / ns[1]
                print(len1A, len1B)
                if (len1A > len1B):
                    deltaL = len1A - len1B
                    print(ns[0], ns[1], l1, deltaL)
                    newlen1A = ((ns[0] + ns[1]) * l1 - ns[1] * deltaL) / (ns[0] + ns[1])
                    newlen1B = ((ns[0] + ns[1]) * l1 + ns[0] * deltaL) / (ns[0] + ns[1])
                    print(newlen1A, newlen1B)
                    for pixel in groupedBlock:
                        if (pixel.getBrightnessGroup() == "1"):
                            if (pixel.getMaskGroup() == "A"):
                                diff = pixel.getBrightness() - newlen1A
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r - diff), int(g - diff), int(b - diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
                            else:
                                diff = newlen1B - pixel.getBrightness()
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r - diff), int(g - diff), int(b - diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
            if (ns[2] != 0 and ns[3] != 0):
                len2A = lens[2] / ns[2]
                len2B = lens[3] / ns[3]
                print(len2A, len2B)
                if (len2A > len2B):
                    deltaL = len2A - len2B
                    print(ns[2], ns[3], l2, deltaL)
                    newlen2A = ((ns[2] + ns[3]) * l2 - ns[3] * deltaL) / (ns[2] + ns[3])
                    newlen2B = ((ns[2] + ns[3]) * l2 + ns[2] * deltaL) / (ns[2] + ns[3])
                    print(newlen2A, newlen2B)
                    for pixel in groupedBlock:
                        if (pixel.getBrightnessGroup() == "2"):
                            if (pixel.getMaskGroup() == "A"):
                                diff = pixel.getBrightness() - newlen2A
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r - diff), int(g - diff), int(b - diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
                            else:
                                diff = newlen2B - pixel.getBrightness()
                                r, g, b = pixelMap[pixel.getXPos(), pixel.getYPos()]
                                r, g, b = int(r + diff), int(g + diff), int(b + diff)
                                pixelMap[pixel.getXPos(), pixel.getYPos()] = (r, g, b)
    
    image.save(encodedSRC)
    return len(binaryText)

def decode(image, seed, limitBrightDiff, mask):
    blocks = getBlocks(image, seed)
    pixelMap = image.load()
    binaryText = ""
    for index in range(len(blocks)):
        block = blocks[index]
        maskedBlock = maskBlock(block, mask)
        sortedBlock = sortBlock(maskedBlock)
        groupedBlock = groupBlock(sortedBlock, limitBrightDiff)

        """
        for pixel in groupedBlock:
            print(pixel.getXPos(), pixel.getYPos(), pixel.getBrightness(), pixel.getBrightnessGroup(), pixel.getMaskGroup())
        """
        
        # DECODE

        lens, ns = getLensAndNs(groupedBlock)
        if (ns[0] == 0 and ns[1] == 0):
            len2A = lens[2] / ns[2]
            len2B = lens[3] / ns[3]
            if (len2A > len2B):
                binaryText += "1"
            else:
                binaryText += "0"
        elif (ns[2] == 0 and ns[3] == 0):
            len1A = lens[0] / ns[0]
            len1B = lens[1] / ns[1]
            if (len1A > len1B):
                binaryText += "1"
            else:
                binaryText += "0"
        else:
            len1A = lens[0] / ns[0]
            len1B = lens[1] / ns[1]
            len2A = lens[2] / ns[2]
            len2B = lens[3] / ns[3]
            if (len1A > len1B and len2A > len2B):
                binaryText += "1"
            elif (len1A < len1B and len2A < len2B):
                binaryText += "0"
            else:
                if ((ns[0] + ns[1]) * (len1A - len1B) + (ns[2] + ns[3]) * (len2A - len2B) > 0):
                    binaryText += "1"
                else:
                    binaryText += "0"
    
    return binaryText