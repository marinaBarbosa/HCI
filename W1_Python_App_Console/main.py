from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text,Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import sqlite3

import book_model
import book_view

import client_view
import client_model

import main_view

def demo(screen, scene):
    scenes = [
        Scene([main_view.Menu(screen)], -1, name="Menu"),
        
        Scene([book_view.BooksList(screen, books)], -1, name="Books List"),
        Scene([book_view.BookView(screen, books)], -1, name="Add Book"),
        
        Scene([client_view.ClientsList(screen, clients)], -1, name="Clients List"),
        Scene([client_view.ClientView(screen, clients)], -1, name="Add Client"),        
      
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)

books = book_model.BookModel()
clients = client_model.ClientModel()

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene