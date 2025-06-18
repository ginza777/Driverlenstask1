import os
import shutil
import logging
from typing import List, Tuple

# Конфигурация логгера
logging.basicConfig(
    filename="file_processor.log",  # Имя файла логов
    level=logging.INFO,  # Уровень логирования: INFO
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщений лога
)
logger = logging.getLogger(__name__)


class FileProcessor:
    @staticmethod
    def copy_directory(source_dir: str, target_dir: str) -> None:
        try:
            if not os.path.exists(source_dir):
                logger.error(f"Source directory '{source_dir}' does not exist.")
                raise FileNotFoundError(f"Source directory '{source_dir}' does not exist.")

            os.makedirs(target_dir, exist_ok=True)
            logger.info(f"Target directory '{target_dir}' is ready.")

            for root, dirs, files in os.walk(source_dir):
                relative_path = os.path.relpath(root, source_dir)
                current_target_dir = os.path.join(target_dir, relative_path)
                os.makedirs(current_target_dir, exist_ok=True)

                # Копируем файлы
                for file in files:
                    source_file_path = os.path.join(root, file)
                    target_file_path = os.path.join(current_target_dir, file)
                    shutil.copy2(source_file_path, target_file_path)
                    logger.info(f"Copied file '{source_file_path}' to '{target_file_path}'.")

            logger.info(f"Successfully copied contents from '{source_dir}' to '{target_dir}'.")

        except Exception as e:
            logger.error(f"An error occurred while copying directory: {str(e)}")
            raise

    @staticmethod
    def process_files(directory: str, extensions: List[str]) -> List[Tuple[str, int]]:
        result = []
        try:
            if not os.path.exists(directory):
                logger.error(f"Directory '{directory}' does not exist.")
                raise FileNotFoundError(f"Directory '{directory}' does not exist.")

            for root, _, files in os.walk(directory):
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                line_count = sum(1 for _ in f)
                            result.append((file, line_count))
                            logger.info(f"Processed file '{file_path}' with {line_count} lines.")
                        except Exception as e:
                            logger.error(f"Could not process file '{file_path}': {str(e)}")

            logger.info(f"Processed files in directory '{directory}' with extensions {extensions}.")

        except Exception as e:
            logger.error(f"An error occurred during file processing: {str(e)}")
            raise

        return result





source_dir = "/Users/admin/Desktop/DriverLens/task4/source"
target_dir = "/Users/admin/Desktop/DriverLens/task4/target"

# Копируем содержимое директории с логированием
try:
    FileProcessor.copy_directory(source_dir, target_dir)
except Exception as e:
    print(f"Ошибка при копировании: {e}")

# Обрабатываем файлы в директории с указанными расширениями
directory = "/Users/admin/Desktop/DriverLens/task4"
extensions = [".txt", ".log"]

try:
    results = FileProcessor.process_files(directory, extensions)
    print("Обработанные файлы:", results)
except Exception as e:
    print(f"Ошибка при обработке файлов: {e}")
