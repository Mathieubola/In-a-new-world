from tkinter import *
import random,time,math

autor='Mathieubl, Julien, Nelson'
version='0.6.0'

fen=Tk()
fen.geometry('1000x440')
fen.title('*-* In a new world *-*')
img_icon = PhotoImage(file='Ressource\Image\Icon.png')
fen.tk.call('wm', 'iconphoto', fen._w, img_icon)
can=Canvas(fen,width=1000,height=440,bg='black')
can.pack()

#Fonctions personnage

#Generation du monde

def generate():
    global decor,dimention,xdim,ydim,item,hight
    #Ouverture et lecture de la map
    FIC=open('Ressource\Map\\'+dimention+'-'+str(xdim)+'-'+str(ydim),'r')
    CTN=FIC.read().split('\n')
    FIC.close()
    #Analyse des onze premières lignes (de 0 a 10) qui deffinissent la texture des décore du tableau
    for MY in range(11):
        M2=CTN[MY].split(',')
        for MX in range(25):
            M=M2[MX]
            if M=='Arbre mort':
                decor.append(can.create_image(MX*40,MY*40,image=img_arbre_mort,anchor=NW))
            elif M=='Herbe mort':
                decor.append(can.create_image(MX*40,MY*40,image=img_herbe_mort,anchor=NW))
            elif M=='Tombe':
                decor.append(can.create_image(MX*40,MY*40,image=img_tombe,anchor=NW))
            elif M=='Stone bric':
                decor.append(can.create_image(MX*40,MY*40,image=img_stone_brick,anchor=NW))        
    #Analyse des ligne 12 à 22 qui deffinissent le relief du tableau
    hight=[]
    for i in range(12,23):
        hight.append(CTN[i].split(','))
    #Analyse de la ligne 24 à la dernière qui definissent les monstres à faire apparraitre
    if len(CTN)>=24:
        for i in range(24,len(CTN)):
            DATA=CTN[i].split(',')
            if DATA[0]=='Pendu':
                SKIN=img_Pendu
            elif DATA[0]=='Chatz':
                SKIN=img_chatz
            elif DATA[0]=='Fantome':
                SKIN=img_fantome
            ##Fonctions:(skin,coord_x,coord_y,attaque,point de vie,vitesse) correspond aux "DATA[]" dans l'ordre
            ia_mob(SKIN,int(DATA[1]),int(DATA[2]),int(DATA[3]),int(DATA[4]),int(DATA[5]),[xdim,ydim])
    #Affichage du personnage principale
    can.delete(item[0])
    if direction=='Droite':
        item[0]=can.create_image(xco,yco,image=hero[0][0])
    else:
        item[0]=can.create_image(xco,yco,image=hero[1][0])

#Fonction de destruction de la carte pour ensuite afficher un menu
def ungenerate():
    global decor
    for i in decor:
        can.delete(i)
    decor=[]

#Fonction permettant d'afficher la vie restante du personnage
def lifemonitor(ITEM1=0,ITEM2=0):
    if ITEM1!=0 and ITEM2!=0:
        can.delete(ITEM1,ITEM2)
    ITEM1=can.create_rectangle(9,9,111,21,fill='Black')
    ITEM2=can.create_rectangle(10,10,10+vie*100/viemax,20,fill='red')
    if etat=='Jeu':
        fen.after(100,lifemonitor,ITEM1,ITEM2)
    else:
        can.delete(ITEM1,ITEM2)

#Fonction permettant de régénérer les points de vie du personnage
def regen():
    global vie
    if vie+rege<=viemax:
        vie+=rege
    else:
        vie=viemax
    if etat=='Jeu':
        fen.after(1000,regen)

#Fonction compte

#Fonction permettant d'enrigistrer un nouveau personnage
def register(PSEUDO):
    #Ouverture du fichier joueur et ajout du joueur avec les compétence de base
    FIC=open('Ressource\Joueur','a')
    FIC.write(PSEUDO+',500,250,Overworld,0,0,100,100,1,0\n')
    FIC.close()

