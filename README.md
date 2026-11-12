# checkbook — Personal Book Library

A mobile app for managing your personal book collection. Keep track of books you've read, are currently reading, or plan to read.

Books can be added manually or by ISBN. Simply scan a book's barcode using your device's camera, and the app will automatically retrieve its title, author, and cover from open book databases.

Built with **Python** and [Flet](https://flet.dev/). Currently available for **Android**, with iOS support planned.

## Features

- **Book collection** — browse and search your library by title, author, or reading status. Supports partial word matching.
- **Reading statuses** — mark books as *Read*, *Planned*, or *Currently Reading*.
- **Book management** — add, edit, and delete books.
- **Ratings & notes** — rate books from 1 to 5 stars and add personal notes, impressions, or quotes.
- **ISBN lookup** — enter an ISBN manually or scan a barcode using your device's camera. Book information is retrieved from Google Books and Open Library.
- **Book covers** — automatically fetch covers online or take your own photos, with built-in cropping.
- **Book spines** — attach photos of book spines, also with cropping support.
- **Light & dark themes** — automatically adapt to your device's system theme.
- **Local storage** — book data is stored in SQLite and persists between app sessions.

## Tech Stack

| Component | Technology |
| --- | --- |
| UI Framework | [Flet 1.1](https://flet.dev/) (Flutter + Python) |
| Camera | flet-camera |
| Barcode Processing | OpenCV (opencv-python) |
| Image Processing | Pillow |
| Database | SQLite (Python's built-in sqlite3) |
| Book Metadata | Google Books API, Open Library API |

## Getting Started

### Prerequisites

- Python 3.14 or later
- Git

### Clone the repository

```bash
git clone https://github.com/KleinerMarcel/Chekbook_app.git
cd CheckBook
```

### Set up a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Install dependencies

```bash
pip install flet flet-camera opencv-python pillow
```

### Run the application

```bash
# Desktop
flet run

# Web browser
flet run --web

# Android
flet run --android

# iOS
flet run --ios
```

To run the app on a mobile device, install the **Flet** app from your device's app store. Make sure your phone and computer are connected to the same Wi-Fi network.

On iOS, you must also allow Flet to access your local network.

## Installing the APK

1. Download the latest APK from the project's [Releases](../../releases) page.
2. Open the downloaded file on your Android device.
3. If prompted, allow installation from unknown sources for the app you're using to open the APK.
4. Grant camera access when prompted on the first launch.

## Data Storage

All data is stored locally on your device.

- **Desktop:** `~/.checkbook/`
  - `books.db` — SQLite database.
  - `photos/` — book cover and spine images.

  To reset your library, simply delete the `.checkbook` directory.

- **Android:** stored in the app's internal storage. Uninstalling the app will also delete its data.

## How ISBN Search Works

1. The app extracts the ISBN from a scanned barcode or manual input, then generates both ISBN-10 and ISBN-13 formats where possible.
2. It searches for the book in Google Books, followed by three different Open Library queries.
3. If the search results don't include a cover image, the app makes an additional request to the Open Library Covers database.
4. If no matching book is found, you can enter its details manually and take a photo of the cover.
