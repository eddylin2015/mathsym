import remi.gui as gui
import time
import datetime
from remi.gui import *
from remi import start, App
import random
import threading
import esmathlib as lib    # 自定義,數學出題庫  

NTE_Storage = {}

'''
        NTE = lib.Get_Expr(QIID, QAMT, Tx)
        SID = lib.GetKey()
        NTE_Storage[SID] = NTE
'''
Tx=0
Th=0
def Tb(num_rows, num_cols):
    data = [['' for j in range(num_cols)] for i in range(num_rows)]
    for i in range(1,11):
       data[i]=[str(i),'','','']
    data[0]=['题號','對/错','耗時','得分']
    data[11]=['總計','','','']
    return data
MarkTb = Tb(12,4)


class CookieInterface(gui.Tag, gui.EventSource):
    def __init__(self, remi_app_instance, **kwargs):
        """
        This class uses javascript code from cookie.js framework ( https://developer.mozilla.org/en-US/docs/Web/API/document.cookie )
        /*\
        |*|
        |*|  :: cookies.js ::
        |*|
        |*|  A complete cookies reader/writer framework with full unicode support.
        |*|
        |*|  Revision #2 - June 13th, 2017
        |*|
        |*|  https://developer.mozilla.org/en-US/docs/Web/API/document.cookie
        |*|  https://developer.mozilla.org/User:fusionchess
        |*|  https://github.com/madmurphy/cookies.js
        |*|
        |*|  This framework is released under the GNU Public License, version 3 or later.
        |*|  http://www.gnu.org/licenses/gpl-3.0-standalone.html
        |*|
        \*/
        """
        super(CookieInterface, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.app_instance = remi_app_instance
        self.EVENT_ONCOOKIES = "on_cookies"
        self.cookies = {}
        
    def request_cookies(self):
        self.app_instance.execute_javascript("""
            var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
            var result = {};
            for (var nLen = aKeys.length, nIdx = 0; nIdx < nLen; nIdx++) { 
                var key = decodeURIComponent(aKeys[nIdx]);
                result[key] = decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(key).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null; 
            }
            remi.sendCallbackParam('%s','%s', result);
            """%(self.identifier, self.EVENT_ONCOOKIES))

    @gui.decorate_event
    def on_cookies(self, **value):
        self.cookies = value
        return (value,)
    
    def remove_cookie(self, key, path='/', domain=''):
        if not key in self.cookies.keys():
            return
        self.app_instance.execute_javascript( """
            var sKey = "%(sKey)s";
            var sPath = "%(sPath)s";
            var sDomain = "%(sDomain)s";
            document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "");
            """%{'sKey': key, 'sPath': path, 'sDomain': domain} )

    def set_cookie(self, key, value, expiration='Infinity', path='/', domain='', secure=False):
        """
        expiration (int): seconds after with the cookie automatically gets deleted
        """

        secure = 'true' if secure else 'false'
        self.app_instance.execute_javascript("""
            var sKey = "%(sKey)s";
            var sValue = "%(sValue)s";
            var vEnd = eval("%(vEnd)s");
            var sPath = "%(sPath)s"; 
            var sDomain = "%(sDomain)s"; 
            var bSecure = %(bSecure)s;
            if( (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) == false ){
                var sExpires = "";
                if (vEnd) {
                    switch (vEnd.constructor) {
                        case Number:
                            sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
                        break;
                        case String:
                            sExpires = "; expires=" + vEnd;
                        break;
                        case Date:
                            sExpires = "; expires=" + vEnd.toUTCString();
                        break;
                    }
                }
                document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
            }
            """%{'sKey': key, 'sValue': value, 'vEnd': expiration, 'sPath': path, 'sDomain': domain, 'bSecure': secure})


class LoginManager(gui.Tag, gui.EventSource):
    """
    Login manager class allows to simply manage user access safety by session cookies
    It requires a cookieInterface instance to query and set user session id
    When the user login to the system you have to call
        login_manager.renew_session() #in order to force new session uid setup
    The session have to be refreshed each user action (like button click or DB access)
    in order to avoid expiration. BUT before renew, check if expired in order to ask user login
        if not login_manager.expired:
            login_manager.renew_session()
            #RENEW OK
        else:
            #UNABLE TO RENEW
            #HAVE TO ASK FOR LOGIN
    In order to know session expiration, you should register to on_session_expired event
        on_session_expired.do(mylistener.on_user_logout)
    When this event happens, ask for user login
    """
    def __init__(self, cookieInterface, session_timeout_seconds = 60, **kwargs):
        super(LoginManager, self).__init__(**kwargs)
        gui.EventSource.__init__(self)
        self.expired = True
        self.session_uid = str(random.randint(1,999999999))
        self.cookieInterface = cookieInterface
        self.session_timeout_seconds = session_timeout_seconds
        self.timer_request_cookies() #starts the cookie refresh
        self.timeout_timer = None #checks the internal timeout
    
    def timer_request_cookies(self):
        self.cookieInterface.request_cookies()
        self.cookie_timer = threading.Timer(self.session_timeout_seconds/10.0, self.timer_request_cookies)
        self.cookie_timer.daemon = True
        self.cookie_timer.start()

    @gui.decorate_event
    def on_session_expired(self):
        self.expired = True
        return ()

    def renew_session(self):
        """Have to be called on user actions to check and renew session
        """
        if ((not 'user_uid' in self.cookieInterface.cookies) or self.cookieInterface.cookies['user_uid']!=self.session_uid) and (not self.expired):
            self.on_session_expired()

        if self.expired:
            self.session_uid = str(random.randint(1,999999999))
        
        self.cookieInterface.set_cookie('user_uid', self.session_uid, str(self.session_timeout_seconds))

        #here we renew the internal timeout timer
        if self.timeout_timer:
            self.timeout_timer.cancel()
        self.timeout_timer = threading.Timer(self.session_timeout_seconds, self.on_session_expired)
        self.timeout_timer.daemon = True
        self.expired = False
        self.timeout_timer.start()


class TestMySelf(App):
    def __init__(self, *args):
        super(TestMySelf, self).__init__(*args)

    def on_login(self, emitter):
        self.login_manager.renew_session()
        self.lblsession_status.set_text('LOGGED IN')

    def on_renew(self, emitter):
        if not self.login_manager.expired:
            self.login_manager.renew_session()
            self.lblsession_status.set_text('RENEW')
        else:
            self.lblsession_status.set_text('UNABLE TO RENEW')

    def on_logout(self, emitter):
        self.lblsession_status.set_text('LOGOUT')


    def main(self):
        self.login_manager = LoginManager(CookieInterface(self), 5)
        self.login_manager.on_session_expired.do(self.on_logout)
        print(self.login_manager.session_uid)
        
        global th
        mainContainer = Container(width=800, height=540,style='background-color:#cdf2ff')
        lblTitle = gui.Label("有理數運算",margin="5px",style='position:absolute; left:300px; top:0px')
        lblTitle.style['font-family'] = '隶书'
        lblTitle.style['font-size'] = '30px'
        lblTitle.style['font-color'] = 'rgb(0,0,255)'
        lblTitle.style['font-weight'] = 'bold'

        mainContainer.append(lblTitle)

        lbl1=gui.Label("班级",margin="0px",style='position:absolute; left:10px; top:50px')
        tin1=gui.Input(width=80,height=20,margin="3px",style='position:absolute; left:38px; top:45px')
        mainContainer.append(lbl1)
        mainContainer.append(tin1)

        lbl2=gui.Label("姓名",margin="0px",style='position:absolute; left:150px; top:50px')
        tin2=gui.Input(width=80,height=20,margin="3px",style='position:absolute; left:178px; top:45px')
        mainContainer.append(lbl2)
        mainContainer.append(tin2)

        lbl3=gui.Label("日期",margin="0px",style='position:absolute; left:320px; top:50px')
        self.tin3=gui.Input(width=70,height=20,margin="3px",style='position:absolute; left:348px; top:45px')
        self.tin3.set_read_only(True)
        mainContainer.append(lbl3)
        mainContainer.append(self.tin3)

        lbl4=gui.Label("時間",margin="0px",style='position:absolute; left:440px; top:50px')
        self.tin4=gui.Input(width=60,height=20,margin="3px",style='position:absolute; left:468px; top:45px')
        self.tin4.set_read_only(True)

        mainContainer.append(lbl4)
        mainContainer.append(self.tin4)

        lbl5=gui.Label("總耗時",margin="0px",style='position:absolute; left:562px; top:50px')
        tin5=gui.Input(width=50,height=20,margin="3px",style='position:absolute; left:605px; top:45px')
        tin5.set_value(0)
        tin5.set_read_only(True)
        mainContainer.append(lbl5)
        mainContainer.append(tin5)

        lbl6=gui.Label("總得分",margin="0px",style='position:absolute; left:678px; top:50px')
        tin6=gui.Input(width=50,height=20,margin="3px",style='position:absolute; left:720px; top:45px')
        tin6.set_value(0)
        tin6.set_read_only(True)
        mainContainer.append(lbl6)
        mainContainer.append(tin6)

        lbl7=gui.Label("題型",margin="0px",style='position:absolute; left:345px; top:90px')
        self.tin7=gui.Input(width=40,height=20,margin="3px",style='position:absolute; left:375px; top:85px')
        self.tin7.set_value(0)
        self.tin7.set_read_only(True)
        mainContainer.append(lbl7)
        mainContainer.append(self.tin7)

        lbl8=gui.Label("題號",margin="0px",style='position:absolute; left:458px; top:90px')
        self.tin8=gui.Input(width=40,height=20,margin="3px",style='position:absolute; left:488px; top:85px')
        self.tin8.set_value(0)
        self.tin8.set_read_only(True)
        mainContainer.append(lbl8)
        mainContainer.append(self.tin8)

        self.bt1 = Button('題型1', width=60, height=25,margin="0px",style='position:absolute; left:10px; top:85px')
        self.bt1.onclick.do(self.on_Bt_TX,1)
        mainContainer.append(self.bt1,'bt1')
        self.bt2 = Button('題型2', width=60, height=25,margin="0px",style='position:absolute; left:80px; top:85px')
        self.bt2.onclick.do(self.on_Bt_TX,2)

        mainContainer.append(self.bt2,'bt2')
        self.bt3 = Button('題型3', width=60, height=25,margin="0px",style='position:absolute; left:150px; top:85px')
        self.bt3.onclick.do(self.on_Bt_TX,3)
        mainContainer.append(self.bt3,'bt3')
        self.bt4 = Button('題型4', width=60, height=25,margin="0px",style='position:absolute; left:220px; top:85px')
        self.bt4.onclick.do(self.on_Bt_TX,4)
        mainContainer.append(self.bt4,'bt4')

        SubCtn = HBox(width=780, height=400, style='position: absolute; left: 10px; top:130px; background-color:#fde9d9')
 
        HboxL = Container(width=500, height=380,style='position: absolute; left: 10px; top:130px;background-color:#fde9d9')
        lbl9=gui.Label('命題',mragin="0px",style='position:absolute; left:10px; top:25px')
        tin9=gui.Input(width=240,height=40,style='position:absolute; left:45px; top:15px')
        self.bt9=gui.Button('下一題',width=60, height=25,style='position:absolute; left:350px; top:25px')
        tin9.set_read_only(True)
        self.bt9.onclick.do(self.on_Bt_Th,1)
        HboxL.append([lbl9,tin9,self.bt9])
     
        lbl10=gui.Label('答題',mragin="0px",style='position:absolute; left:10px; top:85px')
        tin10=gui.Input(width=240,height=40,style='position:absolute; left:45px; top:75px')
        self.bt10=gui.Button('确定',width=60, height=25,style='position:absolute; left:350px; top:85px')
        self.bt10.onclick.do(self.Ok)
        HboxL.append([lbl10,tin10,self.bt10])
        lbl11=gui.Label('答案',mragin="0px",style='position:absolute; left:10px; top:145px')
        tin11=gui.Input(width=240,height=40,style='position:absolute; left:45px; top:135px')
        tin11.set_read_only(True)
        self.bt11=gui.Button('提交',width=60, height=25,style='position:absolute; left:350px; top:150px')
        self.bt11.onclick.do(self.submit)
        self.bt12=gui.Button('重置',width=60, height=25,style='position:absolute; left:430px; top:150px')
        self.bt12.onclick.do(self.Reset)
        HboxL.append([lbl11,tin11,self.bt11,self.bt12])
        
        St="说明：\n1.\n2.\n3.\n"
        tin12=gui.Input(width=492,height=184,style='position:absolute; left:10px;top:200px;background-color:#ffffd8')
        tin12.set_value(St)
        tin12.set_read_only(True)
        HboxL.append([tin12])
        SubCtn.append(HboxL)

        HboxR = VBox(width=240, height=380,style='position:absolute; left:510px;top:130px')
        Tb1=gui.Table.new_from_list(content=MarkTb,width='240px',height='380px')        
        HboxR.append(Tb1)
        SubCtn.append(HboxR)
        mainContainer.append(SubCtn)

        self.mainContainer = mainContainer
        self.Tnow(self)
        return self.mainContainer

    # listener function
    def on_Bt_TX(self,widget,tx):
        global Tx
        Tx=tx
        self.tin7.set_value(Tx)

    def on_Bt_Th(self,widget,th):
        self.Tnow(self)
        global Th
        if Th<10 and Tx>0:
           Th+=th
           self.tin8.set_value(Th)

    def Ok(self,widget):
        self.Tnow(self)


    def submit(self,widget):
        self.Tnow(self)


    def Reset(self,widget):
        self.Tnow(self)
        global Th
        Th=0
        self.tin8.set_value(Th)

    def Tnow(self,widget):
        today=datetime.date.today()
        self.tin3.set_value(today)
        now = datetime.datetime.now()
        nowtime=str(now.hour)+":"+str(now.minute)+":"+str(now.second)
        self.tin4.set_value(nowtime)

#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 811, 'config_address': '0.0.0.0', 'config_start_browser': True, 'config_project_name': 'TestMySelf', 'config_resourcepath': './res/'}
 
if __name__ == "__main__":
    start(TestMySelf, address=configuration['config_address'], port=configuration['config_port'], 
                        multiple_instance=configuration['config_multiple_instance'], 
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])

