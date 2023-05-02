# yt-dlp GUI

A simple and easy-to-use graphical user interface (GUI) for [yt-dlp](https://github.com/yt-dlp/yt-dlp), a powerful video downloader and converter.

## Features

- Download videos from various platforms with a user-friendly interface.
- Set destination folder for downloaded videos.
- Monitor the download progress with a progress bar.

## Installation

### Prerequisites

- Python 3.6 or later
- [yt-dlp](https://github.com/yt-dlp/yt-dlp#installation) command line utility
- GTK 3.0+ and its Python bindings

#### Installing yt-dlp

Follow the [official instructions](https://github.com/yt-dlp/yt-dlp#installation) to install yt-dlp on your system.

#### Installing GTK and Python bindings

For Debian-based systems:

```bash
sudo apt-get install libgtk-3-dev python3-gi
```

For Fedora-based systems:

```bash
sudo dnf install gtk3-devel python3-gobject
```

For Arch-based systems:

```bash
sudo pacman -S gtk3 python-gobject
```

### Clone the repository

```bash
git clone https://github.com/lallesx/yt-dlp-gui.git
```

### Run the application

```bash
cd yt-dlp-gui
python3 ytdlp_gui.py
```

## License

This project is released under the [GPL](LICENSE).

## Contributing

Feel free to submit issues, feature requests, and pull requests to help improve the project.