#Fonction permettant de charger la sauvegarde en tapant son pseudonyme
def login(PSEUDO):
    global xco,yco,dimention,xdim,ydim,vie,viemax,attak,rege
    #Ouverture du fichier joueur
    FIC=open('Ressource\Joueur','r')
    CTN=FIC.read().split('\n')
    FIC.close()
    #Recherche de la sauvegarde du joueur
    for i in range(len(CTN)-1):
        DATA=CTN[i].split(',')
        if DATA[0]==PSEUDO:
            #Enregistrement des compétence dans le programe
            xco,yco=int(DATA[1]),int(DATA[2])
            dimention,xdim,ydim=DATA[3],int(DATA[4]),int(DATA[5])
            vie,viemax,attak,rege=int(DATA[6]),int(DATA[7]),int(DATA[8]),int(DATA[9])
            break

#Fonction permettant de sauvegarder la partie en cours
def save(PSEUDO):
    global xco,yco,dimention,xdim,ydim,pseudo
    #Ouverture du fichier joueur
    FIC=open('Ressource\Joueur','r')
    DATA=FIC.read().split('\n')
    FIC.close()
    MATRICE=[]
    for i in range(len(DATA)-1):
        MATRICE.append(DATA[i].split(','))
    #Recherche de la sauvegarde du joueur
    for i in range(len(DATA)-1):
        if MATRICE[i][0]==pseudo:
            #Enregistrement des compétence dans le fichier joueur
            MATRICE[i][1],MATRICE[i][2]=xco,yco
            MATRICE[i][3],MATRICE[i][4],MATRICE[i][5]=dimention,xdim,ydim
            MATRICE[i][6],MATRICE[i][7],MATRICE[i][8],MATRICE[i][9]=vie,viemax,attak,rege
            FIC=open('Ressource\Joueur','w')
            for i in range(len(MATRICE)):
                FIC.write(str(MATRICE[i][0])+','+str(MATRICE[i][1])+','+str(MATRICE[i][2])+','+str(MATRICE[i][3])+','+str(MATRICE[i][4])+','+str(MATRICE[i][5])+','+str(MATRICE[i][6])+','+str(MATRICE[i][7])+','+str(MATRICE[i][8])+','+str(MATRICE[i][9])+'\n')
            FIC.close()
            break

#Intelligences Artificielles

#Fonction permettant de définir les habilités du personnage
def personage(X,Y,FRAME=0,MIND=0):
    global x,y,direction,item,xdim,ydim,dimention,hero,xco,yco
    if direction=='Gauche':
        TOP=1
    else:
        TOP=0
    FRAME+=0.2
    if FRAME>=3 or ( attaque==1 and MIND==0 ):
        FRAME=0
    if attaque==1 and MIND==0:
        MIND=1
    elif attaque==0 and MIND==1:
        MIND=0
    if attaque==1:
        TOP+=2
    can.delete(item[0])
    item[0]=can.create_image(X,Y,image=hero[TOP][int(FRAME)])
    xco,yco=X,Y
    if x!=0:
        if x<0 and direction!='Gauche':
            direction='Gauche'
        elif x>0 and direction!='Droite':
            direction='Droite'
        #Hit Box
        if int(x+X+12)/40>25 or int(x+X-12)<0:
            X+=x
        elif (hight[int((Y+20)/40)][int((X+x+12)/40)]<=hight[int(Y/40)][int(X/40)] and
            hight[int((Y+20)/40)][int((X+x-12)/40)]<=hight[int(Y/40)][int(X/40)] and
            hight[int(Y/40)][int((X+x+12)/40)]<=hight[int(Y/40)][int(X/40)] and
            hight[int(Y/40)][int((X+x-12)/40)]<=hight[int(Y/40)][int(X/40)]):
            X+=x
        #Déplacement horizontal
        if X<20:
            X=xco=980
            xdim-=1
            ungenerate()
            generate()
        elif X>980:
            X=xco=20
            xdim+=1
            ungenerate()
            generate()
    if y!=0:
        #Hit box
        if int((y+Y+20)/40)>10 or int((Y+y)/40)<0:
            Y+=y
        elif (hight[int((Y+y+20)/40)][int((X+12)/40)]<=hight[int(Y/40)][int(X/40)] and
            hight[int((Y+y+20)/40)][int((X-12)/40)]<=hight[int(Y/40)][int(X/40)] and
            hight[int((Y+y)/40)][int((X+12)/40)]<=hight[int(Y/40)][int(X/40)] and
            hight[int((Y+y)/40)][int((X-12)/40)]<=hight[int(Y/40)][int(X/40)]):
            Y+=y
        #Déplacement vertical
        if Y<20:
            Y=yco=370
            ydim-=1
            ungenerate()
            generate()
        elif Y>370:
            Y=yco=20
            ydim+=1
            ungenerate()
            generate()      
    if x!=0 or y!=0:
        can.coords(item[0],X,Y)
    if vie<=0:
        gameover()
    if etat=='Jeu':
        fen.after(50,personage,X,Y,FRAME,MIND)
    else:
        can.delete(item[0])

