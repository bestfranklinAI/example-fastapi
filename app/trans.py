from .main import cursor, conn
from typing import List
from psycopg2.extras import RealDictRow
class TransPosts():
    def __init__(self,RealDictRow):
        RealDictRow = dict(RealDictRow)
        self.RealDictRow = RealDictRow
        self.title = RealDictRow["title"]
        self.content = RealDictRow["content"]
        self.published = RealDictRow["published"]
        self.id = RealDictRow["id"]
        self.created_at = RealDictRow["created_at"]
        self.owner_id = RealDictRow["owner_id"]
    def list(self):
        post_detail = list(self.RealDictRow.values())
        return post_detail
    def append(self,list: list, something: str):
        list.append(something)
        return list
    def dict(self):
        cursor.execute("""SELECT * FROM users WHERE id = %s""", (str(self.owner_id),))
        owner_details = dict(cursor.fetchone())
        self.RealDictRow["owner"] = owner_details
        return self.RealDictRow

class TransUsers():
    def __init__(self,RealDictRow):
        RealDictRow = dict(RealDictRow)
        self.email = RealDictRow["email"]
        self.password = RealDictRow["password"]
        self.id = RealDictRow["id"]
        self.created_at = RealDictRow["created_at"]
    
    def list(self):
        user_detail = list(self.RealDictRow.values())
        return user_detail
    def append(self,list: list, something: str):
        list.append(something)
        return list
    
class TransAllPosts():
    def __init__(self, RealDictRow : List[RealDictRow]):
        self.RealDictRow = RealDictRow
    def dict(self):
        modify_dict = []
        for i in range(len(self.RealDictRow)):
            modify_dict.append(TransPosts(self.RealDictRow[i]).dict())
        return modify_dict
