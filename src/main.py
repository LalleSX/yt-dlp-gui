import gi
import os
import subprocess
import threading
import yt_dlp
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

class YoutubeDLApp(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.main_window = None

    def do_activate(self):
        if not self.main_window:
            self.main_window = YoutubeDLWindow(application=self)
        self.main_window.present()

class YoutubeDLWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title("Youtube-dl GUI")
        self.set_default_size(400, 200)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(vbox)

        label = Gtk.Label(label="Enter video URL:")
        vbox.append(label)

        self.url_entry = Gtk.Entry()
        vbox.append(self.url_entry)

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        download_button = Gtk.Button(label="Download")
        download_button.connect("clicked", self.on_download_button_clicked)
        vbox.append(download_button)

        folder_button = Gtk.Button(label="Choose Output Folder")
        folder_button.connect("clicked", self.show_open_dialog)
        vbox.append(folder_button)

        self.progress_label = Gtk.Label(label="")
        vbox.append(self.progress_label)

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a Folder")

    def on_download_button_clicked(self, button):
        url = self.url_entry.get_text().strip()
        if not url:
            return

        self.progress_label.set_text("Downloading...")
        threading.Thread(target=self.download_video, args=(url,)).start()
        threading.Thread(target=self.download_thumbnail, args=(url,)).start()

    def download_video(self, url):
        output_folder = self.open_dialog.get_file().get_path()
        ydl_opts = {
            "format": "bestaudio" if "music.youtube.com" in url else "best",
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        }
        yt_dlp.YoutubeDL(ydl_opts).download([url])
        success_message = "Download complete!"
        GLib.idle_add(self.progress_label.set_text, success_message)

    def download_thumbnail(self, url):
        output_folder = self.open_dialog.get_file().get_path()
        ydl_opts = {
            "writethumbnail": True,
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        }
        yt_dlp.YoutubeDL(ydl_opts).download([url])

    def show_open_dialog(self, button):
        self.open_dialog.open()

if __name__ == "__main__":
    app = YoutubeDLApp()
    app.run(None)