#Fonction permettant de définir les habilités du personnage
def ia_mob(SKIN,X,Y,ATT,DEF,VIT,CODIM,MOB=0,FRAME=0):
    global vie,viemax,attak,rege
    STUN=100
    #Création de la texture du monstre
    if MOB==0:
        MOB=can.create_image(X,Y,image=SKIN[0][0])
    #Détermination de la position du joueur par rapport au monstre
    if math.sqrt((X-xco)*(X-xco)+(Y-yco)*(Y-yco))!=0:
        A=-math.asin((Y-yco)/math.sqrt((X-xco)*(X-xco)+(Y-yco)*(Y-yco)))
    else:
        if Y-yco<0:
            A=-math.pi/2
        else:
            A=math.pi/2
    if X-xco>0:
        A+=math.pi
    #Progression de l'annimation du monstre
    FRAME+=1
    if FRAME>len(SKIN[0])-1:
        FRAME=0
    #Détermination de la direction du monstre
    if X-xco<0:
        B=0
    else:
        B=1
    #Mise à jour de la texture du monstre
    can.delete(MOB)
    MOB=can.create_image(X,Y,image=SKIN[B][FRAME])
    #Déplacement du monstre
    if math.sqrt((X-xco)*(X-xco)+(Y-yco)*(Y-yco))>60:
        X+=math.cos(A)*VIT
        if X-xco>0:
            Y-=math.sin(A)*VIT
        else:
            Y+=math.sin(A)*VIT
    else:
        #Attaque du joueur si le monstre est assez près
        vie-=ATT
        X-=30*math.cos(A)
        Y-=30*math.sin(A)
        STUN=1000
        can.coords(MOB,X,Y)
    if math.sqrt((X-xco)*(X-xco)+(Y-yco)*(Y-yco))<80 and attaque==1:
        X-=30*math.cos(A)
        Y-=30*math.sin(A)
        STUN=200
        DEF-=attak
    #augmentation des habilités du personnage si un monstre est vaincu
    if xdim==CODIM[0] and ydim==CODIM[1] and etat=='Jeu' and DEF>0:
        fen.after(STUN,ia_mob,SKIN,X,Y,ATT,DEF,VIT,CODIM,MOB,FRAME)
    elif DEF<=0:
        can.delete(MOB)
        attak+=1
        vie+=5
        viemax+=1
        rege+=1
        if vie>viemax:
            vie=viemax
        if SKIN==img_fantome:
            game_over()
    else:
        #Suppression de la texture du mob
        can.delete(MOB)
    
#Fonction état

#Fonction permettant de lancer le jeu
def Jeu(SUPP=0):
    global etat,item,barre,xco,yco,x,y
    if SUPP!=0:
        etatreset()
    #Changement de l'etat en Jeu, création de la texture du héro,
    #génération  du monde, affichage de la vie, lancement de la regeneration et du héro
    etat='Jeu'
    item.append(can.create_image(xco,yco,image=hero[0][0]))
    generate()
    lifemonitor()
    regen()
    personage(xco,yco)
    x=y=0

