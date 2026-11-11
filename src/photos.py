import io
import time

from PIL import Image, ImageOps

from storage import data_dir


def save_photo(data: bytes, prefix: str) -> str:
    """Сохраняет фото (корешок или обложку) в папку приложения, возвращает путь."""
    folder = data_dir() / "photos"
    folder.mkdir(exist_ok=True)
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    image.thumbnail((1200, 1200))
    path = folder / f"{prefix}_{time.time_ns()}.jpg"
    image.save(path, "JPEG", quality=85)
    return str(path)