class Pixel:

    def __init__(self, xpos, ypos, brightness):
        self.__xpos = xpos
        self.__ypos = ypos
        self.__brightness = brightness
        self.__brightnessGroup = chr(0)
        self.__maskGroup = chr(0)
    
    def getXPos(self):
        return self.__xpos

    def getYPos(self):
        return self.__ypos

    def getBrightness(self):
        return self.__brightness
    
    def setBrightness(self, brightness):
        self.__brightness = brightness
    
    def getBrightnessGroup(self):
        return self.__brightnessGroup
    
    def setBrightnessGroup(self, brightnessGroup):
        self.__brightnessGroup = brightnessGroup
    
    def getMaskGroup(self):
        return self.__maskGroup
    
    def setMaskGroup(self, maskGroup):
        self.__maskGroup = maskGroup