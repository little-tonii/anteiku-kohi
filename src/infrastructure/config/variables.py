import os

DATABASE_URL: str = os.getenv("DATABASE_URL")
SECRET_KEY: str = os.getenv("SECRET_KEY")
HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRES: int = int(os.getenv("ACCESS_TOKEN_EXPIRES"))
REFRESH_TOKEN_EXPIRES: int = int(os.getenv("REFRESH_TOKEN_EXPIRES"))
UPLOAD_FOLDER: str = "public/images"