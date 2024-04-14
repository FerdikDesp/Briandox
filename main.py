from PIL import Image
import ImageEditor
import TextEditor
import random
import plot

src = "nature.jpg"
encodedSRC = "encoded.png"
text = "textABCDE"
limitBrightDiff = 0.05

mask = list('AB'*32)
random.shuffle(mask)

image = Image.open(src)
seed = ImageEditor.encode(image, text, limitBrightDiff, mask, encodedSRC)
binaryDecodedText = ImageEditor.decode(image, seed, limitBrightDiff, mask)

binaryEncodedText = TextEditor.toBinary(text)
print(binaryEncodedText)
print(binaryDecodedText)
print("Процент ошибок: " + str(sum(0 if binaryEncodedText[i] == binaryDecodedText[i] else 1 for i in range(len(binaryDecodedText))) * 100 / len(binaryDecodedText)) + "%")

masks, errors = plot.errorsByMask(text, src, encodedSRC, limitBrightDiff)
plot.createByMask(masks, errors)
"""
brightDiffs, errors = plot.errorsByBrightDiff(text, src, encodedSRC, mask)
plot.createByBrightDiff(brightDiffs, errors)
"""