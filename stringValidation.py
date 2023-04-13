class StringValidation:

    def SearchValidation(db, userId):

        if (db is None):
            print("Parameter 'db' has not been assigned a value")
            return
        
        if (userId is None):
            print("Parameter 'userId' has not been assigned a value")
            return
        
        return str(db.check_findByIdText(userId))[1:-2]

    def ShortenText(text, maxLen):
        
        if (text is None):
            print("Parameter 'text' has not been assigned a value")
            return
        
        if (maxLen is None):
            print("Parameter 'maxLen' has not been assigned a value")
            return
        
        if len(text) > maxLen:
            result = text[:len(text) - (len(text) - maxLen)]
            return result + "..."
        return text

    def GenreStrValidation(text):
        
        if (text is None):
            print("Parameter 'text' has not been assigned a value")
            return
        
        result = ""
        for tmpStr in text:
            result += tmpStr + ", "
        return result[:-2] + "."
