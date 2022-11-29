import sys
try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
import re
import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
try:
    import json
except:
    import simplejson as json

addon_handle = int(sys.argv[1])
__addon__ = xbmcaddon.Addon()
addon = __addon__
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_version = __addon__.getAddonInfo('version')
try:
    profile = xbmcvfs.translatePath(__addon__.getAddonInfo('profile').decode('utf-8'))
except:
    profile = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))
try:
    home = xbmcvfs.translatePath(__addon__.getAddonInfo('path').decode('utf-8'))
except:
    home = xbmcvfs.translatePath(__addon__.getAddonInfo('path'))

search_icon = f'{home}/resources/media/search.png'
favorite_icon = f'{home}/resources/media/favorite.png'
recommended_icon = f'{home}/resources/media/recommended.png'
news_icon = f'{home}/resources/media/news.png'
viral_icon = f'{home}/resources/media/viral.png'
podcast_icon = f'{home}/resources/media/podcast.png'
leader_icon = f'{home}/resources/media/leader.png'
entertaiment_icon = f'{home}/resources/media/entertaiment.png'
sports_icon = f'{home}/resources/media/sports.png'
science_icon = f'{home}/resources/media/science.png'
technology_icon = f'{home}/resources/media/technology.png'
vlog_icon = f'{home}/resources/media/vlog.png'
settings_icon = f'{home}/resources/media/settings.png'
lang = addon.getSetting('lang')
favorites = os.path.join(profile, 'favorites.dat')
FAV = open(favorites).read() if os.path.exists(favorites)==True else []
    

def setlang(id):
    #english
    if int(lang)==0:
        if id == 'add':
            return 'Added to rumble favorites'
        elif id == 'addfav':
            return 'Add to rumble favorites'
        elif id == 'battle-leaderboard':
            return 'Battle leaderboard'
        elif id == 'config':
            return 'Settings'
        elif id == 'entertainment':
            return 'Entertaiment'
        elif id == 'favorites':
            return 'Favorites'
        elif id == 'news':
            return 'News'
        elif id == 'nofav':
            return 'No videos or channels added to favorites'
        elif id == 'page':
            return 'Page'
        elif id == 'remove':
            return 'Removed from rumble favorites'
        elif id == 'removefav':
            return 'Remove from rumble favorites'
        elif id == 'science':
            return 'Science'
        elif id == 'search':
            return 'Search'
        elif id == 'search-channel':
            return 'Search for channel'
        elif id == 'search-videos':
            return 'Search for video'
        elif id == 'sports':
            return 'Sports'
        elif id == 'subscribers':
            return 'Subscribers'
        elif id == 'technology':
            return 'Technology'
        elif id == 'warning':
            return 'Warning'
        else:
            return 'Incorrect id'
    elif id == 'add':
        return 'Adicionado aos favoritos do rumble'
    elif id == 'addfav':
        return 'Adicionar aos favoritos do rumble'
    elif id == 'battle-leaderboard':
        return 'Quadro de liderança'
    elif id == 'config':
        return 'Definições'
    elif id == 'entertainment':
        return 'Entretenimento'
    elif id == 'favorites':
        return 'Favoritos'
    elif id == 'news':
        return 'Notícias'
    elif id == 'nofav':
        return 'Nenhum video ou canal adicionado nos favoritos'
    elif id == 'page':
        return 'Pagina'
    elif id == 'remove':
        return 'Removido dos favoritos do rumble'
    elif id == 'removefav':
        return 'Remover dos favoritos do rumble'
    elif id == 'science':
        return 'Ciência'
    elif id == 'search':
        return 'Pesquisar'
    elif id == 'search-channel':
        return 'Pesquisar por canal'
    elif id == 'search-videos':
        return 'Pesquisar por video'
    elif id == 'sports':
        return 'Esportes'
    elif id == 'subscribers':
        return 'Inscritos'
    elif id == 'technology':
        return 'Tecnologia'
    elif id == 'warning':
        return 'Aviso'
    else:
        return 'Incorrect id'
            
        


def notify(message,name=False,iconimage=False,timeShown=5000):
    if name and iconimage:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (name, message, timeShown, iconimage))
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, message, timeShown, __icon__))


