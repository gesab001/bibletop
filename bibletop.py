import datetime
import json
import subprocess
import time
from tkinter import *
length = 240
id = "1"
start = "00:00:00,000" 
to = "-->"
end = " 00:01:00,000"
words = "Is that you on the beach?"
toString = id + "\n" + start + "\n" + to + "\n" + end + "\n" + words + "\n\n"

totalVerses = 31102
file = open("F:\\movies\\bible.json", "r")
json_data = json.load(file)

def getCurrentID():
   first_time = datetime.datetime(2018,6,23)
   later_time = datetime.datetime.now()    
   duration = later_time - first_time
   duration_in_s = duration.total_seconds() 
   minutes = divmod(duration_in_s, 60)[0]  
   currentID = minutes
   while currentID>totalVerses:
      currentID = currentID - totalVerses
   return int(currentID)

def getBooks():
  verses = json_data["bible"]
  books = []
  for verse in verses:
   book = verse["book"]
   if book not in books:
      books.append(book)
  return books
  
def getBibleTopic(topic):
  verses = []  
  if topic=="all":
    verses = json_data["bible"]
  else:
    bible = json_data["bible"]
    for item in bible:
        verse = item["word"]
        if topic.lower() in verse.lower():
           verses.append(item)
           print(verse)		   
  return verses
 
 
def getBookVerses(bookTitle):
    verses = []
    bible = json_data["bible"]
    for item in bible:
        verse = item["book"]
        if bookTitle.lower() in verse.lower():
           verses.append(item)
           print(verse)		   
    return verses
bible = []
choice = input("topic or book: ")

if choice=="book":
 books = getBooks()
 topic = input("book name: " )
 for book in books:
  if topic.lower() == book.lower():
   bookName = book
   bible = getBookVerses(bookName)
else:  
 topic = input("topic: " )
 bible = getBibleTopic(topic)  

totalVerses = len(bible)
  
def getVerse(id):

	verse = bible[id-1]
	return verse
   
def getMinute(minutes):
   result = '{:02d}:{:02d}:00,000'.format(*divmod(minutes, 60 ))
   return result
 
currentID =  getCurrentID() 
subtitles = ""
subtitles_json = {}
subtitles_list = []
for i in range(1, length, 1):
	id = str(i)
	start = getMinute(i-1)
	end = getMinute(i)
	verse = getVerse(currentID)	
	words = verse["word"] + " \n" + verse["book"] + " " + str(verse["chapter"]) + ":" + str(verse["verse"])
	toString = id + "\n" + start + " " + to + " " + end + "\n" + words + "\n\n"
	print(toString)
	currentID = currentID + 1
	if currentID>totalVerses:
	  currentID = 1
	subtitles = subtitles + toString
	subtitles_list.append(words)

subtitles_json["subs"] = subtitles_list
outfile = open("bible-subtitles.srt", "w")
outfile.write(subtitles)
outfile.close()
outfile = open("bible-subtitles.json", "w")
json.dump(subtitles_json, outfile)
#title = input("title: " )
assfile = "bible-subtitles.ass"
convertoass =  "ffmpeg -i bible-subtitles.srt " + assfile
subprocess.call(convertoass, shell=True)

#moviefilename = title
#fontSize = input("font size: ")
#position = input("position(6=top,2=bottom)")
#repeat = input("repeat (0=forever): ")
#style = ":force_style='Alignment="+position+",Fontsize="+fontSize+"'"
#command = "ffplay -loop "+ repeat +" -vf subtitles="+assfile + style+" -i " + moviefilename;
#subprocess.call(command, shell=True)



class MyFirstGUI:
    id = 0
    string = "hello"
    fontSize = 16
    def __init__(self, master, subs_list):
        self.subs_list = subs_list
        self.master = master
        #self.master.protocol('WM_DELETE_WINDOW', lambda: None) 
        #self.master.overrideredirect(True)
        self.label = Label(self.master, text=self.string)
        #self.label.config(font=("Courier", self.fontSize))
        self.label.pack()
        self.greet()
        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        self.master.attributes('-topmost', 'true')
		
    def greet(self):
        self.string = self.subs_list[self.id]
        self.label.config(text=self.string)
        self.label.pack()
        print(self.string) 
        self.master.title(self.string)
        self.label.pack()
        self.id = self.id + 1
        self.master.after(60000, self.greet)


root = Tk()
my_gui = MyFirstGUI(root, subtitles_list)
root.after(2000, my_gui.greet)
root.mainloop()
  
