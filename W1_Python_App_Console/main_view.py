from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text,Button, TextBox, Widget, MultiColumnListBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys

class Menu(Frame):
    def __init__(self, screen):
        super(Menu, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       hover_focus=True,
                                       title="BOOK STORE")

        # Create the form for displaying the list of contacts.

        self._edit_button = Button("BOOKS", self._books)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Divider(draw_line=True, height=3))
        layout.add_widget(Button("BOOKS", self._books))
        layout.add_widget(Divider(draw_line=True, height=3))
        layout.add_widget(Button("CLIENTS", self._clients))
        layout.add_widget(Divider(draw_line=True, height=3))        
        layout.add_widget(Button("QUIT", self._quit))
        self.fix()
    
        
    def _books(self):
        raise NextScene("Books List")
    
    def _clients(self):
        raise NextScene("Clients List")    
    
    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")    