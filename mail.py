import smtplib
from email.message import EmailMessage

class Emailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send(self, recipient, subject, body):
        msg = EmailMessage()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject  
        msg.set_content(body)

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(self.email, self.password)
        smtp_server.send_message(msg)
        smtp_server.quit()


class SendEmail:

    def __init__(self, email):
        self.emailer = Emailer('sosexamplemessage@gmail.com', 'jrpd befe utpa mxxp')
        self.receiver = email
        self.subject = '🚔👮🏾SOS Alert🏥🩸'

    def _parseLog(self, log):
        logresult = "".join(list(log))

        return logresult

    def minorImpact(self, timestamp, coords, log):
        parsedLog = self._parseLog(log=log)
        mapstring = f'https://www.google.com/maps/@{coords[0]},{coords[1]},17z?entry=ttu'
        message = f'''Accident of Severity Level: 1 [Minor Impact]\n
                    TimeStamp: {timestamp}\n
                    Location of Accident: {mapstring}\n

                    Detailed Analysis of the Situation:
                        {parsedLog}
                '''
        
        self.emailer.send(self.receiver, self.subject, message)
        

    def substantialImpact(self, timestamp, coords, log):
        parsedLog = self._parseLog(log=log)
        mapstring = f'https://www.google.com/maps/@{coords[0]},{coords[1]},17z?entry=ttu'
        message = f'''Accident of Severity Level: 2 [Substantial Impact]\n
                    TimeStamp: {timestamp}\n
                    Location of Accident: {mapstring}\n

                    Detailed Analysis of the Situation:
                        {parsedLog}
                '''
        
        self.emailer.send(self.receiver, self.subject, message)

    def criticalImpact(self, timestamp, coords, log):
        parsedLog = self._parseLog(log=log)
        mapstring = f'https://www.google.com/maps/@{coords[0]},{coords[1]},17z?entry=ttu'
        message = f'''Accident of Severity Level: 3 [Critical Impact]\n
                    TimeStamp: {timestamp}\n
                    Location of Accident: {mapstring}\n

                    Detailed Analysis of the Situation:
                        {parsedLog}
                '''
        
        self.emailer.send(self.receiver, self.subject, message)