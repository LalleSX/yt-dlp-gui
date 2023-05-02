import gi
import subprocess
import threading
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class YTDLPGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="yt-dlp GUI")

        self.set_border_width(10)
        self.set_default_size(300, 200)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.url_label = Gtk.Label(label="URL:")
        vbox.pack_start(self.url_label, True, True, 0)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Enter video URL")
        vbox.pack_start(self.url_entry, True, True, 0)

        self.choose_folder_button = Gtk.Button(label="Choose Destination")
        self.choose_folder_button.connect("clicked", self.on_choose_folder_button_clicked)
        vbox.pack_start(self.choose_folder_button, True, True, 0)

        self.destination_label = Gtk.Label(label="Destination folder:")
        vbox.pack_start(self.destination_label, True, True, 0)

        self.download_button = Gtk.Button(label="Download")
        self.download_button.connect("clicked", self.on_download_button_clicked)
        vbox.pack_start(self.download_button, True, True, 0)

        self.progress_label = Gtk.Label(label="")
        vbox.pack_start(self.progress_label, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)

        self.destination_folder = os.path.expanduser("~")

    def on_choose_folder_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Choose Destination Folder", parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.destination_folder = dialog.get_filename()
            self.destination_label.set_text(f"Destination folder: {self.destination_folder}")

        dialog.destroy()

    def on_download_button_clicked(self, widget):
        url = self.url_entry.get_text()
        if url:
            threading.Thread(target=self.download_video, args=(url,)).start()
        else:
            self.progress_label.set_text("Please enter a URL")

    def download_video(self, url):
        command = ["yt-dlp", "-o", os.path.join(self.destination_folder, "%(title)s.%(ext)s"), url, "--newline"]

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        while True:
            output = process.stdout.readline().strip()
            if output == "" and process.poll() is not None:
                break

            if output.startswith("[download]"):
                percentage = output.split()[-2]
                percentage = float(percentage[:-1]) / 100
                Gdk.threads_enter()
                self.progressbar.set_fraction(percentage)
                self.progress_label.set_text(f"Downloading: {percentage * 100:.1f}%")
                Gdk.threads_leave()

        Gdk.threads_enter()
        self.progressbar.set_fraction(0)
        self.progress_label.set_text("Download completed")
        Gdk.threads_leave()

def main():
    Gdk.threads_init()
    win = YTDLPGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
