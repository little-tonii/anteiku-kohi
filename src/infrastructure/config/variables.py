import os

DATABASE_URL: str = str(os.getenv("DATABASE_URL"))
REDIS_URL: str = str(os.getenv("REDIS_URL"))
SECRET_KEY: str = str(os.getenv("SECRET_KEY"))
HASH_ALGORITHM: str = str(os.getenv("HASH_ALGORITHM"))
ACCESS_TOKEN_EXPIRES: int = int(str(os.getenv("ACCESS_TOKEN_EXPIRES")))
REFRESH_TOKEN_EXPIRES: int = int(str(os.getenv("REFRESH_TOKEN_EXPIRES")))
UPLOAD_FOLDER: str = "public/images"
ANTEIKU_KOHI_EMAIL: str = str(os.getenv("ANTEIKU_KOHI_EMAIL"))
ANTEIKU_KOHI_EMAIL_APP_PASSWORD: str = str(os.getenv("ANTEIKU_KOHI_EMAIL_APP_PASSWORD"))
EMAIL_SALT_VERIFYCATION: str = str(os.getenv("EMAIL_SALT_VERIFYCATION"))

VNPAY_RETURN_URL: str = str(os.getenv("VNPAY_RETURN_URL"))
VNPAY_PAYMENT_URL: str = str(os.getenv("VNPAY_PAYMENT_URL"))
VNPAY_API_URL: str = str(os.getenv("VNPAY_API_URL"))
VNPAY_TMN_CODE: str = str(os.getenv("VNPAY_TMN_CODE"))
VNPAY_HASH_SECRET_KEY: str = str(os.getenv("VNPAY_HASH_SECRET_KEY"))

TARGET_IMAGE_SIZE = 1080
IMAGE_QUALITY = 85
