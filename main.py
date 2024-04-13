from PIL import Image
import ImageEditor
import TextEditor
import random

src = "nature.jpg"
encodedSRC = "encoded.png"
text = "textABCDE"
limitBrightDiff = 0.2

mask = list('AB'*32)
random.shuffle(mask)

image = Image.open(src)
seed = ImageEditor.encode(image, text, limitBrightDiff, mask, encodedSRC)
binaryDecodedText = ImageEditor.decode(image, seed, limitBrightDiff, mask)

binaryEncodedText = TextEditor.toBinary(text)
print(binaryEncodedText)
print(binaryDecodedText)
print("Процент ошибок: " + str(sum(0 if binaryEncodedText[i] == binaryDecodedText[i] else 1 for i in range(len(binaryDecodedText))) * 100 / len(binaryDecodedText)) + "%")