#Bibliothèque
from selenium import webdriver
import pandas as pd
from time import sleep,strptime
from bs4 import  BeautifulSoup
from datetime import datetime 
from pathlib import Path
import tkinter as tk 
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#class

class information:
    def __init__(self,table,nom,classe):
        self.t=table                #Dans quel tableau (web) se trouve l'information (voir Jour 3 du journal de bord)
        self.n=nom                  #Nom qu'a l'élément dans le code source du site
        self.c=classe               #Type statique ou dynamique


# Variable globale

    #Liens site
URL_Xtracker="https://etf.dws.com/en-lu/LU0490618542-sp-500-swap-ucits-etf-1c/"
URL_Invesco="https://etf.invesco.com/lu/institutional/en/product/invesco-sp-500-ucits-etf-dist/security-information"

            #Info à recuellir
    #Xtrackers
ISIN_X=information(1,'ISIN','static')
Launch_Date_X=information(1,'Sub-Fund Launch Date','static')
Curency_X=information(1,'Share Class Currency','static')
Invest_Meth_X=information(2,'Investment Methodology','static')
ETD_X=information(4,'Estimated Tracking Difference','dynamic')
Domicile_X=information(5,'Fund Domicile','static')
NAV_X=information(6,'NAV*','dynamic')
NAV_date_X=information(6,'NAV Date','dynamic')
Out_shares_X=information(6,'Outstanding shares','dynamic')
AUMs_X=information(6,'Total AUM of Fund*','dynamic')
    #Invesco
ISIN_I=information(2,'ISIN','static')
Launch_Date_I=information(1,'Launch date','static')
Out_shares_I=information(1,'Shares outstanding','dynamic')
Curency_I=information(2,'Base currency','static')
NAV_I=information(2,'NAV','dynamic')
NAV_date_I=information(2,'NAV Date','dynamic')
AUMs_I=information(2,'AUM','dynamic')
            #Autre
date=datetime.now()                           #Date 
path_G=Path(__file__).parent                  #Chemin courant du fichier GOLDBAUM

            #Info sous forme tableau
tab_val=[]                                                                      #Initialisation du tableau des valeurs de chaque information
tab_nom_Xtracker=[ISIN_X,Launch_Date_X,Curency_X,Invest_Meth_X,ETD_X,Domicile_X,NAV_X,NAV_date_X,Out_shares_X,AUMs_X]
tab_nom_Invesco=[ISIN_I,Launch_Date_I,Out_shares_I,Curency_I,NAV_I,NAV_date_I,AUMs_I]


def get(n):
    if n==2:
        info_Trackers=get_information(URL_Xtracker,tab_nom_Xtracker)
        store_panda_dynamic(info_Trackers,tab_nom_Xtracker,URL_Xtracker)
        store_panda_static(info_Trackers,tab_nom_Xtracker,URL_Xtracker)
    if n==1:
        info_Invesco=get_information(URL_Invesco,tab_nom_Invesco)
        store_panda_dynamic(info_Invesco,tab_nom_Invesco,URL_Invesco)
        store_panda_static(info_Invesco,tab_nom_Invesco,URL_Invesco)



# Recuperer du site internet
def get_page_dyn(url):              #fonction qui permet de récupérer les données dynamiques
    driver = webdriver.Chrome()
    driver.get(url)
    pass_1st_page(driver,url)
    sourceCode=driver.page_source
    return  sourceCode

def pass_1st_page(driver,url):          #fonction qui permet de passer la page d'accueil du site Xtracker
    if (url==URL_Xtracker):
        sleep(1)
        driver.find_element_by_class_name('audience-selection__item-overlay').click()
        sleep(1)
        driver.find_element_by_id('en-lu').click()
    elif (url==URL_Invesco):
        sleep(1)
        driver.find_element_by_id('popup-buttons').click()                  #Accepter les cookies
        sleep(3)
        driver.find_element_by_class_name('selectboxit-text').click()       #Choisir pays
        sleep(1)
        driver.find_element_by_xpath("//li[@data-id='10']").click()         #Luxembourg
        sleep(1)
        driver.find_element_by_class_name('institutional').click()          #Investisseur privée
        sleep(1)
        driver.find_element_by_id('overlay_button_submit').click()          #Accepter les conditions d'utilisation
    else:
        print("URL non reconnu")
        
