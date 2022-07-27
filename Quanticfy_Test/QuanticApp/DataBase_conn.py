import pymysql
import requests
import json

def Create_db():
    try:
        bd_name="quanticfy_test"
        val=False
        con=pymysql.connect(host="localhost",user="root",passwd="")
        cursor=con.cursor()
        cursor.execute("show databases")
        dbs=cursor.fetchall()
        for i in dbs:
            if(i[0]==bd_name):
                val=True
        if (val==False):
            if(cursor.execute("create database "+bd_name)):
                con=pymysql.connect(host="localhost",user="root",passwd="" ,database=bd_name)
                cursor=con.cursor()
                cursor.execute("CREATE TABLE chantier_perturbant (sujet VARCHAR(255) ,description VARCHAR(255), typologie INTEGER(10),niveau_perturbation INTEGER(10),impact_circulation VARCHAR(255))")
                return True
            else:
                return False
            
        else:
            return ("data base exist choose another name ")
    except pymysql.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if con.open:
            con.close()
            cursor.close()
            print("MySQL connection is closed")





def Get_Data_By_API(url):
    response=requests.get('https://opendata.paris.fr/api/records/1.0/search/?dataset=chantiers-perturbants&q=&rows=156').json()['records']
    listrec =[]
    for d in response:  
            listrec.append(d['fields'])
            #print(listrec)
    return listrec      

        
    

def Set_items_In_DB ():
    try:
        i=0
        list=Get_Data_By_API("url")
        filtredlist=[]
        sql="INSERT INTO  chantier_perturbant (sujet  ,description , typologie ,niveau_perturbation ,impact_circulation ) VALUES (%s,%s,%s,%s,%s)"

        con=pymysql.connect(host="localhost",user="root",passwd="" ,database="quanticfy_test")
        cursor=con.cursor()

        for item in list:
            chantier=(item.get("objet"),item.get("description"),item.get("typologie"),item.get("niveau_perturbation"),item.get("impact_circulation"))
            filtredlist.append(chantier)
        
        for item in filtredlist:
            print(item)
            cursor.execute(sql,item)
            
              
    except pymysql.Error as e:
        print(e)

    finally:
        if con.open:
            con.close()
            cursor.close()
            print("MySQL connection is closed")


        
#Set_items_In_DB()
#print(Create_db())
#Get_items_For_DB()