#Fonction permettant d'afficher le menu
def Menu(SUPP=0,ETATLOC=0,OBJ=[0,0],X=900,PAS=1,ETATIMG=[1,0,0]):
    global etat,item
    if SUPP!=0:
        etatreset()
    
    if ETATLOC==0:
        for i in item:
            can.delete(i)
        item=[]
        etat='Menu'
        ETATLOC=1
        OBJ=[]
        OBJ.append(can.create_image(X,250,image=img_fond_ecran))
        OBJ.append(can.create_image(X,750,image=img_fond_ecran2))
        OBJ.append(250)
        OBJ.append(750)
        item.append(can.create_text(500,75,text='In a new world',font='Arial 105',fill='Black'))
        item.append(can.create_text(500,75,text='In a new world',font='Arial 100',fill='Dark grey'))
        item.append(can.create_rectangle(80,135,920,142,fill='Black'))
        item.append(can.create_rectangle(90,130,910,137,fill='Dark grey',width=0))
        item.append(can.create_rectangle(240,265,760,325,fill='Black'))
        item.append(can.create_rectangle(250,260,750,320,fill='Dark grey',width=3))
        item.append(can.create_text(500,290,text='Singleplayer',font='Arial 25',fill='Black'))
        item.append(can.create_rectangle(240,370,470,430,fill='Black'))
        item.append(can.create_rectangle(250,360,475,420,fill='Dark grey',width=3))
        item.append(can.create_text(362.5,390,text='Options',font='Arial 25',fill='Black'))
        item.append(can.create_rectangle(760,370,530,430,fill='Black'))
        item.append(can.create_rectangle(750,360,525,420,fill='Dark grey',width=3))
        item.append(can.create_text(637.5,390,text='Quit Game',font='Arial 25',fill='Black'))
        item.append(can.create_text(10,420,text='Autor : '+str(autor),font='Arial 7',fill='Black',anchor=W))
        item.append(can.create_text(10,430,text='Version : '+str(version),font='Arial 7',fill='Black',anchor=W))        
        fen.after(10,Menu,0,ETATLOC,OBJ)
    else:
        X-=PAS
        can.coords(OBJ[0],X,OBJ[2])
        can.coords(OBJ[1],X,OBJ[3])        
        ETATIMG[1]+=1
        if ETATIMG[0]==ETATIMG[1]:
            if ETATIMG[2]==0:
                ETATIMG[2]=1
                ETATIMG[0]=random.randint(2,10)
                OBJ[2],OBJ[3]=OBJ[3],OBJ[2]
            elif ETATIMG[2]==1:
                ETATIMG[2]=0
                ETATIMG[0]=random.randint(50,100)
                OBJ[2],OBJ[3]=OBJ[3],OBJ[2]
            ETATIMG[1]=0
        if X<100:
            PAS-=0.02
        elif X>900:
            PAS+=0.02
        if etat=='Menu':
            fen.after(50,Menu,0,ETATLOC,OBJ,X,PAS,ETATIMG)
        else:
            can.delete(OBJ[0],OBJ[1])

#Fonction permettant d'afficher le menu des options
def Option(SUPP=0):
    global etat,item
    if SUPP!=0:
        etatreset()
    etat='Option'
    for i in range(-500,1000,25):
        item.append(can.create_line(i,0,i+500,500,fill='Grey'))
    if up==['Up']:
        item.append(can.create_rectangle(289.5,412.5,43.5,247.5,fill='Black',width=10,outline='White'))
    elif up==['z','Z']:
        item.append(can.create_rectangle(368,412.5,632.5,247.5,fill='Black',width=10,outline='White'))
    elif up==['w','W']:
        item.append(can.create_rectangle(700.5,412.5,964,247.5,fill='Black',width=10,outline='White'))
    item.append(can.create_text(500,75,text='O P T I O N',font='Arial 105',fill='Black'))
    item.append(can.create_text(500,75,text='O P T I O N',font='Arial 100',fill='Dark grey'))
    item.append(can.create_text(500,160,text='Attaque : Left Click',font='Arial 40',fill='Dark grey'))
    item.append(can.create_text(100,20,text='Sortir : Echap',font='Arial 20',fill='Dark grey'))
    item.append(can.create_rectangle(50,205,950,215,fill='Dark grey'))
    item.append(can.create_image(166.5,330,image=img_touchpad_arrow))
    item.append(can.create_image(500,330,image=img_touchpad_azerty))
    item.append(can.create_image(832.5,330,image=img_touchpad_qwerty))