def get_information(url,tab_nom):                                               #Trouve les informations en fonction de l'url       
    soup = BeautifulSoup(get_page_dyn(url),'html.parser') 
    tab_val=[]  
    if (url==URL_Xtracker):
        page_info = soup.find("div", class_="row content internal-concept")
        tables = page_info.find_all('table',class_='table-3')                   #Voir journal de bord 
        i=0
        for table in tables:
            i+=1
            for j in range (len(tab_nom)):
                if (i==tab_nom[j].t):
                    tr_e = table.find_all(class_="tr-even")                     #Les valeurs sont dans les balises tr-even
                    tr_o = table.find_all(class_="tr-odd")                      # et tr-odd
                    tr_i=0
                    test_w=True
                    while(test_w):
                        tmp_te=tr_e[tr_i].find(string=tab_nom[j].n)
                        tmp_to=tr_o[tr_i].find(string=tab_nom[j].n)
                        
                        if(tmp_te == tab_nom[j].n):                             #On test si on a besoin de l'informations dans la balise "tr-even"
                            tab_val.append(tr_e[tr_i].find('td').text)          #Si oui, on garde l'information dans res
                            test_w = False                                      #Et on change d'information
                            
                        elif (tmp_to == tab_nom[j].n):                          #On test si on a besoin des informations dans la balise "tr-odd"
                            tab_val.append(tr_o[tr_i].find('td').text)
                            test_w = False
                            
                        elif ( 'Estimated Tracking Difference'== tab_nom[j].n): # Cet informations est dans une balise différente
                            tab_val.append(tr_o[3].find('span').text)
                            test_w = False
                            
                        else:                                                   #Si l'information que l'on cherche n'est pas là, on change de balise
                            tr_i=tr_i+1
        return(tab_val)
        
    elif (url==URL_Invesco):
        j=0
        for j in range (len(tab_nom)):
            if tab_nom[j].t==1:                                                 # tab_nom[j].t==1 --> information dans 'Key information'
                x = soup.find("div", class_="panel-panel left col-sm-8")
                l_key_value = x.find('table',class_='l-key-value')          
                tbody = l_key_value.find_all('tbody')
                
                for fenetre in tbody:
                        tr = fenetre.find_all('tr')
                        for k in tr:
                            
                            td = k.find_all('td')
                            
                            if(td[0].text.strip()== tab_nom[j].n):
                                res = str(td[1].text.strip())
                                tab_val.append(res)
            elif tab_nom[j].t==2:                                               # tab_nom[j].t==1 --> information dans 'Security information'
                x = soup.find("div", class_="panel-panel right col-sm-4")
                results = x.find_all('table',class_='l-key-value')
                for fenetre in results:
                        tr = fenetre.find_all('tr')
                        for k in tr:
                            td = k.find_all('td') 
                            if(tab_nom[j].n=='NAV' and td[0].text.strip()[0:3]=='NAV'):     #Les valeurs de NAV et NAV date sont confondues sur le site Invesco
                                res = td[1].text.strip()
                                tab_val.append(res)
                            elif(tab_nom[j].n=='NAV Date' and td[0].text.strip()[0:3]=='NAV'):
                                res = td[0].text
                                tab_val.append(get_date(res))
                            elif(td[0].text.strip()== tab_nom[j].n):
                                res = td[1].text.strip()
                                tab_val.append(res)
                                
            
        return(tab_val)
    else:
        print("URL non reconnu")
     
