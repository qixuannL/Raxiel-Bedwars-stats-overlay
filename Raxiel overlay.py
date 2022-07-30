
uuid = "bf8f6baeed0340cebd5c3a6682db7394"
key = "PUT_UR_KEY_HERE"
textSize = int(28)
refreshTime = 300
textColor = "#f7f5f5"
from cmath import log
from distutils.log import error
import os
import time
from tkinter.tix import Tree
from unicodedata import name
import winsound
import pyglet
from operator import itemgetter, attrgetter
pyglet.font.add_file('Minecraft.ttf')
textFont = "MinecraftCHMC"
from tkinter import *
import requests
import json
from pprint import pprint
import time
#BE SURE TO INSTALL THE PACKAGES

url = f"https://api.hypixel.net/player?key={key}&uuid={uuid}"
windowWidth = textSize * 27
windowHeight = textSize * 21
playerlist = []
infogotlist = []
firstrun = True
reqstotal = 0
filelines = 0
toggleon = False
ifcheck = False
ifchecks = False
toggleoff = False
def overon():
	
	global toggleon
	toggleon = True
def overoff():
	global toggleoff
	toggleoff = True

def openBW():
	closeOverlay()
	global gameMode
	gameMode = "bw"
	openOverlay()
def openOverlay():
	global overlay
	global playerlist
	
	global statText
	overlay = Toplevel()
	overlay.title('Overlay')
	overlay.geometry(str(windowWidth) + "x" + str(windowHeight)+"+10+30")
	overlay.wm_attributes("-topmost", 1)
	overlay.attributes('-alpha',0.5)
	overlay.overrideredirect(1)
	overlay.tk_setPalette(background='#666665')
	
	#shitty click and drag function
	def move(event):
	    x, y = overlay.winfo_pointerxy()
	    overlay.geometry(f"+{x-100}+{y-100}")
	overlay.bind('<B1-Motion>',move)
	global my_frame
	my_frame = Frame(overlay, width=850, height=570)
	my_frame.pack(fill='both')
	statText = Label(my_frame, font=(textFont, textSize), fg=textColor, anchor="w")
	
	statText.pack()
	#textbox = Text(overlay, height=1, width=25).pack()
	data = requests.get(url).json()
	if gameMode == "bw":
		openOverlay.bwStartFinals = int(data['player']['stats']['Bedwars'].get('final_kills_bedwars', 0))
		openOverlay.bwStartWins = int(data['player']['stats']['Bedwars'].get('wins_bedwars', 0))
		refreshBW()
	

def closeOverlay():
	try:
		overlay.destroy()
	except NameError:
		pass


def getValueFromPath(dict, path):
    for el in path:
        if(el == path[-1]):
            return int(dict.get(el, 0))
        else:
            dict = dict.get(el, {})
    return 0
user = os.getlogin() # gets environment username

