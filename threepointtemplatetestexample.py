#===== Import Statements================
import sys
import os
import time
from datetime import datetime
import calendar
#====== HATS Specific ==================
from HATS.Generic.TestCaseExecutor import TestCaseExecutor, TestIteration
from HATS.Devices.Harmonic.ACPXmlControl import ChannelProfileHelper
from HATS.Testcases.GenericTemplate.ElectraXDeviceTest.TestCases.UMP.Util.UmpTestUtil import *
from GraphicAnalyzer import *
from PIL import ImageChops
import HATSLogger

from InfoFromPngFile import InfoFromPngFile
#from PIL import *
'''
QC Path: TBD

1. Check Buffer compliance by M2Demux
2. Check graphic overlay:
   TBD
3. Other compliacne test by TxMould
4. No unexpected alarm
5. No coredump

-f ThreePointTemplateNTSC -e email@harmonicinc.com -I C:\HATSFramework\HATS\Datafiles\Generic\Template\hkqa-automation-ini.yml -M C:\Runlist\testEnvManifest_HKQA.yml.output -C http://hdropbox:8080/binary/HKQA/Automation/NMX_Catalog/HKQAGOLDENCATALOG.hzp
'''

def ExecteTestStep_ThreePointTemplateSampleTest(testCaseExecutor, testIteration, iterParam, **param):
    '''
    |Time        |Event
    |T - x       |Activate service
    |T           |start stream source (1st frame with TC 00:00:00:00)
    |T+15        |Send command to trigger graphic insertion at T+75s
    |T+75        |1. Send command to trigger graphic insertion at T+75s+60s
    |            |2. Graphic should be inserted and the corresponding frame should with TC around 00:01:12:27
    '''
    testData = {}

    utcsecs, utcmsec = UmpTestUtil_ConvertDateTime2SCTE104Epoch(param['StreamTime'])
    utcsecs = utcsecs + 75  # The activation time of graphic is stream time + 75 seconds
    secondInsertTimeSec = utcsecs + 60
    secondInsertTimeMsec = utcmsec
    time.sleep(15)

    # Get DPI PID index
    profile = testIteration.GetChannelProfile(testIteration.Channels[0].Name)
    cHelper = ChannelProfileHelper(profile)
    dataInstance = cHelper.GetMWProfileList()[0].GetData('DPI1')
    dpiPidIndex = int(dataInstance.DpiPidIndex.Value)


    # Send graphic insertion command
    dut = testIteration.HatsSysSetup.setup.encObj
    # Get the hostname of DUT
    ump_id = dut.getHostname()
    # Upload the template to ACP
    templateFullPath = iterParam['GraphicOverlay']['GraphicTemplate']
    dut.uploadFile(templateFullPath, 'graphics')

    dut.clearScteLog()  # Clear all SCTE msg log in ACP
    dut.dummyAS.start(dpiPidIndex, ump_id, cmdLogPath=os.path.join(testIteration.iterationResultPath, 'dummyASCmdLog.txt'))
    dut.dummyAS.insertGraphicTemplate(utcsecs, utcmsec, 1001, os.path.basename(templateFullPath), '00:00:15:00', 5)

    param['AnalyzerList']['ICDCommand'] = {}
    param['AnalyzerList']['ICDCommand']['compareTimeList'] = [{'requestTime': {'utcsecs': utcsecs, 'utcmsec': utcmsec}, 'actualTimeLogInx': 4}]
    return testData


def ExecteTestStep_CrawlTextTemplateTest(testCaseExecutor, testIteration, iterParam, **param):
    '''
    |Time        |Event
    |T - x       |Activate service
    |T           |start stream source (1st frame with TC 00:00:00:00)
    |T+15        |Send command to trigger graphic insertion at T+75s
    |T+75        |1. Send command to trigger graphic insertion at T+75s+60s
    |            |2. Graphic should be inserted and the corresponding frame should with TC around 00:01:12:27 
    '''
    testData = {}

    utcsecs, utcmsec = UmpTestUtil_ConvertDateTime2SCTE104Epoch(param['StreamTime'])
    utcsecs = utcsecs + 75  # The activation time of graphic is stream time + 75 seconds
    secondInsertTimeSec = utcsecs + 60
    secondInsertTimeMsec = utcmsec

    time.sleep(15)

    # Get DPI PID index
    profile = testIteration.GetChannelProfile(testIteration.Channels[0].Name)
    cHelper = ChannelProfileHelper(profile)
    dataInstance = cHelper.GetMWProfileList()[0].GetData('DPI1')
    dpiPidIndex = int(dataInstance.DpiPidIndex.Value)


    # Send graphic insertion command
    dut = testIteration.HatsSysSetup.setup.encObj
    # Get the hostname of DUT
    ump_id = dut.getHostname()
    templateFullPath = iterParam['GraphicOverlay']['GraphicTemplate']
    dut.uploadFile(templateFullPath, 'graphics')
    dut.clearScteLog()  # Clear all SCTE msg log in ACP
    dut.dummyAS.start(dpiPidIndex, ump_id)
    dut.dummyAS.insertGraphicTemplate(utcsecs, utcmsec, 1001, os.path.basename(templateFullPath), '00:00:15:00', 5, 1, 1, "HATS Crawl Text Test")

    param['AnalyzerList']['ICDCommand'] = {}
    param['AnalyzerList']['ICDCommand']['compareTimeList'] = [{'requestTime': {'utcsecs': utcsecs, 'utcmsec': utcmsec}, 'actualTimeLogInx': 4}]

    return testData