#Fonction permettant d'afficher le menu de fin de jeu
def game_over():
    global etat,item
    ungenerate()
    etat='Game over'
    for i in item:
        can.delete(item)
    item=[]
    for i in range(-500,1000,25):
        item.append(can.create_line(i,0,i+500,500,fill='Grey'))
    item.append(can.create_text(500,75,text='G A M E   O V E R',font='Arial 90',fill='dark red'))
    item.append(can.create_text(500,75,text='G A M E   O V E R',font='Arial 85',fill='red'))
    item.append(can.create_text(100,20,text='Sortir : Echap',font='Arial 20',fill='Dark grey'))
    item.append(can.create_rectangle(200,300,400,400,fill='red'))
    item.append(can.create_rectangle(800,300,600,400,fill='red'))
    item.append(can.create_text(700,350,text='quit',font='arial 30',fill='black'))
    item.append(can.create_text(300,350,text='restart',font='arial 30',fill='black'))
    item.append(can.create_rectangle(50,205,950,215,fill='Dark grey'))

#Fonction permettant de sélectionner son personnage
def Selection(SUPP=0):
    global etat,item,inputpseudo
    if SUPP!=0:
        etatreset()
    #Changement de l'etat en Sélection et affichage du menu
    etat='Selection'
    item.append(can.create_rectangle(300,50,700,410,fill='Grey'))
    item.append(can.create_text(500,100,text='Choose your heroe',font='Arial 30',fill='Black'))
    item.append(can.create_text(500,150,text='name',font='Arial 30',fill='Black'))
    item.append(can.create_rectangle(400,310,600,385,fill='Black'))
    item.append(can.create_text(500,347.5,text='Jouer',font='Arial 30',fill='Grey'))
    for i in range(-500,1000,25):
        item.append(can.create_line(i,0,i+500,540,fill='Grey'))
    item.append(can.create_rectangle(325,200,675,275,fill='Black'))
    inputpseudo=can.create_text(500,237.5,text='',font='Arial 30',fill='Grey')

#fonction affichant si nécessaire une fenêtre de chargement
def Chargement(TOLAUNCH,SUPP=0,ETATLOC=0):
    global etat,item,iastop
    if ETATLOC==0:
        etat='Charg'
        fen.after(1,Chargement,TOLAUNCH,SUPP,can.create_text(990,430,text='Loading ...',font='Arial 50',fill='White',anchor=SE))
    else:
        if SUPP!=0:
            etatreset()
        if TOLAUNCH=='Jeu':
            Jeu()
        elif TOLAUNCH=='Menu':
            Menu()
        elif TOLAUNCH=='Option':
            Option()
        elif TOLAUNCH=='Selection':
            Selection()
        can.delete(ETATLOC)

#Fonction permettant de définir l'état de fin de jeu
def gameover(TEMP=0):
    global etat,item
    if TEMP==0:
        etatreset()
        ungenerate()
        etat='GameOver'
        TEMP=[]
        TEMP.append(can.create_text(500,220,text='GAME OVER',font='Arial 100',fill='Red'))
        TEMP.append(can.create_text(500,320,text='La partie va recomencer a partir de la derniere sauvegarde',font='Arial 20',fill='Red'))
        fen.after(1000,gameover,TEMP)
    else:
        can.delete(TEMP[0],TEMP[1])
        login(pseudo)
        Jeu()

#Fonction permettant de supprimer les objets actuellement présents sur la carte
def etatreset():
    global item,etat
    for i in item:
        can.delete(i)
    item=[]
    etat='None'

#Fonction s'executant une seconde après l'attaque du personnage et arrêtant l'attaque
def unattak():
    global attaque
    attaque=0

#Fonctions d'entrées

#Fonction permettant de créer dess boutons virtuels dans les différents menus
def key(event):
    T=event.keysym
    if T=='Delete':
        print(xco,yco)
    if etat=='Jeu':
        keyjeu(T)
    elif etat=='Menu':
        keymenu(T)
    elif etat=='Option':
        keyoption(T)
    elif etat=='Selection':
        keyselection(T)
    elif etat=='Game over':
        keyselection(T)

