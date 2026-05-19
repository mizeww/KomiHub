# --- НАСТРОЙКИ MINIO ---
MINIO_ENDPOINT = 'http://localhost:9000'
BUCKET_NAME = 'komihub'
ACCESS_KEY = 'WWZQSC7RO7L0H6P34PSW'  # <--- Вставьте сюда ваш Access Key
SECRET_KEY = 'vdBzCPlmlddIIPjliL65p+yAeSRFXvzjnKzIE+5a'  # <--- Вставьте сюда ваш Secret Key
import asyncio
import aiohttp
import boto3
from io import BytesIO
from PIL import Image
from aiolimiter import AsyncLimiter
from ddgs import DDGS
from app import create_app, db
from app.models.words import Word
from app.models import db_session

# Лимитер скорости: 2 запроса в секунду, чтобы DuckDuckGo не выдал капчу
rate_limiter = AsyncLimiter(max_rate=2, time_period=1)

# Инициализация S3 клиента для MinIO
s3_client = boto3.client(
    's3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='us-east-1'
)


def upload_to_minio(buffer, filename):
    """Синхронная отправка байтов в бакет MinIO"""
    s3_path = f"products/{filename}"
    s3_client.upload_fileobj(
        buffer,
        BUCKET_NAME,
        s3_path,
        ExtraArgs={'ContentType': 'image/webp'}
    )
    return f"{MINIO_ENDPOINT}/{BUCKET_NAME}/{s3_path}"


def convert_to_webp(img_bytes):
    """Сжатие изображения для жесткой экономии места на диске"""
    try:
        img = Image.open(BytesIO(img_bytes))
        if img.width > 800:
            output_size = (800, int(img.height * (800 / img.width)))
            img = img.resize(output_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=75)
        buffer.seek(0)
        return buffer
    except Exception:
        return None


def fetch_ddg_image(ru_name):
    """Синхронный поиск картинки через актуальный класс DDGS"""
    try:
        with DDGS() as ddgs:
            # Передаем строку напрямую первым аргументом без ключевых слов.
            # Дополнительно передаем max_results КАК КЛЮЧЕВОЙ аргумент.
            results = ddgs.images(ru_name, max_results=3)

            # Проверяем, что ответ — это непустой список
            if results and isinstance(results, list) and len(results) > 0:
                # results[0] — это первый словарь в списке. У него берем ключ 'image'.
                return results[0].get('image')
    except Exception as e:
        print(f"Ошибка DDG для слова '{ru_name}': {e}")
    return None

async def download_and_upload(session, word_id, ru_name, loop, app):
    """Основной конвейер обработки одного слова"""
    await rate_limiter.acquire()

    try:

        search_query = f"{ru_name}"
        img_url = await loop.run_in_executor(None, fetch_ddg_image, search_query)

        if not img_url:
            print(f"🤔 Нет картинок в поиске для: {search_query}")
            return

        # 2. Скачиваем байты изображения с таймаутом
        async with session.get(img_url, timeout=10) as img_resp:
            if img_resp.status != 200:
                return
            img_bytes = await img_resp.read()

        # 3. Сжимаем в WebP
        buffer = await loop.run_in_executor(None, convert_to_webp, img_bytes)
        if not buffer:
            return

        # 4. Загружаем в локальное облако MinIO
        filename = f"word_{word_id}.webp"
        public_url = await loop.run_in_executor(None, upload_to_minio, buffer, filename)

        db_sess = db_session.create_session()
        try:
            # Ищем запись по ID через твою систему сессий модели Word
            word_entry = db_sess.query(Word).filter(Word.id == word_id).first()
            if word_entry:
                word_entry.image_url = public_url
                db_sess.commit()
                print(f"✅ ID {word_id} [{search_query}] -> Успешно сохранено в БД и MinIO")
        except Exception as db_err:
            print(f"🛑 Ошибка записи в БД для ID {word_id}: {db_err}")
            db_sess.rollback()  # Откатываем транзакцию при сбое
        finally:
            db_sess.close()  # ГАРАНТИРОВАННО СНИМАЕМ БЛОКИРОВКУ С ФАЙЛА SQLite
        # =====================================================================

    except Exception as e:
        # Игнорируем внешние сетевые падения сторонних сайтов при скачивании самих картинок
        pass


async def main():
    app = create_app()

    # Открываем сессию через ваш кастомный db_session менеджер
    db_sess = db_session.create_session()
    try:
        # Выбираем слова из базы, где ссылка на картинку пустая (None или пустая строка)
        words_from_db = db_sess.query(Word).filter((Word.image_url == 'None') | (Word.image_url == "")).all()
        print(f"Найдено слов без картинок в базе данных: {len(words_from_db)}")
        items_data = [(w.id, w.value) for w in words_from_db]
    finally:
        db_sess.close()  # Обязательно закрываем сессию чтения

    if not items_data:
        print("Все картинки уже успешно загружены!")
        return

    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        loop = asyncio.get_running_loop()
        tasks = [
            download_and_upload(session, word_id, name, loop, app)
            for word_id, name in items_data
        ]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
