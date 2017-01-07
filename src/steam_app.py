#!/usr/bin/env python3

import requests
import json
import pprint
import time
import random 




class new_game:
    def __init__(self, appid, gname, icon, key, playtime=None):
        self.id = appid
        self.key = key
        self.name = gname
        self.playtime_forever = playtime
        self.icon_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/{0}/{1}.jpg'.format(str(self.id), icon)
        self.game_banner = 'http://cdn.edgecast.steamstatic.com/steam/apps/{0}/header.jpg'.format(str(self.id))

    def get_stats(self):
        self.achievements = []
        achieve_url = 'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={0}&appid={1}'.format(self.key, self.id)
        json_obj_stats = requests.get(achieve_url)
        stat_dict = json_obj_stats.json()
        #ADD CHECK FOR ARCHIEVEMENTS
        if 'availableGameStats' in stat_dict['game'].keys():
            self.has_achievements = True
            for achieve in stat_dict['game']['availableGameStats']['achievements']:
                if achieve['hidden'] == 1: #achievement is hidden
                    new_achievement = achievement(achieve['name'], achieve['displayName'], achieve['icon'], "Description Hidden")
                    self.achievements.append(new_achievement)
                elif achieve['hidden'] == 0: #achievement is not hidden
                    new_achievement2 = achievement(achieve['name'], achieve['displayName'], achieve['icon'], achieve["description"])
                    self.achievements.append(new_achievement2)
        else:
            self.has_achievements = False


class achievement:
    def __init__(self, a_name, dname, icon_url, descrip):
        self.name = a_name
        self.display_name = dname
        self.icon = icon_url
        self.description = descrip


class new_friend:
    def __init__(self, friend_id, date, key):
        self.id = friend_id
        self.api_key = key
        if date == 0:
            self.friend_since = None
        else:
            self.friend_since = time.ctime(date)

        self.display_name = None
        self.avatar_img = None

    def friend_get_info(self):
        frnd_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}'.format(
            self.api_key, self.id)
        json_obj_friend = requests.get(frnd_info_url)
        friend_dict = json_obj_friend.json()
        self.display_name = friend_dict['response']['players'][0]['personaname']
        self.avatar_img = friend_dict['response']['players'][0]['avatarfull']


class steam_usr:
    def __init__(self, usr_url, key):
        self.api_key = key
        resolve_vanity = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={0}&vanityurl='.format(self.api_key)
        json_obj_init = requests.get(resolve_vanity + usr_url)
        usr_dict = json_obj_init.json()
        if usr_dict['response']['success'] == 1:
            steamid = usr_dict['response']['steamid']
        else:
            raise ValueError('Steam User not Found') 


        self.api_key = key
        self.url = usr_url
        self.steamid = steamid
        user_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}'.format(
            self.api_key, self.steamid)
        #here we collect of the steam accounts info
        json_obj_usr = requests.get(user_info_url)
        info_dict = json_obj_usr.json()
        self.display_name = info_dict['response']['players'][0]['personaname']
        self.avatar_img = info_dict['response']['players'][0]['avatarfull']
        self.current_state= info_dict['response']['players'][0]['personastate']
        self.creation = time.ctime(info_dict['response']['players'][0]['timecreated'])
        if 'realname' in info_dict['response']['players'][0].keys():
            self.realname = info_dict['response']['players'][0]['realname']
        else:
            self.realname = 'Private'

        #Here we are going to get the users friends list
        friend_url='http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={0}&steamid={1}&relationship=friend'.format(
            self.api_key, self.steamid)
        json_obj_frnd = requests.get(friend_url)
        friend_dict = json_obj_frnd.json()
        self.friends = []
        #DYNAMICALLY CREATE FRIEND OBJECTS WHEN QUERIED
        for i in range(len(friend_dict['friendslist']['friends'])):
            friend = new_friend(friend_dict['friendslist']['friends'][i]['steamid'], friend_dict['friendslist']['friends'][i]['friend_since'],
            self.api_key)
            self.friends.append(friend)
        #get user games
        usr_games = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&include_appinfo=1&steamid={1}&format=json'.format(
            self.api_key, self.steamid)
        json_obj_GMS = requests.get(usr_games)
        games_dict = json_obj_GMS.json()
        self.game_count = games_dict['response']['game_count']
        self.games = []
        for game in games_dict['response']['games']:
            newgame = new_game(game['appid'], game['name'], game['img_icon_url'], self.api_key, game['playtime_forever'])
            self.games.append(newgame)
        #recently played
        

        #will do achievements later
class steam_connect:
    def __init__(self, usr_key):
        self.api_key = usr_key
        test_url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={0}&vanityurl={1}'.format(self.api_key, 'THUGGINANDLOVIN')
        test_key = requests.get(test_url)
        if test_key.status_code == 200:
            #confirmed api key is valid
            pass
        else:
            raise ValueError('Steam API key invalid') 

    def create_usr(self, usr_id):
        return steam_usr(usr_id, self.api_key)
    def create_game(self, game_id):
        return game(self, game_id, self.api_key)

