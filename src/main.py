import gi
import os
import subprocess
import threading
import yt_dlp
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

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

        download_button = Gtk.Button(label="Download")
        download_button.connect("clicked", self.on_download_button_clicked)
        vbox.append(download_button)

        self.progress_label = Gtk.Label(label="")
        vbox.append(self.progress_label)


    def on_download_button_clicked(self, button):
        url = self.url_entry.get_text().strip()
        if not url:
            return

        self.progress_label.set_text("Downloading...")
        threading.Thread(target=self.download_video, args=(url,)).start()
        threading.Thread(target=self.download_thumbnail, args=(url,)).start()
        
    
    def download_video(self, url):
        # If music.youtube.com is the URL then download the best audio only
        if "music.youtube.com" in url:
            yt_dlp.YoutubeDL({"format": "bestaudio"}).download([url])
            success_message = "Download complete!"
        else:
            # Download the best video and audio
            yt_dlp.YoutubeDL().download([url])
            success_message = "Download complete!"
        GLib.idle_add(self.progress_label.set_text, success_message)

    def download_thumbnail(self, url):
        # Download thumbnail
        yt_dlp.YoutubeDL({"writethumbnail": True}).download([url])

if __name__ == "__main__":
    app = YoutubeDLApp()
    app.run(None)
