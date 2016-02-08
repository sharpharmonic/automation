'''
Created on Jul 29, 2015

@author: rcorrell
'''

import Image



class InfoFromPngFile():
    ''' Defines functions used for getting information from a PNG file

    Usage: 
        pngInfo = InfoFromPngFile(<path To PNG Files>)  # for example:  C:\myTemp

        # see graphicPosition and graphicSize comments under __init__ 
        backGroundColor = pngInfo.determineBackGroundColor(<PNG filename>, 
                                                           <graphic position>, 
                                                           <graphic size>)
        print("Background color of banner: %s \n" % backGroundColor) 
    '''

    def __init__(self, pathToPngFiles):
        '''
        Constructor
        '''
        self.pathToPngFiles = pathToPngFiles
        self.pngFileName = None

        # Two input values.
        self.graphicPosition = None     # leftmostPostion + "x" + topmostPosition"
        self.graphicSize = None         # textBoxWidth + "x" + textBoxHeight

        # Four values parsed from input values.
        self.leftmostPostion = None
        self.topmostPosition = None
        self.textBoxWidth = None        # rightmostPosition - leftmostPostion
        self.textBoxHeight = None       # bottommostPosition - topmostPosition

        # Two derived values
        self.bottommostPosition = None  # topmostPosition + textBoxHeight
        self.rightmostPosition = None   # leftmostPostion + textBoxWidth

        self.textBoxPixelCount = 0
        self.blackColorCount = 0
        self.whiteColorCount = 0
        self.greenColorCount = 0
        self.unexpectedColorCount = 0

        '''
        # Example of actual banner (rolling text box) measurements from "0794.png"
        self.graphicSize = "351x351"        # textBoxWidth + "x" + textBoxHeight
        self.graphicPosition = "64x524"     # leftmostPostion + "x" + topmostPosition"
        self.leftmostPostion = 64
        self.topmostPosition = 524
        self.textBoxWidth = 351             # rightmostPosition - leftmostPostion
        self.textBoxHeight = 351            # bottommostPosition - topmostPosition
        self.bottommostPosition = 875       # topmostPosition + textBoxHeight
        self.rightmostPosition = 415        # leftmostPostion + textBoxWidth
        '''

    def setPngFileName(self, thePngFileName):
        ''' sets self.pngFileName to value of thePngFileName parameter

        :Parameters: thePngFileName is a string value for the name of the PNG file.

        :Return: Nothing

        :Exceptions: NA
        ''' 
        self.pngFileName = thePngFileName

    def deriveTopLeftRightBottomOfBanner(self, theGraphicPosition, theGraphicSize):
        ''' Derives the border of the banner and sets six related attributes

        :Parameters: 
        theGraphicPosition is a string value of leftmostPostion + "x" + topmostPosition.
        theGraphicSize is a string value of textBoxWidth + "x" + textBoxHeight

        :Return: Nothing

        :Exceptions: NA
        ''' 
        # leftmostPostion + "x" + topmostPosition"
        self.graphicPosition = theGraphicPosition

        # textBoxWidth + "x" + textBoxHeight
        self.graphicSize = theGraphicSize

        leftValue, rightValue = list(self.graphicPosition.split("x"))
        self.leftmostPostion = int(leftValue)
        self.topmostPosition = int(rightValue)

        leftValue, rightValue = list(self.graphicSize.split("x"))
        self.textBoxWidth = int(leftValue)
        self.textBoxHeight = int(rightValue)

        self.rightmostPosition = self.leftmostPostion + self.textBoxWidth
        self.bottommostPosition = self.topmostPosition + self.textBoxHeight

    def checkPixelColor(self, expectedColor, actualColor, colorTolerance=3):
        ''' Determines whether expected color matches actualColor within colorTolerance

        :Parameters:
        expectedColor is a tuple with three elements representing an expected color
        actualColor is a tuple with three elements representing the actual color
        colorTolerance is an integer for factoring plus or minus variance in actual color

        :Return: True if expectedColor found; otherwise False

        :Exceptions: NA
        ''' 
        NUMBER_OF_ELEMENTS_IN_TUPLE = 3
        result = True
        for i in range(NUMBER_OF_ELEMENTS_IN_TUPLE):
            x = expectedColor[i]
            y = actualColor[i]
            z = x - colorTolerance
            if z < 0:
                z = 0
            if (y < z) or y > (x + colorTolerance):
                return False
        return result

    def calculateMaxColorCount(self):
        ''' Determines max color count among three colors and one unexpected color counter.  

        Relies on attributes.  Assumes background color count is higher than all other 
        color counts, including the possibility of a high unexpected color count n, where 
        n is the total count of all unexpected colors.

        :Parameters: NA

        :Return: A string representing the max color

        :Exceptions: NA
        ''' 
        backgroundColor = None
        if self.greenColorCount > self.blackColorCount \
                and self.greenColorCount > self.whiteColorCount:
            backgroundColor = "green" 
        elif self.blackColorCount > self.whiteColorCount:
            backgroundColor = "black"
        else:
            backgroundColor = "white"

        if self.unexpectedColorCount > \
                max(self.greenColorCount, self.blackColorCount, self.whiteColorCount):
            backgroundColor = "not black, white, or green"

        return backgroundColor

    def traverseTextBox(self):
        ''' Traverses text box.  Relies on global attributes

        :Parameters: NA

        :Return: True if expectedColor found; otherwise False

        :Exceptions: Using Exception to catch a wide range of possible exceptions
        ''' 
        COLOR_TOLERANCE = 5  # Used in factoring plus or minus variance in expected color tuple values
        #BLACK = (0, 0, 0)
        BLACK = (47, 62, 50)  # for black text on green background
        WHITE = (250, 250, 250)
        GREEN = (16, 255, 5)
        try:
            pngFile = "%s\%s" % (self.pathToPngFiles, self.pngFileName)
            print("PNG file: " + pngFile)
            im = Image.open(pngFile)
            #print im.format, im.size, im.mode
            #print im.getbbox()  # (0, 0, 1920, 1080)
            pix = im.load()
            self.textBoxPixelCount = 0
            self.blackColorCount = 0
            self.whiteColorCount = 0
            self.greenColorCount = 0
            self.unexpectedColorCount = 0

            # Determine background color based on highest color count
            for y in range(self.topmostPosition, self.bottommostPosition + 1):
                for x in range(self.leftmostPostion, self.rightmostPosition + 1):
                    self.textBoxPixelCount += 1
                    actualColor = pix[x, y]
                    found = self.checkPixelColor(BLACK, actualColor, COLOR_TOLERANCE)
                    if (found):
                        self.blackColorCount += 1
                        continue
                    found = self.checkPixelColor(WHITE, actualColor, COLOR_TOLERANCE)
                    if (found):
                        self.whiteColorCount += 1
                        continue
                    found = self.checkPixelColor(GREEN, actualColor, COLOR_TOLERANCE)
                    if (found):
                        self.greenColorCount += 1
                    else:
                        self.unexpectedColorCount += 1
                        #print("Unexpected color at " + str(x) + ", " + str(y) + ":")
                        #print(actualColor)

            # These five print statements are optional
            print ("Pixel Count: " + str(self.textBoxPixelCount))
            print ("Black Color Count: " + str(self.blackColorCount))
            print ("White Color Count: " + str(self.whiteColorCount))
            print ("Green Color Count: " + str(self.greenColorCount))
            print ("Unexpected Color Count: " + str(self.unexpectedColorCount))

            return self.calculateMaxColorCount()

        except Exception, e:
            print("got exception: " + str(e))    

    def probeGraphicSize(self):
        ''' Temporary function for local modification while probing position and size

        :Parameters: NA

        :Return: Nothing

        :Exceptions: Exception
        '''    
        try:
            pngFile = "%s\\%s" % (self.pathToPngFiles, self.pngFileName)
            print(pngFile)
            im = Image.open(pngFile)
            print im.format, im.size, im.mode
            print im.getbbox()  # output example: (0, 0, 1920, 1080)

            print("Inside border, expecting white (250,250, 250)")
            print im.getpixel((64, 524))   # width, height of topmostPosition
            print im.getpixel((415, 524))  # width, height of rightmostPosition
            print im.getpixel((64, 875))   # width, height of leftmostPostion
            print im.getpixel((415, 875))  # width, height of bottommostPosition

            print("Outside border, expecting black: (0, 0, 0)")
            print im.getpixel((63, 523))   # width, height   # topmostPosition 
            print im.getpixel((416, 523))  # width, height   # rightmostPosition
            print im.getpixel((63, 876))   # width, height   # leftmostPostion 
            print im.getpixel((416, 876))  # width, height   # bottommostPosition

        except Exception, e:
            print("got exception: " + str(e))

    def determineBackGroundColor(self, thePngFileName, theGraphicPosition, theGraphicSize):
        ''' Determines the background color of a banner in a PNG file.

        :Parameters: 
        thePngFileName is a string value for the name of the PNG file.
        theGraphicPosition is a string value of leftmostPostion + "x" + topmostPosition.
        theGraphicSize is a string value of textBoxWidth + "x" + textBoxHeight

        :Return: A string representing the background color of banner or None with exception

        :Exceptions: NA
        ''' 
        self.setPngFileName(thePngFileName)
        self.deriveTopLeftRightBottomOfBanner(theGraphicPosition, theGraphicSize)

        return self.traverseTextBox()


if __name__ == "__main__":

    #pngInfo = InfoFromPngFile("c:\myPngFiles")
    '''
    backGroundColor = pngInfo.determineBackGroundColor("0794.png", "64x524", "351x351")
    
    backGroundColor = pngInfo.determineBackGroundColor("0001.png", "1x12", "981x83")

    backGroundColor = pngInfo.determineBackGroundColor("0002.png", "4x18", "981x118")
    '''
    #pngInfo = InfoFromPngFile("C:\HATSFramework\HATS\Scripts\GraphicAnalyzers\cap_25001.ts_img")
    #backGroundColor = pngInfo.determineBackGroundColor("cropped0029.png", "0x0", "1845x101")

    #print("Background color of banner: %s \n" % backGroundColor)
    