def to_unicode(text, encoding='utf-8', errors='strict'):
    """Force text to unicode"""
    if isinstance(text, bytes):
        return text.decode(encoding, errors=errors)
    return text
    
def get_search_string(heading='', message=''):
    """Ask the user for a search string"""
    keyboard = xbmc.Keyboard(message, heading)
    keyboard.doModal()
    return to_unicode(keyboard.getText()) if keyboard.isConfirmed() else None


def getRequest(url, ref):
    try:
        ref2 = ref if ref > '' else url
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders=[('Accept-Language', 'en-gb,en;q=0.5'),('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'), ('Referer', ref2)]
        data = opener.open(url).read()
        return data.decode('utf-8')
    except:
        return ''

##menu
def home_menu():
    addDir('[B]'+setlang('search')+'[/B]','',1,search_icon,'','','')
    addDir('[B]'+setlang('favorites')+'[/B]','',7,favorite_icon,'','','')
    addDir('[B]'+setlang('news')+'[/B]','https://rumble.com/category/news'.encode('utf-8'),3,news_icon,'','','other')
    addDir('[B]Viral[/B]','https://rumble.com/category/viral'.encode('utf-8'),3,viral_icon,'','','other')
    addDir('[B]Podcast[/B]','https://rumble.com/category/podcasts'.encode('utf-8'),3,podcast_icon,'','','other')
    addDir('[B]'+setlang('battle-leaderboard')+'[/B]','https://rumble.com/battle-leaderboard'.encode('utf-8'),3,leader_icon,'','','top')
    addDir('[B]'+setlang('entertainment')+'[/B]','https://rumble.com/category/entertainment'.encode('utf-8'),3,entertaiment_icon,'','','other')
    addDir('[B]'+setlang('sports')+'[/B]','https://rumble.com/category/sports'.encode('utf-8'),3,sports_icon,'','','other')
    addDir('[B]'+setlang('science')+'[/B]','https://rumble.com/category/science'.encode('utf-8'),3,science_icon,'','','other')
    addDir('[B]'+setlang('technology')+'[/B]','https://rumble.com/category/technology'.encode('utf-8'),3,technology_icon,'','','other')
    addDir('[B]Vlogs[/B]','https://rumble.com/category/vlogs'.encode('utf-8'),3,vlog_icon,'','','other')
    addDir('[B]'+setlang('config')+'[/B]','',8,settings_icon,'','','')
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=False)
    

def select_search():
    addDir('[B]'+setlang('search-videos')+'[/B]','https://rumble.com/search/video?q='.encode('utf-8'),2,search_icon,'','','video')
    addDir('[B]'+setlang('search-channel')+'[/B]','https://rumble.com/search/channel?q='.encode('utf-8'),2,search_icon,'','','channel')
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle)
    


    

def pagination(url,page,cat,search=False):
    if url > '':
        if search and cat == 'video':
            pageUrl = url + search + "&page=" + str(int(page))
        elif cat in ['channel', 'other']:
            pageUrl = f"{url}?page={int(page)}"
        if int(page) == 1:
            if search:
                status,total = list_rumble(url+search,cat)
            else:
                status,total = list_rumble(url,cat)
        else:
            status,total = list_rumble(pageUrl,cat)
        if search and status == 'true' and cat == 'video' and int(page) < 10 and int(total) > 15:
            name = "[B]"+setlang('page') + " " + str(int(page) + 1) + "[/B]"
            li=xbmcgui.ListItem(name)
            u = f"{sys.argv[0]}?mode=3&name={urllib.quote_plus(name)}&url={urllib.quote_plus(url)}&page={str(int(page) + 1)}&cat={urllib.quote_plus(cat)}&search={urllib.quote_plus(search)}"

            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif not search and cat == 'channel' and status == 'true' and int(page) < 10 and int(total) > 15:
            name = "[B]"+setlang('page') + " " + str(int(page) + 1) + "[/B]"
            li=xbmcgui.ListItem(name)
            u = f"{sys.argv[0]}?mode=3&name={urllib.quote_plus(name)}&url={urllib.quote_plus(url)}&page={str(int(page) + 1)}&cat={urllib.quote_plus(cat)}"

            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif not search and cat == 'other' and status == 'true' and int(page) < 10 and int(total) > 15:
            name = "[B]"+setlang('page') + " " + str(int(page) + 1) + "[/B]"
            li=xbmcgui.ListItem(name)
            u = f"{sys.argv[0]}?mode=3&name={urllib.quote_plus(name)}&url={urllib.quote_plus(url)}&page={str(int(page) + 1)}&cat={urllib.quote_plus(cat)}"

            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle)


