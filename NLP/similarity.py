import random

import gensim
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader


def extract_text_from_pdf(filename, num_random_paragraphs=None, random_paragraph_length=None):
    text = ""
    pdf = PdfReader(filename)
    for page_number in range(len(pdf.pages)):
        page = pdf.pages[page_number]
        page_text = page.extract_text()
        paragraphs = page_text.split("\n\n")  # Разделение текста на абзацы
        for paragraph in paragraphs:
            text += "\n\n" + paragraph.strip()  # Добавление абзаца с двойным переводом строки

    # Добавление случайных абзацев
    if num_random_paragraphs is not None and random_paragraph_length is not None:
        for _ in range(num_random_paragraphs):
            random_paragraph = " ".join(random.choices(dictionary.token2id, k=random_paragraph_length))
            text += "\n\n" + random_paragraph.strip()

    return text


# Создание списка имен файлов
documents = [
    "Брайтон Генри - Искусственный интеллект в комиксах.pdf",
    "Макаров И.М., и др. - Искусственный интеллект и интеллектуальные системы управления-Наука (2006).pdf"
]

# Предобработка и обучение модели
tokenized_docs = [word_tokenize(extract_text_from_pdf(doc)) for doc in documents]
dictionary = gensim.corpora.Dictionary(tokenized_docs)
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

# Создание модели TF-IDF
tfidf = TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# Создание матрицы сходства
similarity_matrix = MatrixSimilarity(corpus_tfidf)

# Выбор случайного абзаца для первого документа
random_paragraph_1 = random.choice(tokenized_docs[0])

# Выбор случайного абзаца для второго документа
random_paragraph_2 = random.choice(tokenized_docs[1])

# Предобработка случайных абзацев
random_paragraph_1_bow = dictionary.doc2bow(random_paragraph_1)
random_paragraph_2_bow = dictionary.doc2bow(random_paragraph_2)
random_paragraph_1_tfidf = tfidf[random_paragraph_1_bow]
random_paragraph_2_tfidf = tfidf[random_paragraph_2_bow]

# Вычисление сходства для случайных абзацев
similarity_scores_1 = similarity_matrix[random_paragraph_1_tfidf]
similarity_scores_2 = similarity_matrix[random_paragraph_2_tfidf]

# Вывод результатов
print("Случайный абзац из первого документа:")
print(f"Абзац: {' '.join(random_paragraph_1)}")
print("Сходство:")
for idx, score in enumerate(similarity_scores_1):
    print(f"Документ: {documents[idx]} | Сходство: {score}")
print("--------------------")

print("\nСлучайный абзац из второго документа:")
print(f"Абзац: {' '.join(random_paragraph_2)}")
print("Сходство:")
for idx, score in enumerate(similarity_scores_2):
    print(f"Документ: {documents[idx]} | Сходство: {score}")
print("--------------------")