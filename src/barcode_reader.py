from isbn import clean_isbn

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

try:  # необязательный декодер для проверки на компьютере
    import zxingcpp
except ImportError:
    zxingcpp = None

MAX_SIDE = 1600


def _as_isbn(code: str) -> str | None:
    isbn = clean_isbn(code)
    if isbn and (len(isbn) == 10 or isbn.startswith(("978", "979"))):
        return isbn
    return None


def _variants(image):
    """Разные версии кадра: так штрихкод находится заметно чаще."""
    h, w = image.shape[:2]
    scale = MAX_SIDE / max(h, w)
    if scale < 1:
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        h, w = image.shape[:2]
    center = image[int(h * 0.2):int(h * 0.8), int(w * 0.05):int(w * 0.95)]
    for img in (center, image):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        yield gray
        yield cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE)  # штрихкод держат вертикально
        yield cv2.resize(gray, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
        yield cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)


def decode_isbn(data: bytes) -> str | None:
    """Ищет штрихкод ISBN на фото (байты JPEG). Возвращает ISBN или None."""
    if cv2 is None:
        return None
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return None

    detector = cv2.barcode.BarcodeDetector() if hasattr(cv2, "barcode") else None
    for img in _variants(image):
        if zxingcpp:
            try:
                for r in zxingcpp.read_barcodes(img):
                    isbn = _as_isbn(r.text)
                    if isbn:
                        return isbn
            except Exception:
                pass
        if detector:
            try:
                result = detector.detectAndDecodeWithType(img)
                if result[0]:
                    for code in result[1]:
                        isbn = _as_isbn(code)
                        if isbn:
                            return isbn
            except Exception:
                pass
    return None