def get_image(data,id):
    image_re = re.compile(
        f"i.user-image--img--id-{str(id)}"
        + ".+?{ background-image: url(.+?);",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    ).findall(data)

    return (
        str(image_re[0]).replace('(', '').replace(')', '')
        if image_re != []
        else ''
    )


def list_rumble(url,cat):
    if 'search' in url and cat == 'video':
        data = getRequest(url, '')
        videos_re = re.compile('<h3 class=video-item--title>(.+?)</h3><a class=video-item--a href=(.+?)><img class=video-item--img src=(.+?) alt.+?<div class=ellipsis-1>(.+?)<.+?</div>.+?datetime=(.+?)-(.+?)-(.+?)T', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)    
        if videos_re !=[]:
            for name, link, img, channel, year, month, day in videos_re:
                if int(lang) == 0:
                    time_ = month+'/'+day+'/'+year
                else:
                    time_ = day+'/'+month+'/'+year
                link2 = 'https://rumble.com'+link
                #ftr = [3600,60,1]
                #seconds = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
                name2 = '[B]'+name+'[/B]\n[COLOR gold]'+channel+' - [COLOR lime]'+time_+'[/COLOR]'
                #abrir pegar url e abrir player
                addDir(name2.encode('utf-8', 'ignore'),link2.encode('utf-8'),4,str(img),str(img),'',cat.encode('utf-8'),False,True,1)
            total = len(videos_re)
            status = 'true'
            return status,total
        else:
            total = 0
            status = 'false'
            return status,total
    elif 'search' in url and cat == 'channel':
        data = getRequest(url, '')        
        channel_re = re.compile("<li.+?video-listing-entry.+?<a class=channel-item--a href=(.+?)>.+?<i class='user-image user-image--img user-image--img--id-(.+?)'>.+?<h3 class=channel-item--title>(.+?)</h3>.+?<span class=channel-item--subscribers>(.+?) subscribers</span>.+?</li>",re.DOTALL).findall(data)
        if channel_re !=[]:
            for link, img_id, channel_name, subscribers in channel_re:
                link2 = 'https://rumble.com'+link
                img = get_image(data,img_id)                
                name2 = '[B]'+channel_name+'[/B]\n[COLOR palegreen]'+subscribers+' [COLOR yellow]'+setlang('subscribers')+'[/COLOR]'
                #abrir pegar url e abrir player
                addDir(name2.encode('utf-8', 'ignore'),link2.encode('utf-8'),3,str(img),str(img),'',cat.encode('utf-8'),True,True)
            total = len(channel_re)
            status = 'true'
            return status,total
        else:
            total = 0
            status = 'false'
            return status,total
    elif cat == 'channel' or cat == 'other':
        data = getRequest(url, '')
        videos_from_channel_re = re.compile('<h3 class=video-item--title>(.+?)</h3><a class=video-item--a href=(.+?)><img class=video-item--img src=(.+?) alt.+?<div class=ellipsis-1>(.+?)<.+?</div>.+?datetime=(.+?)-(.+?)-(.+?)T', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if videos_from_channel_re !=[]:
            for name, link, img, channel, year, month, day in videos_from_channel_re:
                if int(lang) == 0:
                    time_ = month+'/'+day+'/'+year
                else:
                    time_ = day+'/'+month+'/'+year
                time_pt = day+'/'+month+'/'+year
                link2 = 'https://rumble.com'+link
                name2 = '[B]'+name+'[/B]\n[COLOR gold]'+channel+' - [COLOR lime]'+time_+'[/COLOR]'
                addDir(name2.encode('utf-8', 'ignore'),link2.encode('utf-8'),4,str(img),str(img),'',cat.encode('utf-8'),False,True,2)
            total = len(videos_from_channel_re)
            status = 'true'
            return status,total
        else:
            total = 0
            status = 'false'
            return status,total
    elif cat == 'top':
        data = getRequest(url, '')
        top_battle_re = re.compile('<h3 class=video-item--title>(.+?)</h3><a class=video-item--a href=(.+?)>.+?<img class=video-item--img-img src=(.+?) alt.+?<div class=ellipsis-1>(.+?)<.+?</div>.+?datetime=(.+?)-(.+?)-(.+?)T', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if top_battle_re !=[]:
            for name, link, img, channel, year, month, day in top_battle_re:
                if int(lang) == 0:
                    time_ = month+'/'+day+'/'+year
                else:
                    time_ = day+'/'+month+'/'+year            
                time_pt = day+'/'+month+'/'+year
                link2 = 'https://rumble.com'+link
                name2 = '[B]'+name+'[/B]\n[COLOR gold]'+channel+' - [COLOR lime]'+time_+'[/COLOR]'
                addDir(name2.encode('utf-8', 'ignore'),link2.encode('utf-8'),4,str(img),str(img),'',cat.encode('utf-8'),False,True,2)
            total = len(top_battle_re)
            status = 'true'
            return status,total
        else:
            total = 0
            status = 'false'
            return status,total            
    else:
        total = 0
        status = 'false'
        return status,total 
        
        
    
def resolver(url):
    data = getRequest(url, '')
    embed_re = re.compile(',"embedUrl":"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if embed_re !=[]:
        data = getRequest(embed_re[0], '')
        sd_480 = re.compile('480,.+?url.+?:"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        hd_720 = re.compile('720,.+?url.+?:"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        fhd_1080 = re.compile('1080,.+?url.+?:"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        sd_360 = re.compile('360,.+?url.+?:"(.*?)",', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if fhd_1080 !=[]:
            url = fhd_1080[0].replace('\\/', '/')
        elif hd_720 !=[]:
            url = hd_720[0].replace('\\/', '/')      
        elif sd_480 !=[]:
            url = sd_480[0].replace('\\/', '/') 
        elif sd_360 !=[]:
            url = sd_360[0].replace('\\/', '/')
        else:
            url = ''
    else:
        url = ''
    return url


def play_video(name, url, iconimage, play=2):
    url = resolver(url)
    if play == 1:
        li = xbmcgui.ListItem(name, path=url)
        li.setArt({"icon": iconimage, "thumb": iconimage})
        li.setInfo(type='video', infoLabels={'Title': name, 'plot': ''})
        xbmc.Player().play(item=url, listitem=li)
    elif play == 2:
        li = xbmcgui.ListItem(name, path=url)
        li.setArt({"icon": iconimage, "thumb": iconimage})
        li.setInfo(type='video', infoLabels={'Title': name, 'plot': ''})
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    
    

def search_items(url,cat):
    vq = get_search_string(heading="Search")
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    pagination(url,1,cat,title)


def getFavorites():
    try:
        try:
            items = json.loads(open(favorites).read())
        except:
            items = ''
        total = len(items)
        if int(total) > 0:
            for i in items:
                name = i[0]
                url = i[1]
                mode = i[2]
                iconimage = i[3]
                fanArt = i[4]
                description = i[5]
                cat = i[6]
                folder = i[7]
                if folder == 'True':
                    folder = True
                else:
                    folder = False
                play = i[8]
                
                
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),mode,str(iconimage),str(fanArt),str(description).encode('utf-8', 'ignore'),cat.encode('utf-8'),folder,True,int(play))
            SetView('WideList')
            xbmcplugin.endOfDirectory(addon_handle)
        else:
            xbmcgui.Dialog().ok('[B]'+setlang('warning')+'[/B]',setlang('nofav'))                
    except:
        SetView('WideList')
        xbmcplugin.endOfDirectory(addon_handle)
            

def addFavorite(name,url,fav_mode,iconimage,fanart,description,cat,folder,play):
    favList = []
    if os.path.exists(favorites)==False:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
        favList.append((name,url,fav_mode,iconimage,fanart,description,cat,folder,play))
        a = open(favorites, "w")
        a.write(json.dumps(favList))
        a.close()
        notify(setlang('add'),name,iconimage)
        #xbmc.executebuiltin("XBMC.Container.Refresh")
    else:
        a = open(favorites).read()
        data = json.loads(a)
        data.append((name,url,fav_mode,iconimage,fanart,description,cat,folder,play))
        b = open(favorites, "w")
        b.write(json.dumps(data))
        b.close()
        notify(setlang('add'),name,iconimage)
        #xbmc.executebuiltin("XBMC.Container.Refresh")


def rmFavorite(name):
    data = json.loads(open(favorites).read())
    for index in range(len(data)):
        if data[index][0]==name:
            del data[index]
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()
            break
    notify(setlang('remove'))
    #xbmc.executebuiltin("XBMC.Container.Refresh")


def addDir(name,url,mode,iconimage,fanart,description,cat,folder=True,favorite=False,play=False):
    if play:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&cat="+urllib.quote_plus(cat)+"&play="+str(play)
    else:
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&cat="+urllib.quote_plus(cat)
    li=xbmcgui.ListItem(name)
    if folder:
        li.setArt({'icon': 'DefaultFolder.png', 'thumb': iconimage})
    else:
        li.setArt({'icon': 'DefaultVideo.png', 'thumb': iconimage})
    if play == 2 and mode == 4:
        li.setProperty('IsPlayable', 'true')
    li.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
    if fanart > '':
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', home+'/fanart.jpg')
    if favorite:
        try:
            name_fav = json.dumps(name.decode('utf-8'))
        except:
            name_fav = name.decode('utf-8')
        try:
            contextMenu = []
            if name_fav in FAV:
                contextMenu.append((setlang('removefav'),'RunPlugin(%s?mode=6&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
            else:
                fav_params = ('%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&cat=%s&folder=%s&play=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description), urllib.quote_plus(cat), urllib.quote_plus(str(folder)), urllib.quote_plus(str(play)), str(mode)))
                contextMenu.append((setlang('addfav'),'RunPlugin(%s)' %fav_params))
            li.addContextMenuItems(contextMenu)
        except:
            pass    
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=li, isFolder=folder)


def SetView(name):
    if name == 'Wall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(500)')
        except:
            pass
    if name == 'List':
        try:
            xbmc.executebuiltin('Container.SetViewMode(50)')
        except:
            pass
    if name == 'Poster':
        try:
            xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
            pass
    if name == 'Shift':
        try:
            xbmc.executebuiltin('Container.SetViewMode(53)')
        except:
            pass
    if name == 'InfoWall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(54)')
        except:
            pass
    if name == 'WideList':
        try:
            xbmc.executebuiltin('Container.SetViewMode(55)')
        except:
            pass
    if name == 'Fanart':
        try:
            xbmc.executebuiltin('Container.SetViewMode(502)')
        except:
            pass


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param



def main():
    params=get_params()
    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=None
    cat=None
    search=None
    folder=None    
    fav_mode=None
    play=1
    page=1

    try:
        url=urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name=urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        iconimage=urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:
        mode=int(params["mode"])
    except:
        pass
    try:
        fanart=urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        description=urllib.unquote_plus(params["description"])
    except:
        pass

    try:
        subtitle=urllib.unquote_plus(params["subtitle"])
    except:
        pass
    try:
        cat=urllib.unquote_plus(params["cat"])
    except:
        pass        
    try:
        search=urllib.unquote_plus(params["search"])
    except:
        pass
    try:
        page=int(params["page"])
    except:
        pass
    try:
        folder=urllib.unquote_plus(params["folder"])
    except:
        pass        
    try:
        fav_mode=int(params["fav_mode"])
    except:
        pass
    try:
        play=int(params["play"])
    except:
        pass        

    if mode==None:
        home_menu()
    elif mode==1:
        select_search()
    elif mode==2:
        search_items(url,cat)
    elif mode==3:
        if search and search !=None:
            pagination(url,page,cat,search)
        else:
            pagination(url,page,cat)
    elif mode==4:
        play_video(name, url, iconimage, play)
    elif mode==5:
        try:
            name = name.split('\\ ')[1]
        except:
            pass
        try:
            name = name.split('  - ')[0]
        except:
            pass
        addFavorite(name,url,fav_mode,iconimage,fanart,description,cat,str(folder),str(play))
    elif mode==6:
        try:
            name = name.split('\\ ')[1]
        except:
            pass
        try:
            name = name.split('  - ')[0]
        except:
            pass
        rmFavorite(name)
    elif mode==7:
        getFavorites()
    elif mode==8:
        xbmcaddon.Addon().openSettings()
        

if __name__ == "__main__":
	main()
