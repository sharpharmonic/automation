#------------------------------------------------------------------------
# Name: GraphicAnalyzer.py
# Purpose: Analyze transport stream crawl and fade using tesseractOCR                       
# Author: William Gunnells                     
# Created: 7/21/2015             
# Copyright: (c) Harmonic 2015              
# License: GNU               
# Comment: https://code.google.com/p/tesseract-ocr/ 
# Dependencies: pytesseract, PIL, qhull, pytesser
# Required: pytesser.py, util,py, error.py, tesseract.exe, /tessdata 
# Required: Hash init errors replace from PIL import ImageChops with import ImageChops
# Required: easy_install Image  
# Setup: C:\TestSetup\crawl.csv
#    Video,startingFrame,noOfFrames,position,String
#    cap_25001.ts,2270,300,"""4,25,1850,127""",HATS
#------------------------------------------------------------------------                          

#===== Import Statements================
import time, os, sys , shutil 
#====== HATS Specific ==================
from Analyzers.ffmpeg import Parseffmpeg
#====== Analyzer OCR  ==================
from pytesser.pytesser import *
# from PIL import ImageChops
import ImageChops
import datetime

# --------------------------------------------------------------------
#  Globals
# --------------------------------------------------------------------

assetdir = 'c:\ElectraXTestLog\\'
threecrawl = '\ThreePointTemplate\CrawlTextTemplateTest_I2\NTSC_BMW\\'


def largestdir():
    ar = []
    try:
        for i in os.listdir(assetdir):
            if 'csv' not in i:
                #print i
                ar.append(i)
        return max(ar)
    except:
        return max([123, 223])
pack = assetdir + str(largestdir()) + threecrawl
# print pack 


def ConvertTsToPNG(tsFile, startingFrame, noOfFrames, isInterace=False):
    '''Convert to png using values from csv file tsFile=clip.mpg startingFrame=x,noOfFrames=x'''
    # ffmpegObj = Parseffmpeg(tsFile) # directory to tsfile ex:('c:/tempdir' + tsFile)
    ffmpegObj = Parseffmpeg(pack + tsFile)  # directory to tsfile ex:('c:/tempdir' + tsFile)
    pngfolderpath = tsFile + '_img'
    if os.path.exists(pngfolderpath):  # check existing dir
        try:
            shutil.rmtree(pngfolderpath)  # remove existing dir
        except Exception, err:
            sys.stderr.write(str(err))
            #print "make sure you have correct file name"
    print "create png files"
    ffmpegObj.ExtractFramesToPng(pngfolderpath, startingFrame, noOfFrames)  # create blah.mpg_img


def verifycsv(csvfile, number):
    '''Dictionary of: clip, startingFrame,noOfFrames,text_crawl_position=(left,top,right,bottom), String'''
    try:
        f = open(csvfile, 'r')
        dat = f.readlines()
        try:
            data = dat[number].replace("\"", "").split(",")
            mdict = {'video': data[0], 'startingFrame': int(data[1]), 'noOfFrames': int(data[2]), 
                     'left': int(data[3]), 'top': int(data[4]), 'right': int(data[5]), 
                     'bottom': int(data[6]), 'searchstring': data[7]}
            f.close()
            return mdict
        except IndexError:
            print "Incorrect number of fields in CSV file."
    except Exception, err:
        print "\nCSV file issues: %s" % err 


def analyzeborder(tsFile, left, top, right, bottom):  # crawl text border
    '''Text crawl crop function: clip, int=(left,top,right,bottom)'''
    clipfolder = tsFile + '_img/' 
    for i in os.listdir(clipfolder):
        print "working on %s " % i
        im = Image.open(clipfolder + i) 
        box = (left, top, right, bottom)  # megryan=0,0,150,100 ; hk=0,10,1200,80
        area = im.crop(box)
        newimage = tsFile + '_img/' + 'cropped' + i
        area.save(newimage, 'png')
        print "save cropped png"


def analyzecrawl(tsFile, searchstring):
    reportlist = []
    reportdict = {}
    '''Tesseract analyzes text from png files: tsFile=name_of_png_in_directory, searchstring '''
    print "========Analyze Text Crawl========"
    #clip10=tsFile + '_img/' + Clip ;;im = Image.open(clip10);;text = image_to_string(im);;print text
    clipfolder = tsFile + '_img/'
    for i in os.listdir(clipfolder):
        if 'cropped' in i:  # speed search only look at cropped files
            print "analyzing %s" % i
            #time.sleep(2)
            im = Image.open(clipfolder + i)
            print im
            print clipfolder
            print os.getcwd()
            print "cwd printed above"
            # pytesser.image_to_string
            os.chdir("pytesser") # normally not needed but tesseract.exe needs to be in
            # same directory as pytesser.py 
            text = image_to_string(im)  # str contains asci garbage 
            print text
            os.chdir("..") # change back to previous directory where 
            #files are split into png's
            textline = text.split("\n")  # split garbage by lines & make list
            search = searchstring.replace("\n", "")  # remove \n newline 
            for j in range(len(textline)):
                if search in textline[j]:  # search for string in list
                    print 'Pass: %s' % textline[j]  # match
                    reportlist.append(textline[j])
                    reportdict[i] = textline[j]
    print "done analyzing files"
    
    # return reportlist
    return reportdict


