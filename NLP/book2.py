import nltk
from gensim.corpora import Dictionary
from gensim.models import LogEntropyModel
from nltk.corpus import stopwords
from PyPDF2 import PdfReader
from gensim.utils import simple_preprocess
from nltk.tokenize import TreebankWordTokenizer

nltk.download('punkt')
nltk.download('stopwords')
stop_words = stopwords.words('russian')


def extract_text_from_pdf(filename):
    text = ""
    pdf = PdfReader(filename)
    for page_number in range(len(pdf.pages)):
        page = pdf.pages[page_number]
        page_text = page.extract_text()
        paragraphs = page_text.split("\n\n")  # Разделение текста на абзацы
        for paragraph in paragraphs:
            text += "\n\n" + paragraph.strip()  # Добавление абзаца с двойным переводом строки
    return text


def preprocess_text(text):
    tokenizer = TreebankWordTokenizer()
    tokens = tokenizer.tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    return words


filename = "Макаров И.М., и др. - Искусственный интеллект и интеллектуальные системы управления-Наука (2006).pdf"
text = extract_text_from_pdf(filename)
text = text.replace("-\r", "")

output_filename = "book_text2.txt"
with open(output_filename, 'w', encoding='utf-8') as output_file:
    output_file.write(text)

with open(output_filename, encoding='utf-8') as doc:
    paragraphs = doc.read().split('\n\n')
    for paragraph_index, paragraph in enumerate(paragraphs, start=1):
        sentences = nltk.sent_tokenize(paragraph)
        words_list = []
        for sentence in sentences:
            processed_words = preprocess_text(sentence)
            print(processed_words)
            words_list.extend(processed_words)  # Добавляем обработанные слова в общий список
        print("--------------------")
        print(f"Список слов для абзаца {paragraph_index}:")
        print(words_list)
        print("--------------------")

        # Создание словаря и корпуса
        dct = Dictionary([words_list])
        corpus = [dct.doc2bow(words_list)]

        # Применение модели логарифмической энтропии к корпусу
        model = LogEntropyModel(corpus)
        vector = model[corpus[0]]
        print(f"Вектор логэнтропии для абзаца {paragraph_index}:")
        print(vector)
        print("--------------------")