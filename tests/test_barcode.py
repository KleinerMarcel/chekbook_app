import sys
sys.path.insert(0, "src")
import cv2
print("OpenCV", cv2.__version__, "| есть cv2.barcode:", hasattr(cv2, "barcode"))
from barcode_reader import decode_isbn, zxingcpp
print("zxing-cpp:", "есть" if zxingcpp else "нет")
print("Результат:", decode_isbn(open(sys.argv[1], "rb").read()))ы