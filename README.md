# steam_api
![alt tag](http://2.bp.blogspot.com/_pCYGtGEULgk/S9YnaepswpI/AAAAAAAAAFM/l5Vly2qgeEc/s1600/2000px-Steam_logo.svg.png)
## Author
Michael Pare

SteamAPI 
========
An object-oriented Python 3.5+ library for accessing the Steam Web API.

## Coding Specifications
Using the requests and json python module I have created an easy way to access information from Steam's Web Api 
[Web API](http://steamcommunity.com/dev) about steam games as well as steam users to do so with as you please.

# Example

'''
import steam_app
import random 

def main():
    print('{0:=^50s}'.format('=')) #---------------------------------------------------------------------------
    steamid = 0
    steam_obj = steam_app.steam_connect('xxxxxxxxxxxxxxxxxxxxxxxxxx') #ENTER YOUR API CODE HERE
    while True:
        usr_input = input("please enter your steam id or 'q' to quit: ")
        if usr_input == 'q' or usr_input == 'Q':
            print('Goodbye Friend')
            exit()
        elif usr_input == '':
            continue
        try:
            current_user = steam_obj.create_usr(usr_input)
            #t = time.time()
            break
        except ValueError as e:
            print(e)
            continue

    print("Your current steam user name is {0}".format(current_user.display_name))
    if current_user.realname == 'hidden':
        print('You have hidden your real name.')
    else:
        print("Your real name is {0}".format(current_user.realname))

    randnum1 = random.randrange(len(current_user.friends))
    current_user.friends[randnum1].friend_get_info()
    print("You have {0} friends, one of which is {1};\nYou've been friends since {2}"
        .format(len(current_user.friends), current_user.friends[randnum1].display_name, current_user.friends[randnum1].friend_since))
    randnum2 = random.randrange(current_user.game_count) - 1
    print("You have {0} games, one of which is {1};\nwhich you've played for {2} minutes"
        .format(current_user.game_count, current_user.games[randnum2].name, current_user.games[randnum2].playtime_forever))


    #t2 = time.time() - t
    #print(t2)
    print('{0:=^50s}'.format('=')) #---------------------------------------------------------------------------

if __name__ == '__main__':
    main()

'''


