from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy_webview import WebView
import pyttsx3
import os

v = pyttsx3.init()

class HTMLLoginEditorApp(App):
    def build(self):
        self.layout = FloatLayout()
        self.selected_file = None
        self.create_login_screen()
        return self.layout

    def create_login_screen(self):
        self.layout.clear_widgets()

        # User Label
        self.user_label = Label(
            text="User Name:",
            size_hint=(.2, .05),
            pos_hint={"center_x": 0.25, "center_y": 0.7},
            font_size=18
        )
        self.layout.add_widget(self.user_label)

        # User Input
        self.username_input = TextInput(
            hint_text="Enter your name",
            multiline=False,
            size_hint=(.5, .08),
            pos_hint={"center_x": 0.6, "center_y": 0.7},
            font_size=20
        )
        self.layout.add_widget(self.username_input)

        # Panel Label
        self.panel_label = Label(
            text="Panel Name:",
            size_hint=(.2, .05),
            pos_hint={"center_x": 0.25, "center_y": 0.55},
            font_size=18
        )
        self.layout.add_widget(self.panel_label)

        # Panel Input
        self.panel_input = TextInput(
            hint_text="Enter panel name",
            multiline=False,
            size_hint=(.5, .08),
            pos_hint={"center_x": 0.6, "center_y": 0.55},
            font_size=20
        )
        self.layout.add_widget(self.panel_input)

        # Submit Button
        submit_btn = Button(
            text="Submit",
            size_hint=(.3, .1),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            on_press=self.verify_login
        )
        self.layout.add_widget(submit_btn)

    def verify_login(self, instance):
        username = self.username_input.text.strip()
        panel = self.panel_input.text.strip()

        if username == "admin" and panel == "admin":
            v.say("Login successful")
            v.runAndWait()
            self.create_html_editor()
        else:
            msg = f"Invalid login: {username}/{panel}"
            v.say(msg)
            v.runAndWait()

    def create_html_editor(self):
        self.layout.clear_widgets()

        # HTML Text Editor
        self.html_editor = TextInput(
            text="",
            multiline=True,
            font_size=16,
            size_hint=(0.9, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        self.layout.add_widget(self.html_editor)

        # Load HTML File Button
        load_button = Button(
            text="LOAD HTML",
            size_hint=(0.28, 0.1),
            pos_hint={"center_x": 0.2, "center_y": 0.15},
            on_press=self.open_filechooser
        )
        self.layout.add_widget(load_button)

        # Save HTML File Button
        save_button = Button(
            text="SAVE HTML",
            size_hint=(0.28, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            on_press=self.save_file
        )
        self.layout.add_widget(save_button)

        # Create New File Button
        new_button = Button(
            text="CREATE NEW FILE",
            size_hint=(0.28, 0.1),
            pos_hint={"center_x": 0.8, "center_y": 0.15},
            on_press=self.create_new_file_popup
        )
        self.layout.add_widget(new_button)

        # RUN Button (WebView preview)
        run_button = Button(
            text="RUN",
            size_hint=(0.28, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.03},
            on_press=self.run_file
        )
        self.layout.add_widget(run_button)

    def open_filechooser(self, instance):
        content = FloatLayout()
        chooser = FileChooserListView(
            size_hint=(1, 0.8),
            pos_hint={"x": 0, "y": 0.2},
            filters=["*.html"]
        )
        content.add_widget(chooser)

        select_btn = Button(
            text="Select File",
            size_hint=(1, 0.2),
            pos_hint={"x": 0, "y": 0}
        )
        content.add_widget(select_btn)

        popup = Popup(title="Choose HTML File", content=content,
                      size_hint=(0.9, 0.9))

        def on_file_select(*args):
            if chooser.selection:
                self.selected_file = chooser.selection[0]
                try:
                    with open(self.selected_file, 'r', encoding='utf-8') as f:
                        self.html_editor.text = f.read()
                        v.say("HTML file loaded")
                        v.runAndWait()
                except Exception as e:
                    self.html_editor.text = f"Error loading file:\n{e}"
                popup.dismiss()

        select_btn.bind(on_press=on_file_select)
        popup.open()

    def save_file(self, instance):
        if self.selected_file:
            try:
                with open(self.selected_file, 'w', encoding='utf-8') as f:
                    f.write(self.html_editor.text)
                    v.say("File saved successfully")
                    v.runAndWait()
            except Exception as e:
                self.html_editor.text += f"\n\nError saving file:\n{e}"
        else:
            v.say("No file selected")
            v.runAndWait()

    def create_new_file_popup(self, instance):
        popup_layout = FloatLayout()

        filename_input = TextInput(
            hint_text="Enter new file name (e.g., newfile.html)",
            multiline=False,
            size_hint=(0.9, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        popup_layout.add_widget(filename_input)

        create_btn = Button(
            text="Create",
            size_hint=(0.9, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.3}
        )
        popup_layout.add_widget(create_btn)

        popup = Popup(title="Create New HTML File",
                      content=popup_layout,
                      size_hint=(0.8, 0.5))

        def create_file(instance):
            filename = filename_input.text.strip()
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>New File</title>\n</head>\n<body>\n\n</body>\n</html>")
                    self.selected_file = filename
                    self.html_editor.text = "<!DOCTYPE html>\n<html>\n<head>\n<title>New File</title>\n</head>\n<body>\n\n</body>\n</html>"
                    v.say("New file created")
                    v.runAndWait()
                    popup.dismiss()
                except Exception as e:
                    self.html_editor.text = f"Failed to create file:\n{e}"
            else:
                v.say("Please enter file name")
                v.runAndWait()

        create_btn.bind(on_press=create_file)
        popup.open()

    def run_file(self, instance):
        if self.selected_file and os.path.exists(self.selected_file):
            popup = Popup(title="HTML Preview",
                          size_hint=(0.95, 0.95))
            webview = WebView(url="file://" + os.path.abspath(self.selected_file))
            popup.content = webview
            popup.open()
            v.say("Running preview")
            v.runAndWait()
        else:
            v.say("No file selected to run")
            v.runAndWait()


if __name__ == '__main__':
    HTMLLoginEditorApp().run()
