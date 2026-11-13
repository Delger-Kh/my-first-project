
# Тавтай морил - Миний анхны төсөл
Энэ бол миний Программ хангамж хөгжүүлэлтийн процесс хичээлийн анхны төсөл.

   ## Багийн гишүүд
   - Э.Энхсаруул (Product Owner)
   - Х.Дэлгэр (Scrum Master)
   - Ч.Оюумаа (Developer)
   

   ## Төслийн зорилго
   Энэ төслөөр бид Scrum аргачлалыг дагаж, жижиг веб аппликейшн хөгжүүлэх болно.

   ## Лаб 8 — Docker (мобайл апп-ын backend)
   Flutter мобайл апп нь Docker дотор ажиллах REST API (FastAPI) руу хүсэлт илгээнэ; өгөгдөл PostgreSQL-д хадгалагдана.

   ```
   docker build -t plant-api:1.0 .
   docker run -d -p 3000:3000 --name plant-api plant-api:1.0   # SQLite-тэй, ганцаараа
   docker compose up -d --build                                # API + PostgreSQL хамт
   ```
   - API баримт: http://localhost:3000/docs
   - Flutter холболт: `mobile/plant_api.dart` (Android emulator → `http://10.0.2.2:3000`)
