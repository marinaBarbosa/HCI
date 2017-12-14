from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text,Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import book_model

class BookView(Frame):
    def __init__(self, screen, model):
        super(BookView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          title="Book Details",
                                          reduce_cpu=True)
        
        # Save off the model that accesses the books database.
        self._model = model

        # Create the form for displaying the list of books.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Title:", "title"))
        layout.add_widget(Text("Author:", "author"))
        layout.add_widget(Text("Price:", "price"))
        layout.add_widget(Text("Stock:", "stock"))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(BookView, self).reset()
        self.data = self._model.get_current_book()

    def _ok(self):
        self.save()
        self._model.update_current_book(self.data)
        raise NextScene("Books List")

    @staticmethod
    def _cancel():
        raise NextScene("Books List")
    
class BooksList(Frame):
    
    def __init__(self, screen, model):
        super(BooksList, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       title="BOOKS")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="books",
            on_change=self._on_pick)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Add Book")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["books"]
        raise NextScene("Add Book")

    def _delete(self):
        self.save()
        self._model.delete_book(self.data["books"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise NextScene("Menu")