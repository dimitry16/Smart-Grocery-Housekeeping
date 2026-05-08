import os
from app.external_api_services.google_vision import localize_objects

_DIR = os.path.dirname(os.path.abspath(__file__))


def test_image_1():
    result = localize_objects(os.path.join(_DIR, "visiontest1.png"))
    assert result == "banana"


def test_image_2():
    result = localize_objects(os.path.join(_DIR, "visiontest2.png"))
    assert result == "apple"


def test_image_3():
    result = localize_objects(os.path.join(_DIR, "visiontest3.png"))
    assert result == "rambutan"