def ExecteTestStep_SqueezeBackTemplateTest(testCaseExecutor, testIteration, iterParam, **param):
    '''
    |Time        |Event
    |T - x       |Activate service
    |T           |start stream source (1st frame with TC 00:00:00:00)
    |T+15        |Send command to trigger graphic insertion at T+75s
    |T+75        |1. Send command to trigger graphic insertion at T+75s+60s
    |            |2. Graphic should be inserted and the corresponding frame should with TC around 00:01:12:27
    '''
    testData = {}

    utcsecs, utcmsec = UmpTestUtil_ConvertDateTime2SCTE104Epoch(param['StreamTime'])
    utcsecs = utcsecs + 75  # The activation time of graphic is stream time + 75 seconds

    time.sleep(15)

    # Get DPI PID index
    profile = testIteration.GetChannelProfile(testIteration.Channels[0].Name)
    cHelper = ChannelProfileHelper(profile)
    dataInstance = cHelper.GetMWProfileList()[0].GetData('DPI1')
    dpiPidIndex = int(dataInstance.DpiPidIndex.Value)


    # Send graphic insertion command
    dut = testIteration.HatsSysSetup.setup.encObj
    # Get the hostname of DUT
    ump_id = dut.getHostname()
    templateFullPath = iterParam['GraphicOverlay']['GraphicTemplate']
    dut.uploadFile(templateFullPath, 'graphics')
    dut.clearScteLog()  # Clear all SCTE msg log in ACP
    dut.dummyAS.start(dpiPidIndex, ump_id)
    dut.dummyAS.insertGraphicTemplate(utcsecs, utcmsec, 1001, os.path.basename(templateFullPath), '00:00:15:00', 5, 1, 1, 'Crawl Text Test')

    param['AnalyzerList']['ICDCommand'] = {}
    param['AnalyzerList']['ICDCommand']['compareTimeList'] = [{'requestTime': {'utcsecs': utcsecs, 'utcmsec': utcmsec}, 'actualTimeLogInx': 4}]

    return testData

def ExecteValidation_ThreePointTemplateSampleTest(testCaseExecutor, testIteration, iterParam, **param):
    # Get the output list for the channel to be tested
    OutputFileList, OutputDir = testIteration.GetOutputFileListFromChannel("NTSC_BMW")

    # Extract frames to PNG stack from TS
    for output in OutputFileList:
        for outputToVerify in iterParam['GraphicOverlay']['ValidationList']:
            port = (int)(os.path.splitext(os.path.basename(output))[0].split('_')[1])
            if port == outputToVerify['port']:  # Validate
                UmpTestUtil_ConvertTsToPNG(output, outputToVerify['StartFrame'], outputToVerify['FrameCnt'], isInterace=outputToVerify['interalce'])  # Extract frames at around 00:02:10:00 for 30 sec



def ExecteValidation_CrawlTextTemplateTest(testCaseExecutor, testIteration, iterParam, **param):
    # Get the output list for the channel to be tested
    OutputFileList, OutputDir = testIteration.GetOutputFileListFromChannel("NTSC_BMW")

    # Extract frames to PNG stack from TS
    for output in OutputFileList:
        for outputToVerify in iterParam['GraphicOverlay']['ValidationList']:
            port = (int)(os.path.splitext(os.path.basename(output))[0].split('_')[1])
            if port == outputToVerify['port']:  # Validate
                UmpTestUtil_ConvertTsToPNG(output, outputToVerify['StartFrame'], outputToVerify['FrameCnt'], isInterace=outputToVerify['interalce'])  # Extract frames at around 00:02:10:00 for 30 sec


