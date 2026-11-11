import sys
sys.path.insert(0, "src")
from isbn import SOURCES, clean_isbn, variants

isbn = clean_isbn(sys.argv[1])
print("ISBN:", isbn, "варианты:", variants(isbn))
for code in variants(isbn):
    for name, source in SOURCES:
        try:
            print(code, name, "->", source(code))
        except Exception as ex:
            print(code, name, "ОШИБКА:", repr(ex))