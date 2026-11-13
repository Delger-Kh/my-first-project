# Ургамлын өвчин илрүүлэх систем — мобайл апп-ын backend API (Лаб 8)
# Дараалал нь layer caching-д зориулагдсан: бага өөрчлөгддөг зүйл дээр, их өөрчлөгддөг код доор.

# 1. Суурь image — жижиг хэмжээтэй Python
FROM python:3.12-slim

# Python-ийн .pyc файл бичихгүй, логийг шууд хэвлэнэ (docker logs-д харагдана)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 2. Ажлын хавтас
WORKDIR /app

# 3. Зөвхөн хамаарлын файлыг эхэлж хуулна (layer caching)
#    requirements.txt өөрчлөгдөөгүй бол дараагийн RUN layer кэшээс авна
COPY requirements.txt .

# 4. Хамаарал суулгах — хамгийн удаан алхам, тиймээс кэшлэгдэх ёстой
RUN pip install --no-cache-dir -r requirements.txt

# 5. Үлдсэн кодыг хуулна — код өөрчлөгдөхөд зөвхөн эндээс доош дахин build хийгдэнэ
COPY . .

EXPOSE 3000

# 6. API сервер ажиллуулах (Flutter апп энэ порт руу хүсэлт илгээнэ)
CMD ["uvicorn", "api:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "3000"]