def refreshBW():
	
	latest_logs = rf'C:\Users\{user}\.lunarclient\offline\multiver\logs\latest.log'
	global grab_users_data
	global firstrun
	global ifcheck
	global ifchecks
	global overlay
	global reqstotal
	global opText
	global filelines
	global toggleon
	global infogotlist
	global toggleoff
	if ifcheck is True:
		overlay.attributes('-alpha',0)
		infogotlist = []
		ifchecks = True
		ifcheck = False
	if toggleon is True:
		#print("Called")
		overlay.attributes('-alpha',0.5)
		toggleon = False
	if toggleoff is True:
		#print("Called")
		overlay.attributes('-alpha',0.0)
		toggleoff = False	
	if latest_logs is None:
		print("An error has occurred with reading the latest logs file.")
		quit(1)
	counter = 0
	with open(latest_logs, 'r') as f:
		for line in f:
			counter = counter+1
	if firstrun is True:
		#print("FIRST RUN IS CALLED")
		filelines = counter
		firstrun = False
	else:
		#print("NORMAL")
		datatoparse = []
		newlines = counter - filelines
		
		if newlines != 0:
			
			testsite_array = []	
			with open(latest_logs, 'r') as f:
				for line in f:
					testsite_array.append(line)
					
		for x in range(newlines):
			noa = filelines+x
			#print("NOA IS")
			#print(noa)
			#print(testsite_array[noa])
			#datatoparse.append(testsite_array[noa])

			if "[CHAT] ONLINE:" in testsite_array[noa]:
				ifchecks = False
				#print("Do something")
				#occurrences.append(line)
				line = testsite_array[noa].split("ONLINE:")[1].strip()
				#print("FUCTION CALLED")
				players = line.split(", ")
				tempa = []
				for player in players:
					tempa.append(player)
					if(player not in playerlist):
						playerlist.append(player)
						info = grab_users_data(player)
						infogotlist.append(info)
						try:
							infogotlist.sort(key = lambda json: json['weight'], reverse=False)
						except:
							print(" ")#I know this is stupid, But it works.
				for pla in playerlist:
					if(pla not in tempa):
						playerlist.remove(pla)
						for i in range(len(infogotlist)-1):
							if infogotlist[i]["name"] == pla:
								infogotlist.pop(i)
								break
				#print(playerlist)
			if "has joined (" in testsite_array[noa]:
				ifchecks = False
				line = testsite_array[noa].split("[CHAT]")[1].strip().split("has joined")[0].strip()
				if(line not in playerlist):
					playerlist.append(line)
					info = grab_users_data(line)
					#print(info)
					try:
						infogotlist.append(info)
						
						infogotlist.sort(key = lambda json: json['weight'], reverse=False)
					except:
						print(" ")
					#print(infogotlist)
			if "has quit" in testsite_array[noa]:
				ifchecks = False
				line = testsite_array[noa].split("[CHAT]")[1].strip().split("has quit!")[0].strip()
				if(line in playerlist):
					
					playerlist.remove(line)
				
					for i in range(len(infogotlist)-1):
						if infogotlist[i]["name"] == line:
							infogotlist.pop(i)
							break
					
			if "joined the lobby" in testsite_array[noa]:
				if ifchecks is not True:
					ifcheck = True
				
			if "The game starts in 1 second!" in testsite_array[noa]:
				
				overlay.attributes('-alpha',0)
				statText.config(text="")
	filelines = counter
	#print(counter)
	
	#return players
		
	
	def grab_users_data(name):
		global reqstotal
		reqstotal = reqstotal + 1
		if reqstotal > 60:
			print("API_RATE_LIMIT reached")
		
		api_key = key
		overlay.attributes('-alpha',0.5)
		res = requests.get(f"https://api.hypixel.net/player?key={api_key}&name={name}")
		res = json.loads(res.text)
		if res["success"]:
			try:
				bw_stats = res['player']['stats']['Bedwars']
			except:
				return None
			user_bedwars_stats = {}
			#user_bedwars_stats["mcVrp"] = res['player']['mcVersionRp']
			user_bedwars_stats["mvp_pp"] = False
			user_bedwars_stats["rank"] = ""
			user_bedwars_stats["name"] = name
			try:
				rank = res['player']['newPackageRank'] 
			except:
				rank = None
			if rank is None:
				rank = ""
			else:
				if rank == "MVP_PLUS":
					if user_bedwars_stats["mvp_pp"]:
						user_bedwars_stats["rank"] = "[MVP++]"
					else:
						user_bedwars_stats["rank"] = "[MVP+]"
				elif rank == "VIP_PLUS":
					user_bedwars_stats["rank"] = "[VIP+]"
				elif rank == "VIP":
					user_bedwars_stats["rank"] = "[VIP]"
				elif rank == "MVP":
					user_bedwars_stats["rank"] = "[MVP]"
			
			try:
				global fkills
				
				fdeaths = bw_stats['final_deaths_bedwars']
				fkills = bw_stats['final_kills_bedwars']
				
				user_bedwars_stats["fkdr"] = round(fkills/fdeaths, 2)
				
				user_bedwars_stats["finals"] = round(fkills)
				
			except:
				user_bedwars_stats["fkdr"] = 0
				#user_bedwars_stats["fkdr"] 
			try:
				global winss
				winss = bw_stats['wins_bedwars']
				user_bedwars_stats["wins"] = round(winss)
				losss = bw_stats['losses_bedwars']
				user_bedwars_stats["wlr"] = round(winss/losss, 2)

			except:
				user_bedwars_stats["wlr"] = 0
			user_bedwars_stats["lvl"] = res['player']['achievements']['bedwars_level']
			try:
				user_bedwars_stats["ws"] = bw_stats['winstreak']
			except KeyError:
				user_bedwars_stats["ws"] = "?"
			try:
				rank = res['player']['newPackageRank'] 
			except:
				rank = None
			
			user_bedwars_stats["weight"] = round(res['player']['achievements']['bedwars_level']+user_bedwars_stats["fkdr"]*40+winss*0.04+fkills*0.013)
			return user_bedwars_stats
			
		
		else:
			user_bedwars_stats = {}
			user_bedwars_stats["mvp_pp"] = False
			user_bedwars_stats["rank"] = ""
			user_bedwars_stats["name"] = name
			user_bedwars_stats["fkdr"] = "?"
			user_bedwars_stats["wlr"] = "?"
			user_bedwars_stats["finals"] = "?"
			user_bedwars_stats["wins"] = "?"
			user_bedwars_stats["lvl"] = "?"
			user_bedwars_stats["ws"] = "?"
			user_bedwars_stats["weight"] = 100000
			
			
			
			
			
			
			return user_bedwars_stats
	cutestring = ""
	
	for pl in infogotlist:
		try:
			getchar = len("["+str(pl["lvl"])+"⭑]"+pl["rank"]+""+pl["name"])
			air = ""
			for x in range(27-getchar):
				air = air+" "
			getchar2 = len(str(pl["ws"]))
			air2 = ""
			for x in range(4-getchar2):
				air2 = air2+" "
			air3 = ""
			for x in range(6-len(str(pl["fkdr"]))):
				air3 = air3+" "	
			air4 = ""
			for x in range(6-len(str(pl["finals"]))):
				air4 = air4+" "
		
			cutestring =  " ["+str(pl["lvl"])+"⭑]"+pl["rank"]+""+pl["name"]+" "+air+str(pl["ws"]) + air2 + " " + str(pl["fkdr"]) +air3+ " " + str(pl["finals"]) + air4 + " " + str(pl["wins"])+"\n" + cutestring
		except:
			print("")#im so cool.
	statText.config(text=("Player                          | WS | Fkdr | Finals | Wins |\n" + cutestring),anchor="w")
	t = round(time.time())%60
	if t is 60:
		reqstotal = 0
	statText.pack()
	overlay.after(refreshTime, refreshBW)