def store_panda_static(tab_val,tab_nom,url):                                    #Enregistre en .csv les données statiques
    data_static= pd.DataFrame()
    tmpnom=[]
    tmpval=[]
    for i in range(len(tab_nom)):
        if (tab_nom[i].c=='static'):
            tmpnom.append(tab_nom[i].n)
            tmpval.append(tab_val[i])
    data_static['data static']=tmpnom
    data_static['data value']=tmpval
    if (url==URL_Xtracker):
        data_static.to_csv(path_or_buf=str(path_G)+r"\File\Static"+"Xtracers"+".csv",index = False ,mode='w+')
    else:
        data_static.to_csv(path_or_buf=str(path_G)+r"\File\Static"+"Invesco"+".csv",index = False ,mode='w+')

def store_panda_dynamic(tab_val,tab_nom,url):                                   #Enregistre en .csv les données dynamiques
    data_dynamic= get_dynamic_data(url)
    tmpnom=[]
    tmpval=[]
    for i in range(len(tab_nom)):
        if (tab_nom[i].c=='dynamic'):
            tmpnom.append(tab_nom[i].n)
            tmpval.append(tab_val[i])
    data_dynamic['data value '+str(date.day)+'/'+str(date.month)+'/'+str(date.year)]=tmpval
    if (url==URL_Xtracker):
        data_dynamic.to_csv(path_or_buf=str(path_G)+r"\File\Dynamic"+"Xtracers"+".csv",index = False,mode='w+')
    else:
        data_dynamic.to_csv(path_or_buf=str(path_G)+r"\File\Dynamic"+"Invesco"+".csv",index = False,mode='w+')
    
def get_dynamic_data(url):                                                      #Va chercher les données d'un fichier .csv
    if (url==URL_Xtracker):
        data_dynamic= pd.read_csv(str(path_G)+r"\File\Dynamic"+"Xtracers"+".csv")
        return(data_dynamic)
    elif (url==URL_Invesco):
        data_dynamic= pd.read_csv(str(path_G)+r"\File\Dynamic"+"Invesco"+".csv")
        return(data_dynamic)

def get_static_data(url):  
    if (url==URL_Xtracker):
        data_static= pd.read_csv(str(path_G)+r"\File\Static"+"Xtracers"+".csv")
        return(data_static)
    elif (url==URL_Invesco):
        data_static= pd.read_csv(str(path_G)+r"\File\Static"+"Invesco"+".csv")
        return(data_static)

def get_date(chain):                                                            #Fonction spécifique pour recuperer le NAV date sur Invesco 
    out=''
    start=0
    for i in chain:
        if(i=='('):
            start=1
        if(i==')'):
            start=0
        if start==1:
            out+=i
    return(out[1:len(out)])
    
def str_to_datetime(strs):      #
    if v.get()==2:
        m, d, y = (str(x) for x in strs.split(" "))
        d=int(d[0:2])
        y=int(y)
        m=strptime(m,'%b').tm_mon
        return (datetime(y, m, d))
    if v.get()==1:
        d, m, y = (str(x) for x in strs.split(" "))
        d=int(d)
        y=int(y)
        m=strptime(m,'%b').tm_mon
        return (datetime(y, m, d))
