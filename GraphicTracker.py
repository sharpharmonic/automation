#------------------------------------------------------------------------
# Name: GraphicTracker.py
# Purpose: Analyze transport stream crawl and fade using tesseractOCR                       
# Author: William Gunnells                    
# Created: 7/21/2015             
# Copyright: (c) Harmonic 2015              
# License: GNU               
# Comment: https://code.google.com/p/tesseract-ocr/ 
# Dependencies: GraphicAnalyzer.py
#------------------------------------------------------------------------                          

#===== Import Statements================
from GraphicAnalyzer import *
import HATSLogger
from InfoFromPngFile import InfoFromPngFile
# --------------------------------------------------------------------
#  Globals
# --------------------------------------------------------------------



def Track():
    HATSLogger.LoggerFactory.putHatsLoggerKeyword('$TESTCASE', 'TestCase')    
    configData={'TestInformation':{'TestName':'Graphic Analyzer Crawl Test'}}
    logger = HATSLogger.LoggerFactory("$HATS_LOGGER_PATH/config/Testcaselog.yml").getLogger()  
       
    try:
        print os.getcwd()
        os.chdir("C:\HATSFramework\HATS\Testcases\GenericTemplate\ElectraXDeviceTest\TestCases\UMP\GraphicOverlay")
        print os.getcwd()
    except:
        print "====path issue?"
    try: 
        v=verifycsv('c:\TestSetup\crawl.csv',1)
        if v == None:
            logger.hats_log(HATSLogger.FAIL, "verifycsv() CSV file", "Configuration settings tsfile,startframe,noOframes, etc...", "input problem")
            print "====csv file issue"
        else:
            logger.hats_log(HATSLogger.PASS, "verifycsv() CSV file", "Configuration settings tsfile,startframe,noOframes, etc...", v)
                
    except:
        print "====csv file issue"
    try:
        #ConvertTsToPNG(v['video'], v['startingFrame'], v['noOfFrames'], isInterace=False) 
        ConvertTsToPNG(v['video'], 1800, 100, isInterace=False) # 2200 csv should be 1700 at 3000 iterations
        logger.hats_log(HATSLogger.PASS, "ConverTsToPNG() convert to PNG files", "ffmpeg decoder split frames to png files...", 'PASS png creation')
    except:
        print "====convert files to png issue"
        logger.hats_log(HATSLogger.FAIL, "ConverTsToPNG() convert to PNG files", "ffmpeg decoder split frames to png files...", 'FAIL png creation')
    try:
        analyzeborder(v['video'],v['left'],v['top'],v['right'],v['bottom']) 
        bdr=" %s, %s,%s, %s," % (v['left'], v['top'], v['right'], v['bottom'])
        logger.hats_log(HATSLogger.PASS, "analyzeborder() function", "Analyze border to crop images", bdr )
    except:
        print "====analyze border issue check cropped image directory"
        logger.hats_log(HATSLogger.FAIL, "analyzerborder() function", "Analyze border to crop images", 'border issue' )
    
    try:    
        dat=analyzecrawl(v['video'],v['searchstring']) 
        print "check length"
        print len(dat)
        if len(dat)==0:
            issue="did not find string values:%d" % len(dat)
            logger.hats_log(HATSLogger.FAIL, "analyzecrawl() function", "Tesseract OCR function", issue )
        else:
            logger.hats_log(HATSLogger.PASS, "analyzecrawl() function", "Tesseract OCR function", dat.values()[0:5] )
        
    except:
        print "====search string analyzecrawl error: could be a path issue"
    
    try:
        print dat
        print dat.keys()[0]
        print os.getcwd()
        print v
    except:
        print "====several print strings:"
    try:
        keylist=dat.keys()
        keylist.sort()
        print keylist[1]
        print "printing keylist"
        #TempImg(v['video'],dat.keys()[0]) #
        dat.keys()[0] #first element in dictionary
        TempImg(v['video'],keylist[1]) # dat.keys()[0] first element in dictionary
        logger.hats_log(HATSLogger.PASS, "TempImg() function", "Create Template Image algorithm", dat.keys()[0] )
    except:
        print "====create temp image error: could be a path"
        logger.hats_log(HATSLogger.FAIL, "TempImg() function", "Create Template Image algorithm", 'temp image issue' )
    #TempImg('cap_25001.ts',dat.keys()[0]) # dat.keys()[0] first element in dictionary
    try:
        #track=TrackTextCrawl(v['video'],dat.keys()[0]) # this took cropped0091.png sort dictionary then track
        track=TrackTextCrawl(v['video'],keylist[1]) # this took cropped0091.png sort dictionary then track
        t=1000000
        for i in track:
            print t
            if i < t:
                print "Tracking good"
            else:
                print "Tracking false look at template.png in current working directory."
            t=i
            print t
        logger.hats_log(HATSLogger.PASS, "TempTextCrawl() function", "Track crawl text on X-axis ", track )
    except: #Exception, err:
        #sys.stderr.write(str(err))
        print "====track the text crawl: issue could be path related"
        logger.hats_log(HATSLogger.FAIL, "TempTextCrawl() function", "Track crawl text on X-axis ", 'track X issue' )
    try:
        print "===================reporting ================="
        print "Pass: %s" % str(keylist[1])
       
    except:
        print "====reporting error: ? "
        
    try:
        ###################Robert code
        EXPECTED_COLOR = "green"
        pathToPngFiles = v['video'] + '_img'
        pngFileName = dat.keys()[0]
        graphicPosition = "0x0"
        graphicSize = str(v['right'] - v['left'] -1) + 'x' + str(v['bottom'] - v['top'] -1)
    
        pngInfo = InfoFromPngFile(pathToPngFiles)
        backGroundColor = pngInfo.determineBackGroundColor(pngFileName, graphicPosition, graphicSize)
        print("Background color of banner in %s: %s\n" % (pngFileName, backGroundColor))
    
        if (backGroundColor == EXPECTED_COLOR):
            stepStatus = HATSLogger.PASS
        else:
            stepStatus = HATSLogger.FAIL
    
        logger.hats_log(stepStatus, "Background color of banner in %s " % (pngFileName), 
                EXPECTED_COLOR, backGroundColor)

    except: 
        print "Roberts Image color picker error:"
        
        
        #logger.sendMailSimple(configData['TestInformation']['TestName'], 'william.gunnells@harmonicinc.com')
    
    logger.sendMailSimple(configData['TestInformation']['TestName'], 'william.gunnells@harmonicinc.com')
    
if __name__=="__main__":
    Track()
    
    
