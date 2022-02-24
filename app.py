from extensions import SQLAlchemy,db,app,bcrypt
from modules import User,Product
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_user,LoginManager,login_required,current_user,logout_user
from flask import request, render_template, redirect, url_for, jsonify

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

@app.route('/')
def home():   
    return jsonify({"response":"WELCOME"})               

@app.route('/register', methods=["GET","POST",'PUT','DELETE'])
def register():    
    if(request.method=="POST"):
        try:
            v_json = request.get_json()
            v_username = v_json['username']
            v_password = v_json['password']
            v_role = v_json['role']        
            hashed_password = bcrypt.generate_password_hash(v_password)         
            v_user = db.session.query(User).filter_by(username=v_username).first()         
            if(v_user is None):        
                new_user = User(username=v_username,password=hashed_password,role=v_role)
                db.session.add(new_user)
                db.session.commit()           
                return jsonify({"response":"Record registered"})
            else:
                return jsonify({"response":"user alreay present"})  
        except:
            return jsonify({"response":"Check or correct provided input details to Register"})
    elif(request.method=="PUT"):         
        try:
            v_json = request.get_json()
            v_username = v_json['username']
            v_password = v_json['password']
            v_role = v_json['role']        
            hashed_password = bcrypt.generate_password_hash(v_password)         
            v_user = db.session.query(User).filter_by(username=v_username).first()         
            if(v_user):        
                v_user.username = v_username
                v_user.password = hashed_password
                v_user.role = v_role
                db.session.commit()
                return jsonify({"response":"Record Updated"})
        except:
                return jsonify({"response":"Check or correct provided input details for updation"})
    elif(request.method=="DELETE"):         
        try:
            v_json = request.get_json()
            v_username = v_json['username']                     
            v_user = db.session.query(User).filter_by(username=v_username).first()
            if(v_user):
                    db.session.delete(v_user)
                    db.session.commit()
                    return jsonify({"response":"Record Deleted!!!"})           
        except:
                return jsonify({"response":"Check or correct provided input details for deletion"})                
    return jsonify({"response":"Provide User details for addition"}) 

@app.route('/login', methods=["GET","POST"])
def login():    
    if(request.method=="POST"):
        #print("current_user is", current_user.username)
        try:
            v_json = request.get_json()
            v_username = v_json['username']
            v_password = v_json['password'] 
            user = User.query.filter_by(username=v_username).first()
            if user:
                if bcrypt.check_password_hash(user.password, v_password):                    
                    login_user(user)                        
                    return jsonify({"response":"User logged in"})
                return jsonify({"response":"Not logged in,Check password"})     
            return jsonify({"response":"Not logged in,check username"})
        except :
            return jsonify({"response":"Check or correct provided input details to log In"})             
    return jsonify({"response":"POST user details to log In"})

@app.route('/logout', methods=["GET"])
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('login'))
                     
    

