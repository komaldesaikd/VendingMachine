from extensions import db
from flask_login import UserMixin,login_user,LoginManager,login_required,current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    deposit =  db.Column(db.Integer, nullable=False, default=0)  

    def buyerrole(self,v_user):
        self.username = v_user
        self.v_user = db.session.query(User).filter_by(username=self.username).first()
        if(self.v_user.role=='buyer'):
            return(True)
        else:
            return(False)

    def sellerrole(self,v_user):
        self.username = v_user
        self.v_user = db.session.query(User).filter_by(username=self.username).first()
        if(self.v_user.role=='seller'):
            return(True)
        else:
            return(False)         

    def costdeposit(self,v_user, v_cost):
        v_user = db.session.query(User).filter_by(username=v_user).first()
        if(v_user):            
            v_user.deposit = v_cost
            db.session.commit()
        else:
            pass         

    def depositreset(self, v_user): 
        v_user = db.session.query(User).filter_by(username=v_user).first() 
        if(v_user):          
            v_user.deposit = 0
            db.session.commit()

class Product(db.Model):        
    productId = db.Column(db.Integer, primary_key=True)
    amountAvailable = db.Column(db.Integer, nullable =False, default=0)
    cost = db.Column(db.Integer, nullable =False )
    productName = db.Column(db.String(40), unique=True)
    sellerId = db.Column(db.Integer, nullable =False)

    def product_buy(self, v_user, v_id, v_noofprod):
        v_total_spend=0
        self.product_name=""
        self.v_change= 0
        self.v_total_spend=0
        self.user = v_user
        self.id =  v_id
        self.v_noofprod = v_noofprod
        try:
            self.v_user = db.session.query(User).filter_by(username=self.user).first()
            self.v_product = db.session.query(Product).filter_by(productId=self.id).first()
        except:
            self.v_change = self.v_user.deposit             
            v_message = "Input data is not matching with database details"            
            return (self.v_total_spend, self.product_name, self.v_change, v_message)
        if(self.v_user and self.v_product):
            self.amount_available = self.v_product.amountAvailable       
            self.product_name = self.v_product.productName
            self.cost = self.v_product.cost
            self.deposit =  self.v_user.deposit                  
            if(self.amount_available>=self.v_noofprod):
                if(self.deposit>=(self.cost*v_noofprod)):
                    self.v_product.amountAvailable = self.amount_available - v_noofprod
                    self.v_total_spend = v_noofprod * self.cost
                    self.v_change = self.deposit - self.v_total_spend
                    self.v_user.deposit = 0                    
                    db.session.commit()                     
                    v_message = "Your Buy has been Succssesful"
                    return (self.v_total_spend, self.product_name, self.v_change, v_message)
                else:
                    v_message = "Deposit amount does not meet selection product quantity and cost."
                    print(v_message)
                    self.v_change = self.deposit
                    self.product_name = ""
                    return (self.v_total_spend, self.product_name, self.v_change, v_message)
            else:                
                v_message = "Amount of Products are not available"
                self.product_name = ""
                self.v_change = self.deposit
                return (self.v_total_spend, self.product_name, self.v_change,v_message)
        else:
            v_message = "Check user role and product id!!!"     
            return(self.v_total_spend, self.product_name, self.v_change,v_message)            
