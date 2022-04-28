
import datetime

class DateHelper:
    '''Some helper functions to quickly calculate date.'''
    today_date = datetime.date.today()
    def macaodialy_keep_date(self):
        """ 2020-11-18 - 2019-05-01"""
        return date.fromisoformat("2019-05-01")
    def days_later(self, days):
        '''Return days later in YYYY-MM-DD format.'''
        date = self.today_date + datetime.timedelta(days=days)
        return date.isoformat()
    def days_ago(self, days):
        '''Return days ago in YYYY-MM-DD format.'''
        date = self.today_date - datetime.timedelta(days=days)
        return date.isoformat()
    def today(self):
        '''Return today in YYYY-MM-DD format.'''
        return self.today_date.isoformat()        
    def tomorrow(self):
        '''Return tomorrow in YYYY-MM-DD format.'''
        return self.days_later(1)
    def yesterday(self):
        '''Return yesterday in YYYY-MM-DD format.'''
        return self.days_ago(1)
def txt_log(msg):
    with open(f"news_log_{DateHelper().today()}.txt", 'a',encoding='utf-8') as the_file:
        the_file.write(datetime.date.today().isoformat())
        the_file.write(":")
        the_file.write(str(msg))
        the_file.write('\n')
def mail_noti(msg,title="news"):
    return requests.post(
        f"https://api.mail.mycompany.com.mo/mailnoti",
        auth=("api", "API_KEY"),
        data={"from": "FROM",
        "to": "TO",
        "subject": title,
        "text": msg})

