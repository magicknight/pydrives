#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Button(text='Google Drive'))
        self.add_widget(Button(text='DropBox'))
        self.add_widget(Button(text='The Box'))



class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()

