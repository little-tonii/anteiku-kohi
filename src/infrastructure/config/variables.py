import os

DATABASE_URL: str = str(os.getenv("DATABASE_URL"))
SECRET_KEY: str = str(os.getenv("SECRET_KEY"))
HASH_ALGORITHM: str = str(os.getenv("HASH_ALGORITHM"))
ACCESS_TOKEN_EXPIRES: int = int(str(os.getenv("ACCESS_TOKEN_EXPIRES")))
REFRESH_TOKEN_EXPIRES: int = int(str(os.getenv("REFRESH_TOKEN_EXPIRES")))
UPLOAD_FOLDER: str = "public/images"