settings = Tk()
settings.title('Raxiel Overlay')
settings.geometry("280x300")
settings.attributes('-alpha',0.8)
settings.tk_setPalette(background='#474747')
#Settings/Panel Load.
bedwarsText = Label(settings, text="Lunar", font=("Times", 15, "bold")).grid(row=0, column=0)
bedwarsButton = Button(settings, bg="white", height=1, width=2, command=openBW).grid(row=0, column=1)
spacer1 = Label(settings, text="     ", font=("Times", 20, "bold")).grid(row=0, column=2)
skywarsText = Label(settings, text="BLC", font=("Times", 15, "bold")).grid(row=0, column=3)
skywarsButton = Button(settings, bg="white", height=1, width=2, command=openBW).grid(row=0, column=4)
skywarsText2 = Label(settings, text="Other client", font=("Times", 15, "bold")).grid(row=1, column=0)
skywarsButton2 = Button(settings, bg="white", height=1, width=2, command=openBW).grid(row=1, column=1)
linebreak = Label(settings, text="Cmds", font=("Times", 15, "underline")).grid(row=2, column=1)

bridgeText = Label(settings, text="Show", font=("Times", 15, "bold")).grid(row=3, column=0)
bridgeButton = Button(settings, bg="white", height=1, width=2, command=overon).grid(row=3, column=1)
uhcText = Label(settings, text="Hide", font=("Times", 15, "bold")).grid(row=4, column=0)
uhcButton = Button(settings, bg="white", height=1, width=2, command=overoff).grid(row=4, column=1)
linebreak = Label(settings, text="Stats", font=("Times", 15, "underline")).grid(row=5, column=1)
mainloop()
