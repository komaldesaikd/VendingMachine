import unittest
from app import User, db, app
import json
  
class BasicTest(unittest.TestCase):  
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")        
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type,"application/json")

    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue(b'WELCOME' in response.data)

# class DepositResetTest(unittest.TestCase):
#     def test_index(self):
#         tester = app.test_client(self)
#         response = tester.get("/reset")        
#         statuscode = response.status_code        
#         self.assertEqual(statuscode,200)

    # def test_index_content(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/reset")
    #     self.assertEqual(response.content_type,"application/json")

    # def test_index_data(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/reset")        
    #     self.assertTrue(b'reset' in response.data)

    # def test_index_data_pos1(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/reset")
    #     db_deposit = (db.session.query(User).filter_by(username="KomalDesai").first()).deposit
     #   self.assertEqual(db_deposit,0)

# class DepositTest(unittest.TestCase):

#      def test_index(self):
#         tester = app.test_client(self)
#         response = tester.get("/deposit")        
#         statuscode = response.status_code
#         self.assertEqual(statuscode,200)

#      def test_index_content(self):
#         tester = app.test_client(self)
#         response = tester.get("/deposit")       
#         self.assertEqual(response.content_type,"application/json")  

#      def test_index_data(self):
#         tester = app.test_client(self)
#         response = tester.get("/deposit")   
#         self.assertTrue(b'POST' in response.data)      

#      def test_index_post(self):
#         tester = app.test_client(self)
#         v_json = {"deposit":50}
#         response = tester.post("/deposit", json=v_json)             
#         statuscode = response.status_code
#         self.assertEqual(statuscode,302)

#      def test_index_content_post(self):
#         tester = app.test_client(self)
#         v_json = {"deposit":50}
#         response = tester.post("/deposit", json=v_json)               
#         self.assertEqual(response.content_type,"text/html; charset=utf-8")    
      
#      def test_index_data_post_pos(self):
#         tester = app.test_client(self)
#         v_json = {"deposit":50}
#         response = tester.post("/deposit", json=v_json)  
#         self.assertTrue(b'buy' in response.data)

#      def test_index_data_post_neg1(self):
#         tester = app.test_client(self)
#         v_json = {"deposit":55}
#         response = tester.post("/deposit", json=v_json)  
#         self.assertTrue(b'between (5,10,20,50,100)' in response.data)

#      def test_index_data_post_neg2(self):
#         tester = app.test_client(self)
#         v_json = ''
#         response = tester.post("/deposit", json=v_json)  
#         self.assertTrue(b'Check' in response.data)       


# class BuyTest(unittest.TestCase):
#     def test_index(self):
#         tester = app.test_client(self)
#         response = tester.get("/buy")        
#         statuscode = response.status_code
#         self.assertEqual(statuscode,200)

#     def test_index_content(self):
#         tester = app.test_client(self)
#         response = tester.get("/buy")       
#         self.assertEqual(response.content_type,"application/json")  

#     def test_index_data(self):
#         tester = app.test_client(self)
#         response = tester.get("/buy")   
#         self.assertTrue(b'buy' in response.data)

#     def test_index_post(self):
#         tester = app.test_client(self)
#         v_json = {"product_id":1,"product_quantity":2}
#         response = tester.post("/buy", json=v_json)             
#         statuscode = response.status_code
#         self.assertEqual(statuscode,200)

#     def test_index_content_post(self):
#         tester = app.test_client(self)
#         v_json = {"product_id":1,"product_quantity":2}
#         response = tester.post("/buy", json=v_json)               
#         self.assertEqual(response.content_type,"application/json")  

#     def test_index_data_post_pos11(self):
#         tester = app.test_client(self)
#         v_json = {"deposit":50}
#         response = tester.post("/deposit", json=v_json)  
#         self.assertTrue(b'buy' in response.data)      
      
#     def test_index_data_post_pos12(self):
#         tester = app.test_client(self)
#         v_json = {"product_id":1,"product_quantity":2}
#         response = tester.post("/buy", json=v_json)  
#         self.assertTrue(b'change' in response.data)

#     def test_index_data_post_neg11(self):
#         tester = app.test_client(self)
#         v_json = {"deposit":100}
#         response = tester.post("/deposit", json=v_json)  
#         self.assertTrue(b'buy' in response.data)      
      
#     def test_index_data_post_neg12(self):
#         tester = app.test_client(self)
#         v_json = {"product_id":2,"product_quantity":2}
#         response = tester.post("/buy", json=v_json)        
#         v_data = json.loads(response.data.decode('utf-8'))       
#         self.assertTrue(b'change' in response.data)

if __name__ == '__main__':
    unittest.main()
