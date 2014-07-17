#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, sys, urllib, urllib2, urlparse, chardet, xbmcplugin, xbmcgui, xbmcaddon, BeautifulSoup, CommonFunctions

class Util:

  __html = __BShtml = None
  __idPlugin = 'script.neverwise'
  __streamVideo = 'video'


  def __init__(self, url):
    self.__responseError = False
    req = urllib2.Request(url, headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0' })

    try:
      response = urllib2.urlopen(req)
    except:
      self.__responseError = True
    else:
      self.__html = response.read()
      response.close()

    if self.__html != None:
      self.__html = self.__html.replace('\t', '').replace('\r\n', '').replace('\n', '').replace('\r', '').replace('" />', '"/>')
      while self.__html.find('  ') > -1: self.__html = self.__html.replace('  ', ' ')


  def hasErrors(self):
    return self.__responseError


  def getBSHtml(self):
    if self.__BShtml == None and self.__html != None:
      self.__BShtml = BeautifulSoup.BeautifulSoup(self.__html)
    return self.__BShtml


  def getBSHtmlDialog(self, dialogTitle):
    self.__showErrorDialog(dialogTitle)
    return self.getBSHtml()


  def getHtml(self):
    return self.__html


  def getHtmlDialog(self, dialogTitle):
    self.__showErrorDialog(dialogTitle)
    return self.getHtml()


  def __showErrorDialog(self, dialogTitle):
    if self.__responseError:
      Util.showConnectionErrorDialog(dialogTitle)


  @staticmethod
  def showConnectionErrorDialog(dialogTitle):
    xbmcgui.Dialog().ok(dialogTitle, Util.getTranslation(Util.__idPlugin, 30001))


  @staticmethod
  def getTranslation(addonId, translationId):
    return xbmcaddon.Addon(addonId).getLocalizedString(translationId).encode('utf-8')


  @staticmethod
  def normalizeText(text):
    try:
      newText = text.decode('utf8', 'xmlcharrefreplace')
    except:
      newText = ''
      for char in text:
        cType = chardet.detect(char)
        if cType['encoding'] == 'ascii' or cType['encoding'] == 'utf8' or cType['encoding'] == 'utf-8':
          newText += char
    return CommonFunctions.replaceHTMLCodes(newText).strip()


  @staticmethod
  def trimTags(html): return re.sub('<.+?>', '', html)


  # Convert parameters encoded in a URL to a dict.
  @staticmethod
  def urlParametersToDict(parameters):
    if len(parameters) > 0 and parameters[0] == '?':
      parameters = parameters[1:]
    return dict(urlparse.parse_qsl(parameters))


  @staticmethod
  def createListItem(name, thumbimage, fanart, streamtype, infolabels):
    li = xbmcgui.ListItem(name, iconImage = 'DefaultFolder.png', thumbnailImage = thumbimage)
    li.setProperty('fanart_image', fanart)
    li.setInfo(streamtype, infolabels)
    return li


  @staticmethod
  def addItem(handle, name, thumbimage, fanart, streamtype, infolabels, duration, url, isFolder):
    li = Util.createListItem(name, thumbimage, fanart, streamtype, infolabels)
    if isFolder:
      url = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(url))
    if streamtype == Util.__streamVideo and duration != None:
      li.addStreamInfo(streamtype, {'duration': duration})
    return xbmcplugin.addDirectoryItem(handle = handle, url = url, listitem = li, isFolder = isFolder)


  @staticmethod
  def AddItemPage(handle, pageNum, thumbimage, fanart, infolabels, params):
    title = '{0} {1} >'.format(Util.getTranslation(Util.__idPlugin, 30002), pageNum)
    Util.addItem(handle, title, thumbimage, fanart, Util.__streamVideo, infolabels, None, params, True)
