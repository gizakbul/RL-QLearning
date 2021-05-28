from tkinter import * #arayüz kütüphanesi
import tkinter as tk
from random import *
import time
import numpy as np
from PIL import Image, ImageTk
from numpy.lib.npyio import savez_compressed  # For adding images into the canvas widget
import matplotlib.pyplot as plt


master = Tk()
"""ajanX = int(baslangic_x.get())
ajanY = int(baslangic_y.get())
hedefX = int(hedef_x.get())
hedefY = int(hedef_y.get())"""
master.title("Ajan")
gridX=24 #ızgara boyutunun X değeri
gridY=24 #ızgara boyutunun Y değeri
a={}
hold_on=False

engelAdet=((gridX+1)*(gridY+1))*30/100 #ızgaradaki engel sayısı ızgara sayısının %30'u olmalı.
yolAdet=((gridX+1)*(gridY+1))-engelAdet-2 #ızgaradaki yol sayısı = ızgara sayısı - engel sayısı - başlangıç - bitiş

"""ajanX=0 #Başlangıç konumunun X değeri tutulur.
ajanY=24 #Başlangıç konumunun Y değeri tutulur.
hedefX=0 #Bitiş(hedef) konumunun X değeri tutulur
hedefY=0 #Bitiş(hedef) konumunun Y değeri tutulur"""

yolX = [] #Yolların X konumlarını tutan dizi
yolY = [] #Yolların Y konumlarını tutan dizi
randomX = [] #Engellerin X konumlarını tutan dizi
randomY = [] #Engellerin Y konumlarını tutan dizi
success_score=[]
walk_count=[]
ajanX=0
ajanY=8
hedefX=8
hedefY=8
triangle_size = 0.1 #üçgenlerin boyutu
cell_score_min = -0.2 #üçgenlerin başlangıçtaki renklerini belirlemek için
cell_score_max = 0.2 
Width = 38 #kare boyutları
(x, y) = ((gridX+1), (gridY+1))#tablo boyutları
actions = ["up", "down", "left", "right","upleft","upright","downleft","downright"] #gidebileceği yönler
board = Canvas(master, width=x*Width, height=y*Width)
player = (ajanX, ajanY) #başlangıç konumu
score = 1 #skor başlangıçta 0
restart = False #yeniden oynama
walk_reward = -0.3 #her adım -0.04 maliyet ?

find_shortest_x=[]
find_shortest_y=[]

cost_scores=[]

matrisQ = [[0 for x in range(gridX+1)] for y in range(gridY+1)] #Q Matrisi başlangıçta ızgara boyutları belirtilerek iki boyutlu tanımlandı
matrisR = [[0 for x in range(gridX+1)] for y in range(gridY+1)] #R Matrisi başlangıçta ızgara boyutları belirtilerek iki boyutlu tanımlandı

specials = [] #engeller, random olacak !!!!!!!!!!!!!!!!!!! HEDEF NORMALDE 5 PUAN DÜZGÜN ÇALIŞMASI İÇİN ARTIRILDI
cell_scores = {} 
w_count=0
file = open("engel.txt","w") #Engel.txt dosyası oluşturuldu




def update_grid(aX,aY,hX,hY):
    #guncelle=False
    #if(guncelle==True):
    global ajanX,ajanY,hedefX,hedefY
    ajanX=aX
    ajanY=aY
    hedefX=hX
    hedefY=hY

