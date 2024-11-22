from dotenv import load_dotenv
import os, string, hmac, hashlib, base64, random


load_dotenv()
longnameww = len("Wolfeschlegelsteinhausenbergerdorff")
longeadr = 320

class User:
    usid = string # actually is a hmac password hash
    name = "Anosubordigor"
    age = int
    playname = string
    playdash = int
    email = string
    password = string


    def calculateid(self,email,pswrd):
        if len(email) < longeadr:
            self.email = email
        else:
            if len(email)> longeadr:
                raise ValueError("Felicidades, tienes el email más tontamente largo de la historia.")
        self.password = pswrd
        try:
                idme = hmac.new(self.password.encode(), self.email.encode(), hashlib.sha256)
                return idme.hexdigest()
        except Exception as e:
            print(f"Error: {e}")
    
    def newser(self,email,password):
        self.usid = self.calculateid(email,password)
        self.email = email
    
    def setgamename(self,playname):
        self.playname = playname
        # Logic database here
        self.playdash = random.randint(1, 9999)
        return f"{self.playname}-{self.playdash}"


    def checkuser(self,email,password):
        '''
        Tecnical Database Logic should work this way
        1. Check if the email exists in the database
        2. If the email exists, check if the email asociated with usid in database is the same as calculateid(email,password) (is actually a hashed password)
        3. If the email and usid in the database return an id then the user is correct
        4. If the email or usid in the database is not correct then the user is not correct
        '''
        if self.usid == self.calculateid(email,password):
            return True
        else:
            return False
        


if __name__ == "__main__":
    user = User()
    user.newser("example@example.com", "securepassword123")
    print(f"User Email: {user.email}")
    print(f"User Password: {user.password}")
    print(f"User ID: {user.usid}")
    if user.checkuser("example@example.com", "securepassword123") and not user.checkuser("fake@fake.com", "nonono123"):
        print("Checker seems fine")
    else:
        print("Something is wrong with the checker")