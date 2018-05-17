
import random;

# direction list
directions=['north','south','east','west']

# class to describe a room with a true/false indicator for a door in each direction
class Room(object):
  def __init__ (self, xcoord=0,ycoord=0):
# randomly select for each direction whether there is a door or not
     self.doors={dir: bool(random.randint(0,1)) for dir in directions}
     self.xcoord=xcoord
     self.ycoord=ycoord
     
  def wipeDoors(self):
  	 self.doors={dir: False for dir in directions}

  def loadFromFile(self,filename):
     self.sourceFile=filename
  	  
  def listDoors(self):
     print(self.doors)

  def doorList(self):
  	  retStr=""
  	  for dir in directions:
  	  	if self.doors[dir]:
  	  	   retStr+=dir+" "
  	  return retStr
  	  	   
# class to make an n*n array of rooms into a floor
class Floor (object):
	 def __init__(self,size):
	    self.size=size
	    self.rooms=[[Room(x,y) for x in range(size)] for y in range(size)]
	    self.startx=0
	    self.starty=0

	 def loadFloorFile(self, filename):
	     return

	 def randomDoors(self):
	      for x in range(self.size):
	      	for y in range(self.size):
	      		self.rooms[x][y].wipeDoors()
	      		
	      for numDoors in range(self.size*self.size*3):
	 	  	   x1=random.randint(0,self.size-1)
	 	  	   y1=random.randint(0,self.size-1)
	 	  	   x2=x1
	 	  	   y2=y1
	 	  	   dirn1=random.choice(directions)
	 	  	   if dirn1=="north":
	 	  	      y2-=1
	 	  	      dirn2="south"
	 	  	   elif dirn1=="south":
	 	  	   	  y2+=1
	 	  	   	  dirn2="north"
	 	  	   elif dirn1=="east":
	 	  	   	  x2+=1
	 	  	   	  dirn2="west"
	 	  	   else:
	 	  	    	x2-=1
	 	  	    	dirn2="east"
	 	  	    	
	 	  	   if (x2>=0 and x2<self.size and y2>=0 and y2<self.size):
	 	  	    	self.rooms[x1][y1].doors[dirn1]=True
	 	  	    	self.rooms[x2][y2].doors[dirn2]=True
	 	
	 def listRooms(self):
	    print("my floor is ",self.size," by ",self.size)
	    for x in range(self.size):
	 	     for y in range(self.size):
	 	   	    print("room coords x:",self.rooms[x][y].xcoord," y",self.rooms[x][y].ycoord)
	 	   	    self.rooms[x][y].listDoors()

	
	 def drawFloor(self,myX=-1,myY=-1,chars=[],things=[]):
	    for y in range(self.size):
			   ln1="*"
			   ln2="*"
			   for x in range(self.size):
			 	    if self.rooms[x][y].doors["north"]:
			 	       ln1+=" *"
			 	    else:
			 	       ln1+="**"
			 	    if (x==myX and y==myY):
			 	       ln2X="X"
			 	    else:
			 	       ln2X=" "
			 	    for gc in chars:
			 	       if gc.xcoord==x and gc.ycoord==y:
			 	       	  ln2X=gc.myChar() 				 	    
			 	    if self.rooms[x][y].doors["east"]:
			 	   	   ln2+=ln2X+" "
			 	    else:
			 	   	   ln2+=ln2X+'*'	
			   print(ln1)
			   print(ln2)
			   if (y==self.size-1):
			     print("**"*self.size+"*")			 
			     
# implement all the people handling classes	 			           
class Character (object):
	def __init__(self,canMove=True, myX=0,myY=0):
		self.xcoord=myX
		self.ycoord=myY
		self.canMove=canMove
		
	def greeting(self):
		return ""
		
	def mychar(self):
	  return ""
	def playerInteract(self,aPlayer):
	  return

class Wizard(Character):
    def __init__(self,name="", canMove=True,myX=0,myY=0):
      Character.__init__(self,canMove,myX,myY)
      self.name=name

    def greeting(self):
      return "Hello friend, I am the wizard "+self.name
    def myChar(self):
      return "W"
    def playerInteract(self,aPlayer):
      aPlayer.health+=100

class Witch(Character):
    def __init__(self,name="", canMove=True,myX=0,myY=0,myScore=100):
      Character.__init__(self,canMove,myX,myY)
      self.name=name
      self.hurtScore=myScore

    def greeting(self):
      return "Fear me foolish mortal, for I am the witch "+self.name
    def myChar(self):
      return "!"
    def playerInteract(self,aPlayer):
      aPlayer.hurt(self.hurtScore)

class Player(Character):
    def __init__(self,name="",myX=0,myY=0):
      Character.__init__(self,myX,myY)
      self.name=name
      self.health=100
      
    def hurt(self,health=0):
    	self.health-=health
      
       
# now some classes to handle things
class gameThing (object):
	  def __init__(self,myX=0,myY=0,name=""):
	  	self.xcoord=myX
	  	self.ycoord=myY
	  	self.name=name

class gameWeapon(gameThing):
	  def __init__(self,name="weapon",myX=0,myY=0,weaponPoints=0):
	  	gameThing.__init__(self,myX,myY,name)
	  	self.defencePoints=weaponPoints

class gameTreasure(gameThing):
	  def __init__(self,name="treasure",myX=0,myY=0,treasurePoints=0):
	  	gameThing.__init__(self,myX,myY,name)
	  	self.teasurePoints=treasurePoints