#Fonction permettant d'associer une touche à une action dans le jeu
def keyjeu(T):
    global speak,x,y,vitesse
    #en fonction de la touche directionnelle appuier, demander au héro de ce déplacer
    if T in right:
        x=vitesse
    elif T in left:
        x=-vitesse
    elif T in up:
        y=-vitesse
    elif T in down:
        y=vitesse
    #Si le joueur jeu quiter, on efface le monde et on l'envoie au menu
    elif T=='Escape' or T=='Delete':
        ungenerate()
        Chargement('Menu',1)
    #Si le joueur veut taper, demander au héro de ce déplacer
    elif T=='Return' or T=='Space':
        attaque=1
        fen.after(1000,unattak)

#Fonction permettant d'associer une touche à une action dans le menu
def keymenu(T):
    global item
    if T=='Return':
        for i in range(15):
            can.delete(item[0])
            del item[0]
        Chargement('Jeu',1)
    elif T=='Escape':
        save(pseudo)
        fen.destroy()

#Fonction permettant d'associer une touche à une action dans les options
def keyoption(T):
    if T=='Escape':
        Chargement('Menu',1)

#Fonction permettant d'intégrer les différentes touches au programme
def keyselection(T):
    global pseudo,inputpseudo
    CARACTERE=['minus','underscore','space']
    CARACTEREB=['-','_',' ']
    #Si la touche appuier est une lettre alors on l'ajoure au pseudo
    if T in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        pseudo.append(T)
    #Si c'est une caractere spécial, alors on ajoute le caractere corespondant
    elif T in CARACTERE:
        pseudo.append(CARACTEREB[CARACTERE.index(T)])
    #Si l'utilisateur veut supprimer la derniere lettre alors on le fait
    elif T=='BackSpace' and len(pseudo)>0:
        del pseudo[len(pseudo)-1]
    can.delete(inputpseudo)
    inputpseudo=can.create_text(500,237.5,text=str(''.join(pseudo)),font='Arial 30',fill='Grey')
    #Si le joueur veut partir alors on ferme la page
    if T=='Escape':
        fen.destroy()
    #Si j'utilisateur a finit de taper sont pseudo alors on regarde si le pseudo existe pour le charger, si non on crée un nouveau compte
    elif T=='Return':
        MATRICE=[]
        FIC=open('Ressource\Joueur','r')
        CTN=FIC.read().split('\n')
        FIC.close()
        can.delete(inputpseudo)
        pseudo=''.join(pseudo)
        for i in range(len(CTN)):
            if pseudo==CTN[i].split(',')[0]:
                login(pseudo)
                break
            elif i==len(CTN)-1:
                register(pseudo)
        Chargement('Menu',1)

#fonction 
def unkey(event):
    t=event.keysym
    if etat=='Jeu':
        unkeyjeu(t)


def unkeyjeu(T):
    global x,y
    if T in right or T in left:
        x=0
    elif T in up or T in down:
        y=0

#Fonction permettant d'intégrer la fonctionnalité du clique souris
def click(event):
    X,Y=event.x,event.y
    if etat=='Jeu':
        clickjeu(X,Y)
    elif etat=='Menu':
        clickmenu(X,Y)
    elif etat=='Option':
        clickoption(X,Y)
    elif etat=='Selection':
        clickselection(X,Y)
    elif etat=='Game over':
        clickgameover(X,Y)

#Fonction utilisant le clique souris dans le jeu
def clickjeu(X,Y):
    global attaque
    #Si le joueur veut attaquer et qu'il attaque pas déja, on demande au héro d'attaquer
    if attaque==0:
        attaque=1
        fen.after(1000,unattak)

#Fonction utilisant le clique souris dans le menu
def clickmenu(X,Y):
    global pseudo
    if X>250 and X<750 and Y>260 and Y<320:
        Chargement('Jeu',1)
    elif X>250 and X<475 and Y>360 and Y<420:
        Chargement('Option',1)
    elif X>525 and X<750 and Y>360 and Y<420:
        save(pseudo)
        fen.destroy()

