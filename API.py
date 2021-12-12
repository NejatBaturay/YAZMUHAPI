import sqlite3
import os.path
from flask import Flask, json, jsonify, abort, request
app = Flask(__name__)



BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
db_path = os.path.join(BASE_DIR,"Database1.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
cursor = conn.cursor()

@app.route('/api/products', methods=['GET','POST'])

def readproductbycategory():
    listofproducts = []    
    cursor1 = conn.cursor()
    
    category = request.args.get('category') 
    item = request.args.get('q')
    
    translatequery = {
        "meyvesebze":1,
        "kisiselBakim":2,
        "atistirmalik":3
        }
   
    if(item is None):
        
         b = cursor1.execute("SELECT *from Products WHERE CategoryId=?",(translatequery[str(category)],))       
         if(b.fetchone()==None):
             abort(404,"Hata:Böyle bir ürün yok")  
         b = cursor1.execute("SELECT *from Products WHERE CategoryId=?",(translatequery[str(category)],))       
         for row in b:
            
            dictproduct = {
                 "id":row[0],
                 "name":row[1],
                 "image":row[4],
                 "additionalInfo":row[2],
                 "cost":float(row[3])
                 }
            listofproducts.append(dictproduct)
    
        
    else:
        b = cursor1.execute("SELECT *from Products WHERE Name LIKE ?",('%'+item+'%',))
        if(b.fetchone()==None):
            abort(404,"Hata:Böyle bir ürün yok")
        else:
            b= cursor1.execute("SELECT *from Products WHERE Name LIKE ?",('%'+item+'%',))
            for row in b:
             
               dictproduct = {
                    "id":row[0],
                    "name":row[1],
                    "image":row[4],
                    "additionalInfo":row[2],
                    "Price":float(row[3])
                    }
       
            listofproducts.append(dictproduct)
            
   
         
    return jsonify(listofproducts)


@app.route('/api/ads', methods=['GET','POST'])
def readads():
    listofads = []    
    cursor1 = conn.cursor()
   
    b = cursor1.execute("SELECT *from Ads")
    for row in b:
       
        dictproduct = {
            "Id":row[0],
            "image":row[1]
            }

        listofads.append(dictproduct)
        
 
      
    return jsonify(listofads)



@app.route('/api/products/<int:ID>', methods=['GET','POST'])

def readproductbyid(ID):
    
    listofproducts = []    
    cursor1 = conn.cursor()
   
    b = cursor1.execute("SELECT *from Products WHERE ID=?",(ID,))
    for row in b:
       
        dictproduct = {
            "id":row[0],
            "name":row[1],
            "image":row[4],
            "additionalInfo":row[2],
            "Price":row[3]
            }

    
  
    return jsonify(dictproduct)

@app.route('/api/users/<int:userid>', methods=['GET'])
def readuser(userid):
      
    cursor1 = conn.cursor()
    
     
    b = cursor1.execute("SELECT Users.Id,Users.Name,Users.Email,Users.Phone FROM Users WHERE USERS.ID = ?",(userid,))
    for row in b:
       
        dictusers = {
            
            "id":row[0],
            "name":row[1], 
            "email":row[2],
            "phoneNumber":row[3],
            
            }
        
  
    return jsonify(dictusers)



@app.route('/api/users/<int:userid>/credit-cards', methods=['GET'])
def readcards(userid):
    listofcards = []    
    cursor1 = conn.cursor()
   
    b = cursor1.execute("SELECT Cards.Id,Cards.cardName,Cards.lastThreeDigit FROM Cards INNER JOIN Users ON Cards.ID = Users.CardId WHERE USERS.ID = ?",(userid,))
    for row in b:
       
        dictcards = {
            "id":row[0],
            "name":row[1],
            "lastThreeDigit":str(row[2]),
          
            }
        listofcards.append(dictcards)
  
    return jsonify(listofcards)



@app.route('/api/users/<int:userid>/adress', methods=['GET'])
def readadresses(userid):
    listofaddresses = []    
    cursor1 = conn.cursor()
   
    b = cursor1.execute("SELECT Address.Id,Addresses.Address FROM Addresses INNER JOIN Users ON Addresses.ID = Users.AddressID WHERE USERS.ID = ?",(userid,))
    for row in b:
       
        dictusers = {
            "id":row[0],
            "name":row[1],
          
            }
        dictusers.append(listofaddresses)
  
    return jsonify(listofaddresses)


@app.route('/api/order', methods=["POST","GET"])
def writeorders():
    
    data = request.json
    cursor1 = conn.cursor()
    for i in range(0,len(data["products"])):
        cursor1.execute("INSERT INTO Orders values (?,?,?,?,?,?)",(None,data["userId"],data["addressId"],data["creditCardId"],data["products"][i]["productId"],data["products"][i]["count"]))
        conn.commit()
    return jsonify(data)






app.config['JSON_SORT_KEYS'] = False
app.run()