def ExecteValidation_SqueezeBackTemplateTest(testCaseExecutor, testIteration, iterParam, **param):
    # Get the output list for the channel to be tested
    OutputFileList, OutputDir = testIteration.GetOutputFileListFromChannel("NTSC_BMW")

    # Extract frames to PNG stack from TS
    for output in OutputFileList:
        for outputToVerify in iterParam['GraphicOverlay']['ValidationList']:
            port = (int)(os.path.splitext(os.path.basename(output))[0].split('_')[1])
            if port == outputToVerify['port']:  # Validate
                UmpTestUtil_ConvertTsToPNG(output, outputToVerify['StartFrame'], outputToVerify['FrameCnt'], isInterace=outputToVerify['interalce'])  # Extract frames at around 00:02:10:00 for 30 sec



if __name__ == '__main__':
    
    testName = os.path.basename(sys.argv[0]).replace('.py', '')
    inputyml = sys.argv[-1]
    
     
    with TestCaseExecutor(inputyml, testName, 'ThreePointTemplate') as testCaseExecutor:
        testCaseExecutor.initialize(forceRestoreCatalog=True)
        testSetup = testCaseExecutor.HatsSysSetup.setup
       
        dpis = ['DPI1', 'DPI2', 'DPI3']

        mwDPIBasePath = testSetup.cfgparams['DPI-Base-MW']['Path']
        bcDPIBasePath = testSetup.cfgparams['DPI-Base-BC']['Path']

        mwProfilePath = testSetup.cfgparams['Video-MW-Profile']['Path']

        mwVideoPath = testSetup.cfgparams['Video-MW']['Path']
        bcVideoPath = testSetup.cfgparams['Video-BC']['Path']

        (SOURCE_ID, INPUT_SETTING, SHORT_DESC) = ('SourceID', 'InputSetting', 'ShortDesc')

        iterParams = testSetup.cfgparams['IterationParams']

        iterationCnt = 0

        for iterParam in iterParams:
            with TestIteration(iterParam, testCaseExecutor) as testIteration:
                AnalyzerList = {}
                iterationCnt += 1

                testCaseExecutor.HatsIni.logger.MailLog("Info", "", "", "", "Iteration %s: %s (%s)" % (iterationCnt, testIteration.iterationId, iterParam[SHORT_DESC]))

                testIteration.SetChannelStreamerId('%s_BMW' % testSetup.cfgparams['VideoSystem'], iterParam[SOURCE_ID])
                testIteration.Initialize()

                testIteration.RestoreConfig()
                testIteration.UpdateSourceConfiguration()

                ################################## Add-on Setting ##################################
                updateProps = {
                    'Data': {},
                    'DeleteInputPID': {},
                    'DPI': {},
                    'Video':{},
                    'MWProfile': {}
                }

                # DPI streams that should not be deleted
                usedDpi = []

                # Change the input DPI PID, DPISource and DPIProcessMode
                for streamName, streamProps in iterParam['DPI'].iteritems():
                    updateProps['DPI'][bcDPIBasePath + streamName] = streamProps  # TODO: temp comment out
                    updateProps['DPI'][mwDPIBasePath + streamName] = streamProps
                    usedDpi.append(streamName)

                # Delete all un-used DPI and Data PID
                if 'DeleteUnUsedDPI'  not in iterParam or iterParam['DeleteUnUsedDPI'] is True:
                    for streamName in dpis:
                        if streamName not in usedDpi:  # DPI stream not used, delete them
                            updateProps['DeleteInputPID'][bcDPIBasePath + streamName] = {'StreamType': 'DPI'}
                            updateProps['DeleteInputPID'][mwDPIBasePath + streamName] = {'StreamType': 'DPI'}
                    for streamName in ['D1', 'D2', 'D3']:
                        if streamName not in usedDpi:  # DPI stream not used, delete them
                            updateProps['DeleteInputPID'][bcDPIBasePath + streamName] = {'StreamType': 'DATA'}
                            updateProps['DeleteInputPID'][mwDPIBasePath + streamName] = {'StreamType': 'DATA'}

                # Disable logo insertion for all output
                updateProps['Video'][bcVideoPath] = {'EnableLogoInsertion':False, 'EnableAdvanceGraphics': True}  # TODO: temp comment out
                updateProps['Video'][mwVideoPath] = {'MwEnableLogoInsertion':False, 'EnableAdvanceGraphics': True}

                # Update the output resolution of the lowest bitrate as a workaround for TxMould not being able to detect the logo which
                # is at the boundaries of macroblocks
                largerResDict = {'VideoResolution': '480x360', 'VideoEncodingLevel': 'H.264 3'}
                updateProps['MWProfile'][mwProfilePath] = {'ProfilesGrid_Profiles':
                                                                {
                                                                    'P5': largerResDict,
                                                                    'P6': largerResDict
                                                                }
                                                          }

                testIteration.UpdateServiceConfiguration(updateProps)
                ################################## Add-on Setting ##################################

                testIteration.ActivateService()
                testIteration.StartCapturing()
                startStreamTime = testIteration.StartStreaming()

                ############################ Graphic insertion command ############################
                testCaseSpecificParam = {'StreamTime': startStreamTime[iterParam[SOURCE_ID]][0], 'AnalyzerList': AnalyzerList}
                if iterParam['TestCaseId'] == 'ThreePointTemplateSampleTest':
                    testData = ExecteTestStep_ThreePointTemplateSampleTest(testCaseExecutor, testIteration, iterParam, **testCaseSpecificParam)
                elif iterParam['TestCaseId'] == 'CrawlTextTemplateTest':
                    testData = ExecteTestStep_CrawlTextTemplateTest(testCaseExecutor, testIteration, iterParam, **testCaseSpecificParam)
                elif iterParam['TestCaseId'] == 'HarmonicSqueezeBackTemplateTest' or iterParam['TestCaseId'] == 'DTVSqueezeBackTemplateTest':
                    testData = ExecteTestStep_SqueezeBackTemplateTest(testCaseExecutor, testIteration, iterParam, **testCaseSpecificParam)
                ############################ Graphic insertion command ############################

                testIteration.StopStreaming()
                testIteration.StopCapturing()
                testIteration.DeactivateService()

                if testIteration.HatsSysSetup.setup.encObj.dummyAS is not None:
                    testIteration.HatsSysSetup.setup.encObj.dummyAS.stop()
                OutputFileList, OutputDir = testIteration.GetOutputFileListFromChannel("NTSC_BMW")
                scte30Log, scte104Log = testIteration.HatsSysSetup.setup.encObj.getScteLog(OutputDir)

                # Execute M2Demux, TxMould and PlatformValidator validation
                AnalyzerList['PlatformValidator'] = {}