def random_cell():
    count=0
    global specials, player
    specials=[(ajanX,ajanY, "#00D5D4",-1),(hedefX, hedefY, "#91EE75", 100)]
    file.write("("+str(ajanX)+","+str(ajanY)+",M)"+"\n") #kullanıcının seçtiği başlangıç noktası dosyaya yazıldı
    file.write("("+str(hedefX)+","+str(hedefY)+",Y)"+"\n") #kullanıcının seçtiği hedef noktası dosyaya yazıldı
    player = (ajanX, ajanY)
    while(count <  int(engelAdet)):
            randomX.append(randint(0, gridX)) #random olarak engellerin X noktaları belirlendi
            randomY.append(randint(0, gridY)) #random olarak engellerin Y noktaları belirlendi
            if(randomX[count]==ajanX and randomY[count]==ajanY): #random belirlenen ızgaranın başlangıç noktası ile aynı nokta olması durumu kontrol edildi, bu durumda eski değer silindi ve yeni bir random değer atandı
                print("Bu konum Mavi olmalı listeden ",randomX[count],",",randomY[count]," noktası çıkarıldı. Yeni liste: ",randomX, "\n",randomY)
                randomX.pop()
                randomY.pop()
                randomX.append(randint(0, gridX)) 
                randomY.append(randint(0, gridY))
                print("Mavi çıkarılmış liste güncel: \n",randomX,"\n",randomY)
            if(randomX[count]==hedefX and randomY[count]==hedefY): #random belirlenen ızgaranın hedef noktası ile aynı nokta olması durumu kontrol edildi, bu durumda eski değer silindi ve yeni bir random değer atandı
                print("Bu konum Yeşil olmalı listeden ",randomX[count],",",randomY[count]," noktası çıkarıldı. Yeni liste: ",randomX, "\n",randomY)
                randomX.pop()
                randomY.pop()
                randomX.append(randint(0, gridX)) 
                randomY.append(randint(0, gridY))
                print("Yeşil çıkarılmış liste güncel: \n",randomX,"\n",randomY)
            """if(randomX[count]==randomX[count2] and randomY[count] == randomY[count2]):
                print("Bu konum Kırmızı olmalı listeden ",randomX[count],",",randomY[count]," noktası çıkarıldı. Yeni liste: ",randomX, "\n",randomY)
                randomX.pop()
                randomY.pop()
                randomX.append(randint(0, 49)) 
                randomY.append(randint(0, 49))
                print("Kırmızı çıkarılmış liste güncel: \n",randomX,"\n",randomY)"""
            count=count+1
    for i in range(int(engelAdet)):
        specials.append((randomX[i],randomY[i],"red",-30))
    for i in range(int(engelAdet)): #Engel noktalarının konumları dosyaya yazdırıldı
            file.write("("+str(randomX[i])+","+str(randomY[i])+",K)"+"\n")

#random_cell()
def create_triangle(i, j, action): #üçgenleri oluşturuyor, 4 durumu da ekle
    if action == actions[0]:#up
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:#down
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:#left
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:#right
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[4]:#upleft
        return board.create_polygon((i+0.75)*Width, (j+0.25)*Width,
                                    (i+0.75)*Width, (j+0.25+triangle_size)*Width,
                                    (i+0.75)*Width, (j+0.75)*Width,
                                    fill="white", width=1)
    elif action == actions[5]:#upright
        return board.create_polygon((i+0.75-triangle_size)*Width, (j+0.25)*Width,
                                    (i+0.75)*Width, (j+0.25+triangle_size)*Width,
                                    (i+0.75)*Width, (j+0.25)*Width,
                                    fill="white", width=1)
    elif action == actions[6]:#downleft
        return board.create_polygon((i+0.25)*Width, (j+0.75-triangle_size)*Width,
                                    (i+0.25+triangle_size)*Width, (j+0.75)*Width,
                                    (i+0.25)*Width, (j+0.75)*Width,
                                    fill="white", width=1)
    elif action == actions[7]:#downright
        return board.create_polygon((i+0.75-triangle_size)*Width, (j+0.75-triangle_size)*Width,
                                    (i+0.75)*Width, (j+0.75)*Width,
                                    (i+0.75)*Width, (j+0.75)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, Width, x, y, player
    
    print("aaaaajjx: ",ajanX," aaajjy: ",ajanY, " hhhx: ",hedefX," hhhy: ",hedefY)
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
#render_grid()

def set_cell_score(state, action, val): #hareketler sonrası üçgen renkleri değişir
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):# konum değişir, (0,1)-(1,-1) gibi değerler gelir.
    global player, x, y, score, walk_reward, agent, restart,find_shortest_x,find_shortest_y, w_count

    new_x = player[0] + dx #yeni konum un X'i artık başlangıç konumu + gelen dx değeri
    new_y = player[1] + dy #yeni konum un Y'i artık başlangıç konumu + gelen dy değeri
    

    score += walk_reward #skor a adım atma maliyeti eklenir.
    
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y): #eğer grid dışında bi değer değilse
        board.coords(agent, new_x*Width+Width*3/10, new_y*Width+Width*3/10, new_x*Width+Width*7/10, new_y*Width+Width*7/10) #ajanın konumu buradaki gibi değişir.
        player = (new_x, new_y) #ajanın konumu artık budur
        find_shortest_x.append(new_x)
        find_shortest_y.append(new_y)
        w_count=w_count+1
    
    for (i, j, c, w) in specials: #w = maliyet, c=renk
        if new_x==i and new_y==j: #eğer şimdiki konuma geldiyse
            
            score -= walk_reward #hedefe geldiyse ya da engele çarptıysa eklenen adım maliyeti geri alınır.
            score += w
            walk_count.append(w_count)
            cost_scores.append(score)
            print("walk_count: ",walk_count)
            print("cost_scores: ",cost_scores)


            if new_x==hedefX and new_y==hedefY: #hedefe geldiyse
               # w_count=(len(find_shortest_x))
                """walk_count.append(len(find_shortest_x))
                min_walk=9999999
                for i in range(len(walk_count)):
                    if(int(walk_count[i])<min_walk):
                        min_walk=walk_count
                print("min_walk: ",min_walk)"""
                success_score.append(score)
                
                print ("Success! score: ", score, "adım sayısı: ",walk_count)
                success_len=len(success_score)
                print("boyut: ",success_len)
                if(success_len>5):
                    if(success_score[success_len-1]==success_score[success_len-2] and success_score[success_len-2]==success_score[success_len-3] and success_score[success_len-3]==success_score[success_len-4] and success_score[success_len-4]==success_score[success_len-5]):
                        print("ana yol bulundu!") #adım sayısına göre git lan
                        print("X: \n",find_shortest_x)
                        print("Y: \n",find_shortest_y)
                        for i in range(len(find_shortest_x)):
                            draw_route(find_shortest_x[i],find_shortest_y[i])
                            time.sleep(0.5)
                        draw_graphic(walk_count,cost_scores)
                        restart=False

                    else:
                        restart=True
            else:
                print ("Fail! score: ", score)
            restart = True #yeniden oyna
            
            return
    #print "score: ", score
    
    if restart == True:
        restart_game()