#Fonction utilisant le clique souris dans les options
def clickoption(X,Y):
    global up,down,left,right
    if X<289.5 and X>43.5 and Y<412.5 and Y>247.5:
        up,down,left,right=['Up'],['Down'],['Left'],['Right']
        Option(1)
    elif X<632.5 and X>368 and Y<412.5 and Y>247.5:
        up,down,left,right=['z','Z'],['s','S'],['q','Q'],['d','D']
        Option(1)
    elif X<964 and X>700.5 and Y<412.5 and Y>247.5:
        up,down,left,right=['w','W'],['s','S'],['a','A'],['d','D']
        Option(1)

#Fonction utilisant le clique souris dans le menu de sélection du personnage
def clickselection(X,Y):
    global pseudo
    #Si j'utilisateur a finit de taper sont pseudo alors on regarde si le pseudo existe pour le charger, si non on crée un nouveau compte
    if X<600 and X>400 and Y<385 and Y>310:
        MATRICE=[]
        FIC=open('Ressource\Joueur','r')
        CTN=FIC.read().split('\n')
        FIC.close()
        can.delete(inputpseudo)
        pseudo=''.join(pseudo)
        for i in range(len(CTN)):
            if pseudo==CTN[i].split(',')[0]:
                login(pseudo)
                break
            elif i==len(CTN)-1:
                register(pseudo)
        Chargement('Menu',1)

#Fonction utilisant le clique souris dans le menu de fin de jeu
def clickgameover(X,Y):
    global pseudo
    if X<400 and X>200 and Y<400 and Y>300:
        dimention,xdim,ydim='Overworld',0,0
        vie,viemax,attak,rege=100,100,1,0
        save(pseudo)
        login(pseudo)
        Menu()
    elif X<800 and X>600 and Y<400 and Y>300:
        dimention,xdim,ydim='Overworld',0,0
        save(pseudo)
        fen.destroy()

#Fonction permettant d'afficher une animation lors du survol d'une case spécifique
def survol(event):
    X,Y=event.x,event.y
    if etat=='Menu':
        survolmenu(X,Y)

#Fonction appliquant la fonction "survol" au menu
def survolmenu(X,Y):
    global item,variabletemporaire
    if variabletemporaire==1:
        can.delete(item[5])
        can.delete(item[6])
        item[5]=can.create_rectangle(250,260,750,320,fill='Dark Grey',width=3)
        item[6]=can.create_text(500,290,text='Singleplayer',font='Arial 25',fill='Black')
    elif variabletemporaire==2:
        can.delete(item[8])
        can.delete(item[9])
        item[8]=can.create_rectangle(250,360,475,420,fill='Dark Grey',width=3)
        item[9]=can.create_text(362.5,390,text='Options',font='Arial 25',fill='Black')
    elif variabletemporaire==3:
        can.delete(item[11])
        can.delete(item[12])
        item[11]=can.create_rectangle(750,360,525,420,fill='Dark Grey',width=3)
        item[12]=can.create_text(637.5,390,text='Quit Game',font='Arial 25',fill='Black')
    if X>250 and X<750 and Y>260 and Y<320:
        variabletemporaire=1
        can.delete(item[5])
        can.delete(item[6])
        item[5]=can.create_rectangle(250,260,750,320,fill='Black',width=3,outline='Dark Grey')
        item[6]=can.create_text(500,290,text='Singleplayer',font='Arial 25',fill='Dark Grey')
    elif X>250 and X<475 and Y>360 and Y<420:
        variabletemporaire=2
        can.delete(item[8])
        can.delete(item[9])
        item[8]=can.create_rectangle(250,360,475,420,fill='Black',width=3,outline='Dark Grey')
        item[9]=can.create_text(362.5,390,text='Options',font='Arial 25',fill='Dark Grey')
    elif X>525 and X<750 and Y>360 and Y<420:
        variabletemporaire=3
        can.delete(item[11])
        can.delete(item[12])
        item[11]=can.create_rectangle(750,360,525,420,fill='Black',width=3,outline='Dark Grey')
        item[12]=can.create_text(637.5,390,text='Quit Game',font='Arial 25',fill='Dark Grey')
    else:
        variabletemporaire=0

#Variables

