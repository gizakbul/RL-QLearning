



#https://github.com/jalajthanaki/Q_learning_for_simple_atari_game 'dan uyarlanmıştır.


from tkinter import * #arayüz kütüphanesi
import tkinter as tk
from random import *
from numpy import *
import threading
import time

ajanX = 0
ajanY = 0
hedefX = 0
hedefY = 0

gridX=24 #ızgara boyutunun X değeri
gridY=24 #ızgara boyutunun Y değeri
s = "0-",gridX," Aralığında Bir Değer Giriniz!"

def degerAl():
    global ajanX,ajanY,hedefX,hedefY
    ajanX = int(baslangic_x.get())
    ajanY = int(baslangic_y.get())
    hedefX = int(hedef_x.get())
    hedefY = int(hedef_y.get())

    
    if ajanX>gridX or ajanY>gridY or hedefX>gridX or hedefY>gridY or ajanX<0 or ajanY<0 or hedefX<0 or hedefY<0: #kullanıcının ızgara boyutundan büyük ya da küçük bir başlangıç-bitiş noktası seçme durumu kontrol edildi
        print("0-",gridX," Aralığında Bir Değer Giriniz!")
        errorPage = tk.Tk()
        errorPage.title("ERROR!")
        errorPage.config(bg="#FF0000")
        frame = tk.Frame(master=errorPage)
        frame.pack()
        label = tk.Label(master=frame, text=s, font="Verdana 10",bg="#FF0000")
        label.pack()
    if(ajanX==hedefX and ajanY==hedefY): #kullanıcının başlangıç-bitiş noktasını aynı değer girme durumu kontrol edildi
        print("Başlangıç ve Bitiş Noktası Aynı Seçilemez!")
        errorPage = tk.Tk()
        errorPage.title("ERROR!")
        errorPage.config(bg="#FF0000")
        frame = tk.Frame(master=errorPage)
        frame.pack()
        label = tk.Label(master=frame, text="Başlangıç ve Bitiş Noktası Aynı Seçilemez!", font="Verdana 10",bg="#FF0000")
        label.pack()
        mainPage.mainloop()

    mainPage.destroy()


mainPage = Tk()
mainPage.title("User Interface")

canvas = Canvas(mainPage, height = 500 , width=800, bg="#0E363C")
canvas.pack()

frame_baslik = Frame(mainPage, bg = '#3A5A5F')
frame_baslik.place(relx=0.25 , rely=0.08 , relwidth=0.5 , relheight=0.13)

frame_ajan = Frame(mainPage , bg='#8C9194')
frame_ajan.place(relx=0.09, rely=0.28 , relwidth = 0.4 , relheight=0.55)

frame_hedef = Frame(mainPage , bg='#8C9194')
frame_hedef.place(relx=0.5, rely=0.28 , relwidth = 0.4 , relheight=0.55)

label_baslik = Label(frame_baslik , bg = '#3A5A5F' , text = "HOŞGELDİNİZ", font="Verdana 12 bold", fg='#FFFFFF')
label_baslik.place(relx=0.32,rely=0.3)

label_ajan_baslangic = Label(frame_ajan , bg='#8C9194' , text = "Ajanın Başlangıç Konumu:", font="Verdana 10 bold", fg='#D6F0FF')
label_ajan_baslangic.place(relx=0.1,rely=0.1)

label_ajan_baslangic_X = Label(frame_ajan , bg='#04D5B1' , text = "X Konumu:", font="Verdana 10 bold", fg='#D6F0FF')
label_ajan_baslangic_X.place(relx=0.1,rely=0.33)

label_ajan_baslangic_Y = Label(frame_ajan , bg='#04D5B1' , text = "Y Konumu:", font="Verdana 10 bold", fg='#D6F0FF')
label_ajan_baslangic_Y.place(relx=0.1,rely=0.6)

label_hedef = Label(frame_hedef , bg='#8C9194' , text = "Hedef Konumu:", font="Verdana 10 bold", fg='#D6F0FF')
label_hedef.place(relx=0.1,rely=0.1)

label_hedef_X = Label(frame_hedef , bg='#04D5B1' , text = "X Konumu:", font="Verdana 10 bold", fg='#D6F0FF')
label_hedef_X.place(relx=0.1,rely=0.33)

label_hedef_Y = Label(frame_hedef , bg='#04D5B1' , text = "Y Konumu:", font="Verdana 10 bold", fg='#D6F0FF')
label_hedef_Y.place(relx=0.1,rely=0.6)

baslangic_x = Spinbox(font="Verdana 11", from_=0, to=gridX , width=10, bg="#FBE6D0", fg="#FF8300")
baslangic_x.place(relx=0.27,rely=0.46)

baslangic_y = Spinbox(font="Verdana 11", from_=0, to=gridY , width=10, bg="#FBE6D0", fg="#FF8300")
baslangic_y.place(relx=0.27,rely=0.61)

