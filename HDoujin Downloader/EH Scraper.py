# -*- coding: UTF-8 -*-
# ==Headers==
# @Name:               EH Scraper
# @Description:        EH Scraper
# @Version:            1.0.0
# @Author:             dodying
# @Date:               2018-02-14 10:10:01
# @Last Modified by:   dodying
# @Last Modified time: 2018-06-02 13:54:26
# @Namespace:          https://github.com/dodying/EH-Scraper
# @SupportURL:         https://github.com/dodying/EH-Scraper/issues
# @Import:
# ==/Headers==

#@Name  EH Scraper
#@Key   EH_Scraper
#@Image EH.png
#@Hook  Books

import clr
import re

clr.AddReference("System")
from System.IO import StreamReader, Directory
from System.Text import UTF8Encoding
# from System.Net import WebRequest
# from System.Text import Encoding

clr.AddReference("Ionic.Zip.dll")
from Ionic.Zip import ZipFile

clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer

def EH_Scraper(books):
  for book in books:
    # ((cYo.Projects.ComicRack.Engine.ComicBook)book).FileLocation
    with ZipFile.Read(book.FileLocation) as zipfile:
      for i in zipfile.Entries:
        if re.search('info.txt', i.FileName):
          infoFile = i.FileName
          with StreamReader(zipfile[infoFile].OpenReader(), UTF8Encoding) as stream:
            contents = stream.ReadToEnd()
            try:
              info = parseInfoContent(contents)
            except:
              print
            else:
              for i in info:
                setattr(book, i, info[i])
            # result = re.search('g/(\d+)/(\w+)/', contents)
            # gid = result.group(1)
            # token = result.group(2)

def parseInfoContent(text):
  info = {}
  text = re.sub('(Page|Image) \\d+: .*','', text)
  text = re.sub('(Downloaded at|Generated by).*', '', text)
  text = re.sub('([\r\n]){2,}', '\n', text)
  text = re.sub('[\r\n]+$', '', text)
  text = re.sub('[\r\n]+> ', '\n', text)
  a = re.compile('[\r\n]+').split(text)
  b = {}

  for i in a:
    t = i.split(': ')
    if len(t) > 1:
      b[t[0].lower()] = t[1]

  print b

  info['Title'] = b['title']
  info['Writer'] = b['author']
  info['Inker'] = b['artist']
  info['Publisher'] = b['publisher']
  info['Summary'] = b['description']
  info['Tags'] = b['tags']
  info['Genre'] = b['type']
  info['Characters'] = b['characters']
  info['Series'] = b['series']
  info['AlternateSeries'] = b['parody']
  info['Web'] = b['url']

  if re.search('Chinese', b['language']):
    info['LanguageISO'] = 'zh'
  elif re.search('English', b['language']):
    info['LanguageISO'] = 'en'
  elif re.search('Japanese', b['language']):
    info['LanguageISO'] = 'jp'
  else:
    info['LanguageISO'] = ''

  return info
