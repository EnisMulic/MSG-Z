class DLWMS_Notification:
    def __init__(self, link, title, date, subject, author, mail):
        self.link = link
        self.title = title
        self.date = date
        self.subject = subject
        self.author = author
        self.mail = mail
        
    def __str__(self):
        return "Naslov: " + self.title + \
               "\nDatum: " + self.date + \
               "\nAutor: " + self.author + \
               "\nMail: " + self.mail + "\n"
    
    def __eq__(self, other):
        return self.link == other.link and \
               self.title == other.title and \
               self.date == other.date and \
               self.subject == other.subject and \
               self.author == other.author and \
               self.mail == other.mail

class Discord_Bot_Notification:
    def __init__(self, author, title, desctiption, date, colour):
        self.author = author
        self.title = title,
        self.desctiption = description,
        self.date = date,
        self.colour = colour

    
