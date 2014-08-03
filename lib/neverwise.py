#!/usr/bin/python
# -*- coding: utf-8 -*-
import re, sys, urllib, urllib2, urlparse, chardet, xbmcplugin, xbmcgui, xbmcaddon, BeautifulSoup, CommonFunctions

class Util(object):

  _html = _BShtml = None
  _idPlugin = 'script.module.neverwise'
  _addonName = xbmcaddon.Addon().getAddonInfo('name')


  def __init__(self, url):
    self._responseError = False
    req = urllib2.Request(url, headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0' })

    try:
      response = urllib2.urlopen(req)
    except:
      self._responseError = True
    else:
      self._html = response.read()
      response.close()
      if self._html.find(b'\0') > -1: # null bytes, if there's, the response is wrong.
        self._responseError = True
        self._html = None

    if self._html != None:
      self._html = self._html.replace('\t', '').replace('\r\n', '').replace('\n', '').replace('\r', '').replace('" />', '"/>')
      while self._html.find('  ') > -1: self._html = self._html.replace('  ', ' ')


  def getBSHtml(self, showErrorDialog = False):
    self._showErrorDialog(showErrorDialog)
    if self._BShtml == None and self._html != None:
      self._BShtml = BeautifulSoup.BeautifulSoup(self._html)
    return self._BShtml


  def getHtml(self, showErrorDialog = False):
    self._showErrorDialog(showErrorDialog)
    return self._html


  def _showErrorDialog(self, showErrorDialog = False):
    if showErrorDialog and self._responseError:
      Util.showConnectionErrorDialog()


  @staticmethod
  def showConnectionErrorDialog():
    xbmcgui.Dialog().ok(Util._addonName, Util.getTranslation(33001, Util._idPlugin))


  @staticmethod
  def showVideoNotAvailableDialog():
    xbmcgui.Dialog().ok(Util._addonName, Util.getTranslation(33002, Util._idPlugin))


  @staticmethod
  def getTranslation(translationId, addonId = ''):
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
  def createListItem(label, label2 = '', iconImage = None, thumbnailImage = None, path = None, fanart = None, streamtype = None, infolabels = None, duration = '', isPlayable = False):
    li = xbmcgui.ListItem(label, label2)

    if iconImage:
      li.setIconImage(iconImage)

    if thumbnailImage:
      li.setThumbnailImage(thumbnailImage)

    if path:
      li.setPath(path)

    if fanart:
      li.setProperty('fanart_image', fanart)

    if streamtype:
      li.setInfo(streamtype, infolabels)

    if streamtype == 'video' and duration:
      li.addStreamInfo(streamtype, {'duration': duration})

    if isPlayable:
      li.setProperty('IsPlayable', 'true')

    return li


  @staticmethod
  def addItems(handle, items):
    if len(items) > 0:
      listItems = []
      for url, listitem, isFolder, urlIsParams in items:
        if urlIsParams:
          url = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(url))
        listItems.append([url, listitem, isFolder])

      xbmcplugin.addDirectoryItems(handle, listItems)
      xbmcplugin.endOfDirectory(handle)
    else:
      xbmcgui.Dialog().ok(Util._addonName, Util.getTranslation(33003, Util._idPlugin))


  @staticmethod
  def createItemPage(pageNum):
    title = '{0} {1} >'.format(Util.getTranslation(33000, Util._idPlugin), pageNum)
    return Util.createListItem(title)


  @staticmethod
  def playStream(handle, label, thumbnailImage = None, path = None, streamtype = None, infolabels = None):
    li = Util.createListItem(label, thumbnailImage = thumbnailImage, path = path, streamtype = streamtype, infolabels = infolabels)
    xbmcplugin.setResolvedUrl(handle, True, li)
