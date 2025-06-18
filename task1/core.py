import logging
from pymongo import MongoClient
from typing import Dict

# 📘 Log faylga yoziladi
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='[%(asctime)s] ACTION: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class DataStorage:
    def __init__(
        self,
        uri: str = "mongodb://localhost:27017/",
        db_name: str = "datastore",
        collection_name: str = "storage"
    ):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        logging.info("MongoDB bilan bog‘landi")

    def add(self, key: str, value: str) -> None:
        """Kalit bo‘yicha qiymat qo‘shadi yoki yangilaydi"""
        self.collection.update_one({"key": key}, {"$set": {"value": value}}, upsert=True)
        logging.info(f"Qo‘shildi/Yangilandi — key: {key}, value: {value}")

    def get(self, key: str) -> str:
        """Kalit bo‘yicha qiymatni qaytaradi"""
        doc = self.collection.find_one({"key": key})
        if doc:
            logging.info(f"Oqib olindi — key: {key}")
            return doc["value"]
        else:
            logging.info(f"Topilmadi — key: {key}")
            return "Key not found"

    def delete(self, key: str) -> None:
        """Kalit bo‘yicha qiymatni o‘chiradi"""
        result = self.collection.delete_one({"key": key})
        if result.deleted_count > 0:
            logging.info(f"O‘chirildi — key: {key}")
        else:
            logging.info(f"O‘chirishga urinish, ammo topilmadi — key: {key}")

    def list(self) -> Dict[str, str]:
        """Barcha ma’lumotlarni dict ko‘rinishida qaytaradi"""
        all_data = {doc["key"]: doc["value"] for doc in self.collection.find()}
        logging.info("Barcha ma’lumotlar ro‘yxati olindi")
        return all_data


# 🔎 Test qilish uchun
if __name__ == "__main__":
    store = DataStorage()

    store.add("name", "Sherzamon")
    store.add("job", "Python Developer")
    print(store.get("name"))           # Sherzamon
    print(store.get("unknown"))        # Key not found
    print(store.list())                # {'name': ..., 'job': ...}
    store.delete("name1")
    print(store.list())                # {'job': ...}