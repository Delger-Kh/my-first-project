import os
import tempfile

# Тестэд PostgreSQL биш түр SQLite файл ашиглана (CI дээр ч ажиллана)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.mkdtemp()}/test.db")
