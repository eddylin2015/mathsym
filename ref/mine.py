import datetime
FORWARD="forward"
GRASS="grass"
DOWN="down"
RIGHT_TURN="right"
class Player:
    def on_chat(self, talk, act):
        '''Return days later in YYYY-MM-DD format.'''
        print("Talk...")
        return None

class Agent:
    '''Some helper functions to quickly calculate date.'''
    today_date = datetime.date.today()
    def move(self, act, step=1):
        '''Return days later in YYYY-MM-DD format.'''
        print(act)
        print(step)
        return None
    
    def till(self,dire):
        print(dire)
        
    def place(self, place):
        '''Return days ago in YYYY-MM-DD format.'''
        print(place)
        return None
    
    def set_item(self,mat,i,j):
        '''Return today in YYYY-MM-DD format.'''
        print(r"set item %s " % mat)
        return None

    def turn(self,dire):
        '''Return tomorrow in YYYY-MM-DD format.'''
        print(r"turn %s " % dire)
        return None
    
    def teleport_to_player(self):
        '''Return yesterday in YYYY-MM-DD format.'''
        print("call to here")
        return None