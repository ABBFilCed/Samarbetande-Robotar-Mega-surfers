from tkinter import * # importerar tkinter som är ett grafiskt bibilotek
import time
print("helo")
master = Tk()
master.geometry('1000x1000')

txt = Text(master, height = 2, width = 50) # skapar textruta
txt.pack()
txt.insert(END, "Visualisering av robotens körsträcka.")

distx = 0
disty = 0 
strlRuta = 10

C = Canvas(master, height = 1000, width = 1000)
C.pack()
w = 50
h = 50
num = 5

for row in range (0, w): # skapar matrix, kollar vidare på detta för utveckling sen. 
    for col in range(0, h):
        distx += strlRuta
        koordinater = distx, disty, distx + strlRuta, disty + strlRuta # koordinater för x och y led samt bredd och höjd på dessa
        if num % 50 == 0:
            time.sleep(1)
            C.create_rectangle(koordinater, fill = "SkyBlue2")
        else:
            C.create_rectangle(koordinater, fill = "White")
        num += 1
    disty += strlRuta
    distx = 0 

def whereHaveIBeen():
    linesPassed = "mqtt"
    if forward:
        newcoordinates = distx, (disty + 1), distx + strlRuta, (disty + 1) + strlRuta
    if backward:
        newcoordinates = distx, (disty - 1), distx + strlRuta, (disty - 1) + strlRuta
    if right:
        newcoordinates = (distx + 1), disty, (distx + 1) + strlRuta, disty + strlRuta
    if left:
        newcoordinates = (distx + 1), disty, (distx + 1) + strlRuta, disty + strlRuta


    if linePassed == True: 
        C.create_rectangle(newcoordinates, fill = "SkyBlue2")
        
    

mainloop()