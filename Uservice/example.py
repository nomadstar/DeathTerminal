import string, hmac, hashlib, base64

longnameww = len("Wolfeschlegelsteinhausenbergerdorff")
longeadr = 320

class User:
    usid = string
    name = string
    age = int
    playname = string
    playdash = int
    usrnm = string
    email = string
    password = string

    def newser(self,usrnm,email,pswrd):
        if len(email) < longeadr or len(usrnm)<36:
            self.email = email
            self.usrnm = usrnm
        else:
            if len(usrnm)>36:
                raise ValueError("Felicidades, tienes el nombre de usuario más tontamente largo de la historia.")
            if len(email)> longeadr:
                raise ValueError("Felicidades, tienes el email más tontamente largo de la historia.")
        self.password = pswrd
        try:
                idme = hmac.new(self.password.encode(), self.email.encode(), hashlib.sha256)
                self.usid = idme.hexdigest()
        except Exception as e:
            print(f"Error: {e}")
            
