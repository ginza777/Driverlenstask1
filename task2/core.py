import logging
import re
from collections import Counter
from typing import List, Tuple

# 📘 Log fayl sozlamalari
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='[%(asctime)s] ACTION: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def find_top_k_frequent_words(text: str, k: int) -> List[Tuple[str, int]]:
    """
    Kiritilgan matndan eng ko‘p uchraydigan k ta so‘z va ularning chastotasini qaytaradi.
    Agar noyob so‘zlar soni k dan kam bo‘lsa — bo‘sh ro‘yxat qaytariladi.
    """

    # 🔤 Matnni tozalash va kichik harflarga o'tkazish
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    words = cleaned_text.split()
    word_counts = Counter(words)

    # ❗️ Shart: agar noyob so‘zlar k dan kam bo‘lsa — bo‘sh list
    if len(word_counts) < k:
        logging.info(
            f"Top {k} so‘z so‘raldi, ammo faqat {len(word_counts)} noyob so‘z mavjud. [] qaytarildi."
        )
        return []

    top_k = word_counts.most_common(k)
    logging.info(f"Top {k} eng ko‘p so‘zlar: {top_k}")
    return top_k


# 🧪 Test qilish uchun
if __name__ == "__main__":
    text = "Hello world! Hello everyone. This is a simple test.txt. Test, test.txt, hello. hello"
    k = 2

    result = find_top_k_frequent_words(text, k)
    print("Результат:", result)