xco,yco=250,220
x=y=0
vitesse=10
attaque=0
dimention,xdim,ydim='Overworld',0,0
vie,viemax,attak,rege=100,100,1,0
variabletemporaire=0
direction='Droite'
etat='None'
decor,item,pseudo=[],[],[]
up,down,left,right=['z','Z'],['s','S'],['q','Q'],['d','D']

#Images hero

hero=[[],[],[],[]]
hero[0].append(PhotoImage(file='Ressource\Image\herod 1.png'))
hero[0].append(PhotoImage(file='Ressource\Image\herod 2.png'))
hero[0].append(PhotoImage(file='Ressource\Image\herod 3.png'))
hero[1].append(PhotoImage(file='Ressource\Image\herog 1.png'))
hero[1].append(PhotoImage(file='Ressource\Image\herog 2.png'))
hero[1].append(PhotoImage(file='Ressource\Image\herog 3.png'))
hero[2].append(PhotoImage(file='Ressource\Image\herod attack 1.png'))
hero[2].append(PhotoImage(file='Ressource\Image\herod attack 2.png'))
hero[2].append(PhotoImage(file='Ressource\Image\herod attack 3.png'))
hero[3].append(PhotoImage(file='Ressource\Image\herog attack 1.png'))
hero[3].append(PhotoImage(file='Ressource\Image\herog attack 2.png'))
hero[3].append(PhotoImage(file='Ressource\Image\herog attack 3.png'))

#Images Monstres

#Pendu
img_Pendu=[[],[]]
img_Pendu[0].append(PhotoImage(file='Ressource\Image\Pendu 1.png'))
img_Pendu[0].append(PhotoImage(file='Ressource\Image\Pendu 2.png'))
img_Pendu[0].append(PhotoImage(file='Ressource\Image\Pendu 3.png'))
img_Pendu[0].append(PhotoImage(file='Ressource\Image\Pendu 4.png'))
img_Pendu[1].append(PhotoImage(file='Ressource\Image\Pendu 5.png'))
img_Pendu[1].append(PhotoImage(file='Ressource\Image\Pendu 6.png'))
img_Pendu[1].append(PhotoImage(file='Ressource\Image\Pendu 7.png'))
img_Pendu[1].append(PhotoImage(file='Ressource\Image\Pendu 8.png'))

#Chat Zombie
img_chatz=[[],[]]
img_chatz[0].append(PhotoImage(file='Ressource\Image\Chat Zombie 3.png'))
img_chatz[0].append(PhotoImage(file='Ressource\Image\Chat Zombie 4.png'))
img_chatz[1].append(PhotoImage(file='Ressource\Image\Chat Zombie 1.png'))
img_chatz[1].append(PhotoImage(file='Ressource\Image\Chat Zombie 2.png'))

#Fantome
img_fantome=[[],[]]
img_fantome[0].append(PhotoImage(file='Ressource\Image\Fantom 1.png'))
img_fantome[0].append(PhotoImage(file='Ressource\Image\Fantom 2.png'))
img_fantome[1].append(PhotoImage(file='Ressource\Image\Fantom 3.png'))
img_fantome[1].append(PhotoImage(file='Ressource\Image\Fantom 4.png'))

#Images Décore
img_arbre_mort=PhotoImage(file='Ressource\Image\\arbre mort.png')
img_herbe_mort=PhotoImage(file='Ressource\Image\herbe mort.png')
img_tombe=PhotoImage(file='Ressource\Image\\tombe.png')
img_stone_brick=PhotoImage(file='Ressource\Image\Stone brick.png')

#Image Menu
img_fond_ecran=PhotoImage(file='Ressource\Image\Fond ecran 1.png')
img_fond_ecran2=PhotoImage(file='Ressource\Image\Fond ecran 2.png')

#Image option
img_touchpad_arrow=PhotoImage(file='Ressource\Image\\Touchpad arrow.png')
img_touchpad_azerty=PhotoImage(file='Ressource\Image\\Touchpad azerty.png')
img_touchpad_qwerty=PhotoImage(file='Ressource\Image\\Touchpad qwerty.png')

#Fonction de départ
Selection()

#Fin du programme

fen.bind('<Motion>',survol)
fen.bind('<Key>',key)
fen.bind('<KeyRelease>',unkey)
fen.bind('<Button-1>',click)

fen.mainloop()