def draw_route(x,y):
        global gridX,gridY,restart
            # Aracıyı sonunda silme
        restart=False
        board.delete(agent)            
        board.create_oval(x*Width+Width*2/10, y*Width+Width*2/10,x*Width+Width*8/10, y*Width+Width*8/10, fill="yellow", width=1)
        


def  draw_graphic(steps,cost):
            #
        #plt.tight_layout()  # Rakamlar arasında mesafe bırakma işlevi

        plt.figure('Episode via steps Graphic')
        plt.plot(np.arange(len(steps)), steps, 'b')
        plt.title('Episode via steps')
        plt.xlabel('Episode')
        plt.ylabel('Steps')
        #
        plt.figure('Episode via cost Graphic')
        plt.plot(np.arange(len(cost)), cost, 'r')
        plt.title('Episode via cost')
        plt.xlabel('Episode')
        plt.ylabel('Cost')

        # Showing the plots
        plt.show()
      

def call_up(event): #yukarı çıkma komutu verilirse konumlara bu değerler eklenir.
    try_move(0, -1)

def call_down(event):
    try_move(0, 1)

def call_left(event):
    try_move(-1, 0)

def call_right(event):
    try_move(1, 0)

def call_upleft(event):
    try_move(-1, -1)

def call_upright(event):
    try_move(1, -1)

def call_downleft(event):
    try_move(-1, 1)

def call_downright(event):
    try_move(1, 1)


def restart_game():
    global player, score, agent, restart,find_shortest_x,find_shortest_y,walk_count,w_count
    w_count=0
    find_shortest_x.clear()
    find_shortest_y.clear()

    player = (ajanX,ajanY)
    score = 1
    restart = False
    board.coords(agent, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart
def bind_functions():
    master.bind("<Up>", call_up)
    master.bind("<Down>", call_down)
    master.bind("<Right>", call_right)
    master.bind("<Left>", call_left)
    master.bind("<Up><Left>", call_upleft)
    master.bind("<Down><Left>", call_downleft)
    master.bind("<Up><Right>", call_upright)
    master.bind("<Down><Right>", call_downright)
def render_continue():
    global agent
    agent = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                                player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="#FFB500", width=1, tag="agent")

    board.grid(row=0, column=0)
def final_states():
    return a

def start_game():
    master.mainloop()