hedef_x = Spinbox(font="Verdana 11", from_=0, to=gridX , width=10, bg="#FBE6D0", fg="#FF8300")
hedef_x.place(relx=0.68,rely=0.46)

hedef_y = Spinbox(font="Verdana 11", from_=0, to=gridY , width=10, bg="#FBE6D0", fg="#FF8300")
hedef_y.place(relx=0.68,rely=0.61)

devam_buton = Button(canvas,text="Devam Et" ,font="Verdana 12", bg="#FF8300",fg="#FFFFFF",command=degerAl)
devam_buton.place(relx=0.426, rely=0.85)

mainPage.mainloop()

import World


time.sleep(0.1)
World.ajanX = ajanX
World.ajanY = ajanY
World.hedefX = hedefX
World.hedefY = hedefY

print("ajanx: ",World.ajanX," ajany: ",World.ajanY," hedefx: ",World.hedefX," hedefy: ",World.hedefY)
World.update_grid(ajanX,ajanY,hedefX,hedefY) #World sayfasına kullanıcının seçtiği değerler gönderildi
World.random_cell() #random engel değerleri oluşturuldu ve başlangıç-bitiş noktaları güncellendi
World.render_grid() #grid ekrana güncel değerlerle basıldı
World.bind_functions() #ajanın hareketleri
World.render_continue() #ajanın özellikleri
World.file.close()

indirim_faktoru = 0.9 
actions = World.actions #yukarı,aşağı,sağ,sol,sağ alt, sol alt, sağ üst, sol üst değerleri action değişkeni içinde tutulur
states = [] #durumları tutar
Q = {} #Q matrisibaşta boş verilir
#print("Q Matrisi: \n",Q)


for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))
#print("States: \n",states)

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp
    #print(Q)
#print("Q Matrisi: \n",Q)

for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w #geldiği konma hangi yönden geldiğini ve geldiğinde kaç puan aldığını ekler.
        #print(Q)
        World.set_cell_score((i, j), action, w)
        #print("i: ",i," j: ",j," action: ",action," w: ",w)
        

def do_action(action):
    s = World.player #ilk durumu
    r = -World.score #ödül durumu
    if action == actions[3]:
        #print("Sağ")
        World.try_move(1, 0)
    elif action == actions[1]:
        #print("Aşağı")
        World.try_move(0, 1)
    elif action == actions[2]:
        #print("Sol")
        World.try_move(-1, 0)
    elif action == actions[0]:
        #print("Yukarı")
        World.try_move(0, -1)
    elif action == actions[4]:
        #print("sol üst")
        World.try_move(-1, -1)
    elif action == actions[5]:
        #print("sağ üst")
        World.try_move(1, -1)
    elif action == actions[6]:
        #print("sol alt")
        World.try_move(-1, 1)
    elif action == actions[7]:
        #print("sağ alt")
        World.try_move(1, 1)
    else:
        return
    s2 = World.player #hareket ettikten sonraki konumu yeni duruma atılır
    r += World.score #r=reward , skor ödül değerine eklenir
    return s, action, r, s2 #ilk durum, eylemi, aldığı ödül, yeni durum döndürülür.


def max_Q(s):
    val = None #değer
    act = None #hareket
    for a, q in Q[s].items(): #Q[s].items() başlangıç noktasına her döndüğünde kaç puanla döndüğünü tutar
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha #s, şimdiki durum, a, hareketler, Q(s,a) değeri sıfılanır
    Q[s][a] += alpha * inc #s durumundan s2 durumuna geçtiğindeki anlık kazancını tutar
    World.set_cell_score(s, a, Q[s][a])


def run():
    global indirim_faktoru
    time.sleep(0.000000000000000000000000000000000000001)
    alpha = 1
    t = 1
    while (True):
        # Doğru eylemi seçin
        s = World.player #ilk konum, ajanın konumu olarak belirlenir.
        max_act, max_val = max_Q(s) #maxQ fonk dan dönen act değeri max_act'da, val değeri max_val da tutulur
        (s, a, r, s2) = do_action(max_act) #ajan hareket eder

        # Q güncelleme
        max_act, max_val = max_Q(s2) #yeni durum için maxQ fonk dan dönen act değeri max_act'da, val değeri max_val da tutulur
        inc_Q(s, a, alpha, r + indirim_faktoru * max_val) #Q(s,a) = R(s,a)+indirim_faktörü*max(Q(tüm durumlar,tüm hareketler)) Q LEARNING'IN ASIL FORMULÜ OLAN BU İŞLEM BURADA GERÇEKLEŞİR
        #print("SONUÇ: ",(r + indirim_faktoru * max_val))

        # Oyunun yeniden başlayıp başlamadığını kontrol edin
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.000000000000000000000000000000000000000000000001)
            t = 1.0
        alpha = pow(t, -0.1)

        time.sleep(0.0000000000000000000000000000000000000000001)
    #World.draw_graphic(World.walk_count,World.cost_scores)



t = threading.Thread(target=run)
t.setDaemon = True
t.start()

time.sleep(0.1)
World.start_game()



