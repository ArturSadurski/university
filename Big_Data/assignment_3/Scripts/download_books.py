import requests
from bs4 import BeautifulSoup
import os


def get_top_books(url):
    """Pobiera listę najpopularniejszych ID książek z podanego URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)
    book_ids = []

    for link in links:
        href = link["href"]
        if href.startswith("/ebooks/"):
            book_id = href.split("/")[2]
            if book_id.isdigit():
                book_ids.append(book_id)

    return book_ids


def download_book(book_id, target_directory):
    """Pobiera książkę w formacie '.txt.utf-8' jeśli dostępna."""
    url = f"https://www.gutenberg.org/ebooks/{book_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)
    txt_link = None

    # Szukaj linku do pliku tekstowego
    for link in links:
        if link["href"].endswith(".txt.utf-8"):
            txt_link = f"https://www.gutenberg.org{link['href']}"
            break

    if txt_link:
        try:
            print(f"Trying to download book ID: {book_id} from {txt_link}")
            response = requests.get(txt_link)
            if response.status_code == 200:
                file_name = f"{book_id}.txt"
                file_path = os.path.join(target_directory, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded {file_path}")
            else:
                print(
                    f"Failed to download {txt_link}, status code: {response.status_code}"
                )
        except Exception as e:
            print(f"Error downloading book ID {book_id}: {str(e)}")
    else:
        print(f"No text file found for book ID {book_id}")


def download_books(book_ids, target_directory):
    """Pobiera książki na podstawie listy ID."""
    os.makedirs(target_directory, exist_ok=True)
    for book_id in book_ids:
        download_book(book_id, target_directory)


top_books_url = "https://www.gutenberg.org/browse/scores/top"
download_directory = (
    "/home/artur_176/university/Big_Data/assignment_3/Scripts/downloaded_books"
)
top_book_ids = get_top_books(top_books_url)

download_books(top_book_ids, download_directory)


download_books(download_directory)