def matchTemplate(searchImage, templateImage):
    '''Template matching algorithm: searchImage, templateImage. TempImg() saves templateImage save file''' 
    minScore = -1000
    matching_xs = 0
    matching_ys = 0
    # convert images to "L" to reduce computation by factor 3 "RGB"->"L"
    searchImage = searchImage.convert(mode="L")
    templateImage = templateImage.convert(mode="L")
    searchWidth, searchHeight = searchImage.size
    print "------"
    print searchImage.size
    print "------"
    templateWidth, templateHeight = templateImage.size
    # make a copy of templateImage and fill with color=1
    templateMask = Image.new(mode="L", size=templateImage.size, color=1)
    #loop over each pixel in the search image
    for xs in range(searchWidth - templateWidth + 1):
        for ys in range(searchHeight - templateHeight + 1):
            #set some kind of score variable to "All equal"
            score = templateWidth * templateHeight
            # crop the part from searchImage
            searchCrop = searchImage.crop((xs, ys, xs + templateWidth, ys + templateHeight))
            diff = ImageChops.difference(templateImage, searchCrop)
            notequal = ImageChops.darker(diff, templateMask)
            countnotequal = sum(notequal.getdata())
            score -= countnotequal
            if minScore < score:
                minScore = score
                matching_xs = xs
                matching_ys = ys
    print "Location=", (matching_xs, matching_ys), "Score=", minScore
    return matching_xs
    im1 = Image.new('RGB', (searchWidth, searchHeight), (80, 147, 0))
    im1.paste(templateImage, ((matching_xs), (matching_ys)))
    #searchImage.show()
    #im1.show()
    im1.save('template_matched_in_search.png')


def TempImg(tsFile, cropped):
    '''TempImage is less than half the first cropped image for left=50%, top=0,right=50, bottom=25%''' 
    # clip=tsFile + '_img/'+ 'cropped0025.png'
    clip = tsFile + '_img/' + cropped
    im = Image.open(clip)
    width = im.size[0] 
    height = im.size[1]
    # box=(int(width/2),0,int(width/2)+80,int(height/1.25))
    box = (width - 200, 0, int(width - 200) + 80, int(height / 1.25))
    print box
    area = im.crop(box)
    newimage = tsFile + '_img/' + 'template.png'
    area.save(newimage, 'png')
    print "saved template image"


def TrackTextCrawl(tsFile, pngkey):
    track = []
    dirpath = tsFile + '_img/'
    Timage = tsFile + '_img/' + 'template.png'
    num = 0
    token = False
    for i in os.listdir(dirpath):
        dat = i.startswith(pngkey)
        if dat:
            token = True
        if token:
            if num <= 3:
                if 'cropped' in i:  # read only cropped images
                    searchImage = Image.open(dirpath + i) 
                    templateImage = Image.open(Timage)
                    t1 = datetime.datetime.now()
                    matchTemplate(searchImage, templateImage)
                    track.append(matchTemplate(searchImage, templateImage))
                    delta = datetime.datetime.now() - t1
                    print "Time=%d.%d" % (delta.seconds, delta.microseconds)
                    print i
                    num += 1
            else:
                break
    return track


if __name__ == "__main__":
    v = verifycsv('c:\TestSetup\crawl.csv', 1)
    #ConvertTsToPNG(v['video'], v['startingFrame'], v['noOfFrames'], isInterace=False) 
    ConvertTsToPNG(v['video'], v['startingFrame'], 10, isInterace=False) 
    analyzeborder(v['video'], v['left'], v['top'], v['right'], v['bottom']) 
    dat = analyzecrawl(v['video'], v['searchstring']) 
    print dat
    TempImg(v['video'], dat.keys()[0])  # dat.keys()[0] first element in dictionary
    track = TrackTextCrawl(v['video'], dat.keys()[0])
    print "===================reporting ================="
    print "Pass: %s" % str(dat.keys()[0])


    ''' # unittest
    print type(verifycsv('crawl.csv',4))  == type({})
    assert verifycsv('crawl.csv',1) , 'The file does not exist: %s' % 'crawl.csv'
    assert type(verifycsv('crawl.csv',1))==type({})
    # ConvertTsToPNG('obrother.mpg', 665, 10, isInterace=False) 
    '''