def new_winF(v):    # new window definition

    fen_graph = tk.Toplevel(root)
    if v.get()==2:                              #Choix Xtrackers
        td=get_dynamic_data(URL_Xtracker)
        ts=get_static_data(URL_Xtracker)
        fen_graph.title('Data ETF Xtrackers')
    if v.get()==1:                              #Choix Invesco
        ts=get_static_data(URL_Invesco)
        td=get_dynamic_data(URL_Invesco)
        fen_graph.title('Data ETF Invesco')
                  #Création sous-fenetre 
    
    t_dv=ts.loc[:,'data value']                  #Affichage static data
    tk.Label(fen_graph, text='DATA VALUE', bg='white', width=35, height=2, relief=tk.RIDGE, fg='blue').grid(row=0, column=1)
    t_ds=ts.loc[:,'data static']
    tk.Label(fen_graph, text='DATA STATIC', bg='white', width=35, height=2, relief=tk.RIDGE, fg='blue').grid(row=0, column=2)
    for j in range (len(t_dv)):
        tk.Label(fen_graph, text=t_ds[j], bg='white', width=35, height=2).grid(row=j+1, column=1)
        tk.Label(fen_graph, text=t_dv[j], bg='white', width=35, height=2).grid(row=j+1, column=2)
    
    tk.Button(fen_graph, text='Quit', command=fen_graph.destroy, bg='red', width=25,font=("bold")).grid(row=len(t_dv)+1, column=1)
    tk.Button(fen_graph, text='Get', command=lambda : get(v.get()), bg='green', width=25,font=("bold")).grid(row=len(t_dv)+1, column=2)
    tk.Label(fen_graph, text=' Program by L.Pagny for GOLDBAUM', font=("Helvetica", 10, "bold italic")).grid(row=len(t_dv)+2, column=1)
                                                                            #Graph NAVs et AUM
    
    t_nav=[]                            #tableaux intermédiaires
    t_navd=[]
    t_out=[]
    td_out=[]
    
    nav_y=[]                            #tableau ordonnee NAV
    nav_x=[]                            #tableau abscisse NAV
    aum_y=[]                           #tableau ordonnee Outstanding shares
    aum_x=[]                           #tableau abscisse Outstanding shares
    
    if v.get()==1:
        n=4
    if v.get()==2:
        n=5
    
    for j in range (1,n):               #Permet de récuperer au format brut les données
        nav=td.iloc[j]
        for i in range (len(nav)):
            if (nav[i]!=nav[i-1]):
                if (j==2): 
                    t_navd.append(nav[i])
                if (j==1):
                    t_nav.append(nav[i])
                if (j==3) and (v.get()==1):
                    t_out.append(nav[i])
                    td_out.append(td.iloc[j-1][i])
                if (j==4) and (v.get()==2):
                    t_out.append(nav[i])
                    td_out.append(td.iloc[j-2][i])
                
    for i in range (1,len(t_nav)):      #Permet d'avoir des NAV en ordonnée et des dates en abscisse
        if v.get()==1:
            nav_y.append(float(t_nav[i][1:len(t_nav[i])]))
            nav_x.append(str_to_datetime(t_navd[i]))
        if v.get()==2:
            nav_y.append(float(t_nav[i][0:len(t_nav[i])-4]))
            nav_x.append(str_to_datetime(t_navd[i]))
    for i in range (1,len(t_out)):
        if v.get()==1:
            aum_y.append(int(str(t_out[i])[1:len(t_out[i])].replace(',','')))
            aum_x.append(str_to_datetime(td_out[i]))
        if v.get()==2:
            aum_y.append(float(str(t_out[i][0:4])))
            aum_x.append(str_to_datetime(td_out[i]))
            
    if v.get()==2:
        fig1, ax1 = plt.subplots()
        ax1.plot(nav_x,nav_y)
        ax1.grid(True)
        fig1.autofmt_xdate()
        plt.title('NAV (Net Asset Value)')
        plt.savefig(str(path_G)+r'\File\NavGraphX.png',dpi=80)        
        plt.close(fig1)
        
        fig2, ax2 = plt.subplots()
        ax2.plot(aum_x,aum_y)
        ax2.grid(True)
        fig2.autofmt_xdate()
        plt.title('AUM (Assets Under Management)')
        plt.savefig(str(path_G)+r'\File\AumGraphX.png',dpi=80)
        plt.close(fig2)
    if v.get()==1:
        fig1, ax1 = plt.subplots()
        ax1.plot(nav_x,nav_y)
        ax1.grid(True)
        fig1.autofmt_xdate()
        plt.title('NAV (Net Asset Value)')
        plt.savefig(str(path_G)+r'\File\NavGraphI.png',dpi=80)        
        plt.close(fig1)
        
        fig2, ax2 = plt.subplots()
        ax2.plot(aum_x,aum_y)
        ax2.grid(True)
        fig2.autofmt_xdate()
        plt.title('AUM (Assets Under Management)')
        plt.savefig(str(path_G)+r'\File\AumGraphI.png',dpi=80)
        plt.close(fig2)
    
    
    # Canvas NAV
    if v.get()==2:

        gph_navX=tk.Canvas(fen_graph,height=480,width=680,bg='white')
        gph_aumX=tk.Canvas(fen_graph,height=480,width=680,bg='white')
        gph_navX.grid(row=0, column=3, rowspan=len(t_dv)+1)
        gph_aumX.grid(row=len(t_dv)+1, column=3, columnspan=len(ts)+3)
    
        NavGraphX = tk.PhotoImage(file=(str(path_G)+r'\File\NavGraphX.png'))
        AumGraphX = tk.PhotoImage(file=(str(path_G)+r'\File\AumGraphX.png'))
        root.NavGraphX = NavGraphX  # to prevent the image garbage collected.
        root.AumGraphX = AumGraphX  
        gph_navX.create_image((0,0), image=NavGraphX, anchor='nw')
        gph_aumX.create_image((0,0), image=AumGraphX, anchor='nw')
        
    if v.get()==1:
        
        gph_navI=tk.Canvas(fen_graph,height=480,width=680,bg='white')
        gph_aumI=tk.Canvas(fen_graph,height=480,width=680,bg='white')
        gph_navI.grid(row=0, column=3, rowspan=len(t_dv)+1)
        gph_aumI.grid(row=len(t_dv)+1, column=3, columnspan=len(ts)+3)
        
        NavGraphI = tk.PhotoImage(file=(str(path_G)+r'\File\NavGraphI.png'))
        AumGraphI = tk.PhotoImage(file=(str(path_G)+r'\File\AumGraphI.png'))
        root.NavGraphI = NavGraphI  # to prevent the image garbage collected.
        root.AumGraphI = AumGraphI  # to prevent the image garbage collected.
        gph_navI.create_image((0,0), image=NavGraphI, anchor='nw')
        gph_aumI.create_image((0,0), image=AumGraphI, anchor='nw')
    
    
