import sqlite3

class Database:
    
    def GetCurrentDBConnection():
        return sqlite3.connect('db.db')
    
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        
    def add_id_user(self, id_user, first_name, last_name, username, Panel, ACTIVE_TAB, jamSelect, jamDay, findByIdBool, findByIdText, findByNameBool, findPersonByName, findReviewById):
        with self.connection:
            try:
                return self.cursor.execute("INSERT INTO Users ('ID', 'first_name', 'last_name', 'Username', 'Panel', 'ACTIVE_TAB', 'jamSelect', 'jamDay', 'findByIdBool', 'findByIdText', 'findByNameBool', 'findPersonByName', 'findReviewById') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [id_user, first_name, last_name, username, Panel, ACTIVE_TAB, jamSelect, jamDay, findByIdBool, findByIdText, findByNameBool, findPersonByName, findReviewById])
            except:
                return
            
    def add_Panel(self, Panel, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET Panel = ? where ID = ?", [Panel, ID])

    def check_Panel(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT Panel FROM Users where ID = ?', [ID]).fetchone()
        
    def add_ACTIVE_TAB(self, ACTIVE_TAB, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET ACTIVE_TAB = ? where ID = ?", [ACTIVE_TAB, ID])

    def check_ACTIVE_TAB(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT ACTIVE_TAB FROM Users where ID = ?', [ID]).fetchone()
        
    def add_jamSelect(self, jamSelect, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET jamSelect = ? where ID = ?", [jamSelect, ID])

    def check_jamSelect(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT jamSelect FROM Users where ID = ?', [ID]).fetchone()
        
    def add_jamDay(self, jamSelect, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET jamDay = ? where ID = ?", [jamSelect, ID])

    def check_jamDay(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT jamDay FROM Users where ID = ?', [ID]).fetchone()
        
    def add_findByIdBool(self, findByIdBool, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET findByIdBool = ? where ID = ?", [findByIdBool, ID])

    def check_findByIdBool(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT findByIdBool FROM Users where ID = ?', [ID]).fetchone()
        
    def add_findByIdText(self, findByIdText, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET findByIdText = ? where ID = ?", [findByIdText, ID])

    def check_findByIdText(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT findByIdText FROM Users where ID = ?', [ID]).fetchone()
        
    def add_findByNameBool(self, findByNameBool, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET findByNameBool = ? where ID = ?", [findByNameBool, ID])

    def check_findByNameBool(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT findByNameBool FROM Users where ID = ?', [ID]).fetchone()

    def add_findPersonByName(self, findPersonByName, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET findPersonByName = ? where ID = ?", [findPersonByName, ID])
    def check_findPersonByName(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT findPersonByName FROM Users where ID = ?', [ID]).fetchone()

    def add_findReviewById(self, findReviewById, ID):
        with self.connection:
            return self.cursor.execute("UPDATE Users SET findReviewById = ? where ID = ?", [findReviewById, ID])
    def check_findReviewById(self, ID):
        with self.connection:
            return self.cursor.execute('SELECT findReviewById FROM Users where ID = ?', [ID]).fetchone()