#                AnalyzerList['TxMould'] = {'mode': 'Golden', 'referenceFilePath': iterParam['GraphicOverlay']['TxMouldGoldenReference'], 'force_list': ['GraphicsOverlayExaminer']}
                AnalyzerList['TxMould'] = {'mode': 'normal'}
                AnalyzerList['M2Demux'] = {'skipM2DemuxBitrate': 240}
                if 'ICDCommand' in AnalyzerList:
                    AnalyzerList['ICDCommand']['scte30LogRef'] = iterParam['GraphicOverlay']['SCTE30ReferenceLogFile']
                    AnalyzerList['ICDCommand']['scte104LogRef'] = iterParam['GraphicOverlay']['SCTE104ReferenceLogFile']
                    AnalyzerList['ICDCommand']['scte30Log'] = scte30Log
                    AnalyzerList['ICDCommand']['scte104Log'] = scte104Log

                testIteration.Validate(AnalyzerList)

                ########################### Graphic insertion validation ############################
                if iterParam['TestCaseId'] == 'ThreePointTemplateSampleTest':
                    ExecteValidation_ThreePointTemplateSampleTest(testCaseExecutor, testIteration, iterParam, **testData)
                elif iterParam['TestCaseId'] == 'CrawlTextTemplateTest':
                    ExecteValidation_CrawlTextTemplateTest(testCaseExecutor, testIteration, iterParam, **testData)
                elif iterParam['TestCaseId'] == 'HarmonicSqueezeBackTemplateTest' or iterParam['TestCaseId'] == 'DTVSqueezeBackTemplateTest':
                    ExecteValidation_SqueezeBackTemplateTest(testCaseExecutor, testIteration, iterParam, **testData)
                ########################### Graphic insertion validation ############################
                testCaseExecutor.HatsIni.logger.MailLog("Info", "Hello1", "World", "This", "works1" )
                #testIteration.Report()
                
        
                testIteration.Report()
                testCaseExecutor.HatsIni.logger.MailLog("Info", "Hello2", "World", "This", "works2" )
    



    
    #HatsIni.logger.MailLog("Info", "", "", "", "Iteration %s: %s (%s)"
    testCaseExecutor.HatsIni.logger.MailLog("Info", "Hello3", "World", "This", "works3" )
    '''
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
         dat.keys()[0] first element in dictionary
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

        #logger.sendMailSimple(configData['TestInformation']['TestName'], 'robert.correll@harmonicinc.com')
        
        
        
        
        #logger.sendMailSimple(configData['TestInformation']['TestName'], 'william.gunnells@harmonicinc.com')
    except:
        print "====reporting error: ? "
    logger.sendMailSimple(configData['TestInformation']['TestName'], 'william.gunnells@harmonicinc.com')
    ''' 
    
