import kivy
import sys
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

kivy.require('1.0.6')  # replace with your current kivy version !
from kivy.app import App

from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '200')


class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='FAN APP ID'))
        self.fan_app_id = TextInput(padding=10, text = "572146392962149")
        self.add_widget(self.fan_app_id)
        self.add_widget(Label(text='FAN ACCESS TOKEN'))
        self.fan_access_token = TextInput(padding=10, text="572146392962149|6FaUn4IDwSOhGCzfDHLZEx9IHko")
        self.add_widget(self.fan_access_token)
        self.add_widget(Button(text='Cancel', on_press=self.cancel_button_callback))
        self.add_widget(Button(text='OK', on_press=self.ok_button_callback))

    def ok_button_callback(self, instance):
        fan_app_id = self.fan_app_id.text
        fan_access_token = self.fan_access_token.text
        print('The FAN APP ID is %s ' % fan_app_id)
        print('The FAN ACCESS TOKEN is %s ' % fan_access_token)
        #FANHelper.get_and_plot_fan_data(fan_app_id, fan_access_token)


    def cancel_button_callback(self, instance):
        print("Cancel Button is pressed. Exiting the Application.")
        sys.exit()


class MyApp(App):
    title = 'FAN Report'
    def build(self):
        return LoginScreen(padding=50)
