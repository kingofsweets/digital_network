from email import message
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import time

global shotdown
global join

join = False

import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()
        
    def send_mess(self):
        key = 8194
        message = self.message_text.text
        crypt = ""
        for i in message:
            crypt += chr(ord(i)^key)
        local = message
        message = crypt
        if message != "":
            self.s.sendto(("["+ self.nickname_text.text + "] :: "+message).encode("utf-8"),self.server)
            self.chat_text.text = self.chat_text.text + '\n'  + 'Вы: ' + local
            self.message_text.text = ''
            
    def make_invis(self, widget):
        widget.visible = False
        widget.size_hint_x = None
        widget.size_hint_y = None
        widget.width = 0
        widget.height = 0
        widget.text = ""
        widget.opacity = 0
        
    def connect_to_server(self):
        if self.nickname_text.text != "":
            host = socket.gethostbyname(socket.gethostname())
            port = 0

            self.server = ("3.10.223.13",9090)

            self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.s.bind((host,port))
            self.s.setblocking(0)
            if 1:
                self.s.sendto(("["+ self.nickname_text.text + "] => join chat ").encode("utf-8"),self.server)
                self.send_btn.disabled = False
                self.message_text.disabled = False
                self.conn_btn.disabled = True
                
                self.make_invis(self.simple)
                self.make_invis(self.conn_btn)
                
                thread = threading.Thread(target=self.receving)
                thread.start()

    
    def receving (self):
        key = 8194
        while True:
            try:
                while True:
                    data, addr = self.s.recvfrom(1024)
                    decrypt = ""; k = False
                    for i in data.decode("utf-8"):
                        if i == ":":
                            k = True
                            decrypt += i
                        elif k == False or i == " ":
                            decrypt += i
                        else:
                            decrypt += chr(ord(i)^key)
                    print(decrypt)
                    self.chat_text.text = self.chat_text.text + '\n' + decrypt
                    time.sleep(0.2)
            except:
                pass
                
        

class WebChat(App):
    def build(self):
        return MyRoot()
    
nn_webchat = WebChat()
nn_webchat.run()