# FRONT END
root = tk.Tk()
root.title('MainWindow - Choose your ETF')
v = tk.IntVar()

            #CREATION DES WIDGETS
btn_quit=tk.Button(root, text='Quit', command=root.destroy, bg='red')
Titre_main=tk.Label(root, text='Application Scrapping ETF', padx=2, pady=1, width=30,font=("Times new romans", 15, "bold"))
CB_Invesco=tk.Radiobutton(root,text='Invesco', variable=v, value=1, font=("Times new romans", 10))
CB_Xtrackers=tk.Radiobutton(root,text='Xtrackers',variable=v, value=2, font=("Times new romans", 10))
btn_win=tk.Button(root, text ="Click to open", command =( lambda: new_winF(v) ) )
Label1=tk.Label(root, text="Choose an ETF :",compound=tk.LEFT, font=("Times new romans", 10,"underline"))
Espace1=tk.Label(root, text="")
Espace2=tk.Label(root, text="")

            #POSITON DES WIDGETS
btn_win.grid(row=5,column=2)
btn_quit.grid(row=5,column=4)
CB_Invesco.grid(row=3,column=3)
CB_Xtrackers.grid(row=3,column=2)
Titre_main.grid(row=1,column=2)
Label1.grid(row=3, column=1)
Espace1.grid(row=4, column=3)
Espace2.grid(row=2, column=3)

            # PARAMETRE FENETRE
root.minsize(110,110)
root.mainloop()