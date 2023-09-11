import os.path
import re
import PyPDF2
import nltk
from PyPDF2.errors import PdfReadError
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog
from gensim.corpora import Dictionary
from gensim.models import LogEntropyModel
import matplotlib.pyplot as plt

nltk.download('stopwords')


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    filtered_text = ' '.join(filtered_words)

    return filtered_text


def process_word_list(text):
    pages = text.strip().split('\n\n')

    for i, page in enumerate(pages, start=1):
        print(f"Страница {i}:")
        words = re.findall(r'\b\w+\b', page)
        filtered_words = [word for word in words if word not in stop_words]
        formatted_words = [f"[{word}]" for word in filtered_words]
        print(", ".join(formatted_words))
        print()


def process_log_entropy(text):
    words = re.findall(r'\b\w+\b', text)
    stop_words_removed = [word for word in words if word not in stop_words]
    dictionary = Dictionary([stop_words_removed])
    corpus = [dictionary.doc2bow(stop_words_removed)]
    log_entropy_model = LogEntropyModel(corpus)
    entropy_vector = log_entropy_model[corpus[0]]
    entropy_words = [(dictionary[index], value) for index, value in entropy_vector]

    return entropy_words


def show_word_info_bar(entropy_words):
    entropy_words = sorted(entropy_words, key=lambda x: x[1], reverse=True)[:10]
    words = [word for word, _ in entropy_words]
    entropy = [entropy for _, entropy in entropy_words]

    plt.barh(range(len(words)), entropy)
    plt.yticks(range(len(words)), words)
    plt.xlabel('Лог-энтропия')
    plt.ylabel('Слова')
    plt.title('Топ 10 значимых слов в тексте')
    plt.show()


def show_word_info_vector(entropy_words):
    for word, entropy in entropy_words:
        print(f"{word}: {entropy}")

def display_text_statistics(text):
    pages = [page.strip() for page in text.strip().split('\n\n') if page.strip()]
    num_pages = len(pages)
    num_total_words = 0
    word_freq = nltk.FreqDist()

    for page in pages:
        preprocessed_page = preprocess_text(page)
        words = preprocessed_page.split()
        num_words = len(words)
        num_total_words += num_words
        word_freq.update(words)

    most_common_words = word_freq.most_common(5)

    print(f"Количество страниц: {num_pages}")
    print(f"Количество слов: {num_total_words}")
    print("Наиболее часто встречающиеся слова:")
    for word, freq in most_common_words:
        print(f"{word}: {freq}")


def write_to_file(total_text, choice):
    pages = [page.strip() for page in total_text.strip().split('\n\n') if page.strip()]
    for i, page in enumerate(pages, start=1):
        print(f"Страница {i}:")
        print(page.strip())
        print()


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        print(f"Вы выбрали файл: {file_name}")
    return file_path


def add_new_book():
    total_text = ""
    file_path = select_file()
    while file_path:
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfFileReader(pdf_file)
                num_pages = reader.getNumPages()
                for i in range(num_pages):
                    page = reader.getPage(i)
                    text = page.extractText()
                    if text.strip():
                        total_text += text + '\n\n'
            break
        except PdfReadError as e:
            print("Ошибка чтения файла PDF:", str(e))
            print("Выберите другой файл:")
            file_path = select_file()
    return total_text



stop_words = set(stopwords.words('russian'))

print("Выберите файл:")
total_text = add_new_book()
while True:
    print("Выберите действие:")
    print("1. Вывести содержимое книги")
    print("2. Вывести статистику текста")
    print("3. Вывести список слов книги")
    print("4. Вывести график лог-энтропии")
    print("5. Вывести вектор лог-энтропии")
    print("6. Выбрать другой файл")
    print("7. Выйти")

    choice = input("Введите номер действия: ")

    if choice == "1":
        write_to_file(total_text, choice)
    elif choice == "2":
        display_text_statistics(total_text)
    elif choice == "3":
        process_word_list(total_text)
    elif choice == "4":
        entropy_words = process_log_entropy(total_text)
        show_word_info_bar(entropy_words)
    elif choice == "5":
        entropy_words = process_log_entropy(total_text)
        with open("log_entropy_vector.txt", "w", encoding="utf-8") as file:
            for word, entropy in entropy_words:
                file.write(f"{word}: {entropy}\n")
        print("Вектор лог-энтропии записан в файл log_entropy_vector.txt")
        show_word_info_vector(entropy_words)
    elif choice == "6":
        total_text = add_new_book()
    elif choice == "7":
        break
    else:
        print("Неверный номер действия. Попробуйте снова.")