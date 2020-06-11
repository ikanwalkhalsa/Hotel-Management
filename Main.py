from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import config

class Login(Screen):
    username=ObjectProperty(None)
    password=ObjectProperty(None)
    Type=None
    def verify(self):
        result=config.db.verify(self.username.text.upper(),self.password.text.upper())
        if result:
            self.Type=config.db.get_type(self.username.text.upper()).lower()
            config.current=self.username.text.upper()
            config.db.log_event('LOGIN',config.current,'',f'{config.current} logged in')

        else:
            self.Type=None
            popup=Popup(title='Try Again!!!',content=Label(text='Invalid username or password!'),size_hint=(None,None),size=(300,100))
            popup.open()

class Guest(Screen):
    history=ObjectProperty(None)
    def order(self):
        Order().open()
    def settings(self):
        Settings().open()
    def show_history(self):
        self.history.opacity=100
        ordr=config.db.get_history(config.current)
        self.history.text='Order History \n'+ordr

class Employee(Screen):
    search=ObjectProperty(None)
    result=ObjectProperty(None)
    def settings(self):
        Settings().open()
    def checkin(self):
        if config.db.available() is not None:
            Checkin().open()
        else:
            popup=Popup(title='Checkin',content=Label(text='Rooms not available!'),size_hint=(None,None),size=(300,100))
            popup.open()
    def checkout(self):
        Checkout().open()
    def Search(self):
        self.result.text=config.db.search(self.search.text.upper(),'guest')

class Admin(Screen):
    search=ObjectProperty(None)
    result=ObjectProperty(None)
    def settings(self):
        Settings().open()
    def info(self):
        inf=config.db.info()
        popup=Popup(title='INFO',content=Label(text=inf),size_hint=(None,None),size=(250,200))
        popup.open()
    def hire(self):
        Hire().open()
    def fire(self):
        Fire().open()
    def Search(self):
        self.result.text=config.db.search(self.search.text.upper(),)
    def view_logs(self):
        self.result.text=config.db.show_logs()

class WindowManager(ScreenManager):
    pass

class Settings(Popup):
    user=config
    pwd=ObjectProperty(None)
    def submit(self):
        config.db.change_password(self.user.current,self.pwd.text.upper())

class Order(Popup):
    ic=ObjectProperty(None)
    drinks=ObjectProperty(None)
    user=config
    def submit(self):
        event=f'{config.current} placed an order'
        odr ="Ice Creams X "+self.ic.text+"\nCold Drinks X "+self.drinks.text
        config.db.log_event('ORDER',self.user.current,odr,event)

class Checkin(Popup):
    name=ObjectProperty(None)
    avail=ObjectProperty(None)
    room=config.db.available()[0] if config.db.available() is not None else ''
    def submit(self):
        config.db.checkin(self.avail.text.upper(),self.name.text.upper())
        config.db.log_event('CHECKIN',self.avail.text.upper(),'',f'{self.name.text} checked into {self.avail.text}')

class Checkout(Popup):
    name=ObjectProperty(None)
    room=ObjectProperty(None)
    def submit(self):
        config.db.checkout(self.room.text.upper(),self.name.text.upper())
        config.db.log_event('CHECKOUT',self.room.text.upper(),'',f'{self.name.text} checked out from {self.room.text}')

class Hire(Popup):
    name=ObjectProperty(None)
    eid=ObjectProperty(None)
    def submit(self):
        config.db.hire(self.eid.text.upper(),self.name.text.upper())
        config.db.log_event('HIRE','ADMIN','',f'You hired {self.name.text} as {self.eid.text}')


class Fire(Popup):
    name=ObjectProperty(None)
    eid=ObjectProperty(None)
    def submit(self):
        config.db.fire(self.eid.text.upper(),self.name.text.upper())
        config.db.log_event('HIRE','ADMIN','',f'You fired {self.name.text} as {self.eid.text}')

kv=Builder.load_file('Design.kv')

class HotelApp(App):
    Window.size=(config.WIDTH,config.HEIGHT)
    def build(self):
        return kv

if __name__ == "__main__":
    HotelApp().run()