# gameWorld is the class that brings all the bits together
class GameWorld (object):
	  def __init__(self,mySize=10):
	  	self.size=mySize
	  	self.floor=Floor(mySize)
	  	self.floor.randomDoors()
	  	self.me=Player(self.floor.startx,self.floor.starty)
	  	self.gameChars=[]
	  	self.gameThings=[]
	  	self.cntTreasure=0
	  	
	  	# add a list of characters in random places
	  	self.addCharacter(Wizard("Gandalf",True,self.randCoord(), self.randCoord()))
	  	self.addCharacter(Wizard("Gizarro",True,self.randCoord(), self.randCoord()))
	  	self.addCharacter(Witch("Medusa",True,self.randCoord(),self.randCoord(),100))
	  	self.addCharacter(Witch("East Witch",False,self.randCoord(),self.randCoord(),400))
	  	
	  	#add some weapons in random places
	  	for wp in ["Gun","Knife","Pepper Spray"] :
	  	  self.addThing(gameWeapon(wp,self.randCoord(),self.randCoord(),100))
	 
	  	#add some treasure in random places
	  	for tr in ["Gold coin","Haribo sweet","Silver coin","Pair of Jordans","map"] :
	  	  self.addThing(gameTreasure(tr,self.randCoord(),self.randCoord(),100))
	  	
	  def addCharacter(self,aChar):
	  	self.gameChars.append(aChar)
	  	

	  def addThing(self,aThing):
	  	self.gameThings.append(aThing)
	  	if type(aThing)=="Treasure":
	  		self.cntTreasure+=1
	  	
	  def randCoord(self):
	  	return random.randint(0,self.size-1)
	  	
	  def characterGreet(self):
	  	for gc in self.gameChars:
	  		print(gc.xcoord, gc.ycoord,gc.greeting())
	  		
	  def getRoomDoorList(self):
	  	return self.floor.rooms[self.me.xcoord][self.me.ycoord].doorList()	
	  def drawGame(self):
	  	self.floor.drawFloor(self.me.xcoord,self.me.ycoord,self.gameChars,self.gameThings)
	
	  def drawStatus(self):
	  	print("you are in room x=",self.me.xcoord," y=",self.me.ycoord)
	  	dlist=self.getRoomDoorList()
	  	thingStr="You are holding:"
	  	for th in self.gameThings:
	  		if th.xcoord==-1 and th.ycoord==-1:
	  			thingStr+=" "+th.name
	  	print(thingStr)
	  			
	  	print("I see doors to the:",dlist)
	  	print("health=",self.me.health)
	  	for wp in self.gameThings:
	  		if wp.xcoord==self.me.xcoord and wp.ycoord==self.me.ycoord:
	  			print("There is a ",wp.name," here")
	  			
	  def moveCharacters(self):      
	    for gc in self.gameChars:
	    	if gc.canMove:
	  		  thisRoom=self.floor.rooms[gc.xcoord][gc.ycoord]
	  		  dirn=random.choice(directions)
	  		  if thisRoom.doors[dirn]==True:
	  		     if dirn=="north":
	  		        gc.ycoord-=1
	  		     elif dirn=="south":
	  		   	    gc.ycoord+=1
	  		     elif dirn=="west":
	  		   		  gc.xcoord-=1
	  		     else:
	  		   	    gc.xcoord+=1
	    return
	    
	  def countRoomThings(self):
	  	cnt=0
	  	for th in self.gameThings:
	  		if th.xcoord==self.me.xcoord and th.ycoord==self.me.ycoord:
	  			cnt+=1
	  	return cnt 
	  	
	  def pickUpThings(self):
	  	for th in self.gameThings:
	  		if th.xcoord==self.me.xcoord and th.ycoord==self.me.ycoord:
	  		  print("picked up ",th.name)
	  		  th.xcoord=-1
	  		  th.ycoord=-1
	  	
		
# Start setting ourselves up. make it 10*10
MySize=10
gw=GameWorld(MySize)

# for debugging list the doors and draw the structure
#afloor.listRooms()


print("*** NEW GAME STARTING ***")
# debugging 
for gt in gw.gameThings:
	print(gt.name,"at x:",gt.xcoord," y:",gt.ycoord)
print()


finished=False
# game loop moving you around and interacting with stuff
while not finished:
	print()
	gw.drawGame()
	gw.drawStatus()
# debug gw.characterGreet()
#	greet and interact with you if you're in the same room as one of the characters
	for gc in gw.gameChars:
		if (gc.xcoord==gw.me.xcoord and gc.ycoord==gw.me.ycoord):
			print(gc.greeting())
			gc.playerInteract(gw.me)
			finished=(gw.me.health<=0 or gw.me.health>400)

# handle picking up things
	if gw.countRoomThings()>0:
		if input("Would you like to pick this stuff up Y/N?")=="Y":
			gw.pickUpThings()
	
	# check if i have all treasure
	allTreasure=False
	for gt in gw.gameThings:
	  if isinstance(gt,gameTreasure) and (gt.xcoord!=-1 or gt.ycoord!=-1):
		  print("you dont have:",gt.name)
		  allTreasure=False	
	finished=finished or allTreasure
	
	# handle moving. 	
	dlist=gw.getRoomDoorList()
	usrInput=input("where would you like to go N/S/E/W/Q?")
	#only allow Go N/S/E/W in legitimate directions
	if usrInput=="N" and "north" in dlist:
		  gw.me.ycoord-=1 
	if usrInput=="S" and "south" in dlist:
		  gw.me.ycoord+=1
	if usrInput=="E" and "east" in dlist:
		  gw.me.xcoord+=1 
	if usrInput=="W" and "west" in dlist:
		  gw.me.xcoord-=1 
	
	finished= finished or usrInput=="Q"
	
	gw.moveCharacters()

print("*** GAME OVER ***")
if gw.me.health<=0:
	print("you died!")
elif usrInput=="Q":
	print("You Quit!")
else:
	print("congrats - you won!")