@app.route('/products',methods=['GET','POST','PUT','DELETE'])
@login_required
def product():
    user = User()
    v_username = current_user.username    
    op_json = {}
    v_list = []
    if (request.method=="GET"): 
        prod = Product.query.all()
        for item in prod:           
            v_list.append({"productId":item.productId})
            v_list.append({"amountAvailable":item.amountAvailable})
            v_list.append({"cost":item.cost})
            v_list.append({"sellerId":item.sellerId})            
            op_json[item.productName] = v_list 
            v_list = []                
        return jsonify(op_json)
    if(user.sellerrole(v_username)==True):    
        if(request.method =="POST"):
            try:
                v_json = request.get_json()
                v_id = int(v_json['product_id'])
                v_amt_available = int(v_json['amount_available'])
                v_cost = int(v_json['cost'])
                v_product_name = v_json["product_name"]
                v_Seller_id = int(v_json["seller_id"])                    
                v_product = Product(productId=v_id, amountAvailable=v_amt_available, cost=v_cost, productName=v_product_name,sellerId=v_Seller_id)  
                db.session.add(v_product)
                db.session.commit()
                return jsonify({"response":"Record added!"})
            except:
                return jsonify({"response":"Check provided input data again!!!"})    
        elif(request.method =="PUT"):
            try:
                v_json = request.get_json()
                v_id = int(v_json['product_id'])
                v_amt_available = int(v_json['amount_available'])
                v_cost = int(v_json['cost'])
                v_product_name = v_json["product_name"]
                v_seller_id = int(v_json["seller_id"])
                v_product = db.session.query(Product).filter_by(productId=v_id).first()
                if(v_product):
                    v_product.productId = v_id
                    v_product.amountAvailable = v_amt_available
                    v_product.productName = v_product_name
                    v_product.cost = v_cost
                    v_product.sellerId = v_seller_id
                    db.session.commit()
                    return jsonify({"response":"Record updated!!!"})
                else:
                    return jsonify({"response":"No record available with provided productid!!!"})    
            except:
                return jsonify({"response":"Check provided input data again!!!"})                
        elif(request.method =="DELETE"): 
            try:
                v_json = request.get_json()   
                v_id = int(v_json['product_id'])
                v_product = db.session.query(Product).filter_by(productId=v_id).first()
                if(v_product):
                    db.session.delete(v_product)
                    db.session.commit()
                    return jsonify({"response":"Record Deleted!!!"})    
                else:
                    return jsonify({"response":"No record available with provided productid!!!"}) 
            except:
                return jsonify({"response":"Check provided input data again!!!"})
    else:
        return jsonify({"response":"User is not valid to do product Changes!!!"})

@app.route('/deposit',methods=['GET','POST'])
@login_required
def deposit():   
    v_user = current_user.username
    #v_user ="KomalDesai"
    user = User()
    user_role=user.buyerrole(v_user)
    if(user_role==True):
        if(request.method=="POST"):
            try:    
                v_json = request.get_json()            
                v_cost = int(v_json['deposit'])            
                if(v_cost in (5,10,20,50,100)):               
                    user.costdeposit(v_user, v_cost)
                    return redirect(url_for("buy"))
                else:                
                    return jsonify({"response":"Deposit amount should be between (5,10,20,50,100)"})
            except:
                return jsonify({"response":"Check provided input Data!!!"})
        else:
            return jsonify({"response":"Deposit amount should be submitted through POST method"})        
    else:     
        v_message = "User role is not valid for amount Deposit."       
        return jsonify({"response": "User role is not valid for amount Deposit."})

@app.route('/buy',methods=['GET','POST'])
@login_required
def buy():
    v_user = current_user.username
    #v_user = "KomalDesai"
    user = User()
    user_role=user.buyerrole(v_user)
    v_message=''
    op_json = {}
    if(user_role==True):
        if(request.method=="POST"):
            try:            
                v_json = request.get_json()
                v_id = int(v_json["product_id"])             
                v_amt_available  = int(v_json["product_quantity"])         
                prodobj = Product()
                v_total, v_prod_nm, v_change, v_message = prodobj.product_buy(v_user,v_id, v_amt_available)
                op_json['total_spend_money'] = v_total
                op_json['product'] = v_prod_nm
                op_json['change'] = v_change            
                return jsonify(op_json)
            except:
                return jsonify({"response":"Check provided input Data!!!"})
        return jsonify({"response":"buy an Item !!!"})
    else:
        return jsonify({"response":"You are not authorised user to buy an product"})    
            
@app.route('/reset',methods=['GET'])
@login_required
def depositreset():
    v_user = current_user.username
    #v_user = "KomalDesai"
    user = User()
    user_role=user.buyerrole(v_user)
    if(user_role==True):
        user.depositreset(v_user)        
        return jsonify({"response":"Deposit reseted."})
    else:        
        return jsonify({"response":"You are not valid user to reset deposit"})    

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return ('Page is not available'), 404 

@app.errorhandler(405)
def method_not_allowed(e):
    # note that we set the 404 status explicitly
    return ('Method is not allowed'), 405        
        
if __name__ == "__main__":
    app.run()    