import ImageEditor
import TextEditor
import random
from PIL import Image

def errorsByMask(encodedText, imageSRC, encodedSRC, limitBrightDiff):
    masks, errors = [], []

    for i in range(10):
        mask = list('AB'*32)
        random.shuffle(mask)
        masks.append(i)

        image = Image.open(imageSRC)
        seed = ImageEditor.encode(image, encodedText, limitBrightDiff, mask, encodedSRC)
        binaryDecodedText = ImageEditor.decode(image, seed, limitBrightDiff, mask)
        binaryEncodedText = TextEditor.toBinary(encodedText)
        
        error = 0

        for j in range(len(binaryDecodedText)):
            if (binaryDecodedText[j] != binaryEncodedText[j]):
                error += 1
        
        error *= 100
        error /= len(binaryEncodedText)

        errors.append(error)
    
    return masks, errors

def errorsByBrightDiff(encodedText, imageSRC, encodedSRC, mask):
    brightDiffs, errors = [], []

    for brightDiff in range(0, 50, 5):
        brightDiffs.append(brightDiff / 100)

        image = Image.open(imageSRC)
        seed = ImageEditor.encode(image, encodedText, brightDiff, mask, encodedSRC)
        binaryDecodedText = ImageEditor.decode(image, seed, brightDiff, mask)
        binaryEncodedText = TextEditor.toBinary(encodedText)
        
        error = 0

        for j in range(len(binaryDecodedText)):
            if (binaryDecodedText[j] != binaryEncodedText[j]):
                error += 1
        
        error *= 100
        error /= len(binaryEncodedText)

        errors.append(error)
    
    return brightDiffs, errors

def createByMask(masks, errors):
    import matplotlib.pyplot as plt

    plt.plot(masks, errors)
    plt.title("Зависимость % ошибок от маски")
    plt.xlabel("Маска")
    plt.ylabel("% ошибок")
    plt.show()

def createByBrightDiff(brightDiffs, errors):
    import matplotlib.pyplot as plt

    plt.plot(brightDiffs, errors)
    plt.title("Зависимость % ошибок от порога изменения яркости")
    plt.xlabel("Порог изменения яркости")
    plt.ylabel("% ошибок")
    plt.show()