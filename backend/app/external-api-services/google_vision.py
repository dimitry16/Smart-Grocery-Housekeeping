# Name: Yasser Hernandez (hernayas)
# Citation for the ode below:
# Date: 04/18/2025
# Adapted from "Detect multiple objects" sample code from Google Cloud Vision API documentation.
# Source URL: https://docs.cloud.google.com/vision/docs/object-localizer


from dotenv import load_dotenv

load_dotenv()


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    detected_objects = []

    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        if object_.score >= 0.5:  # print objects with confidence >= 0.6
            # print("Normalized bounding polygon vertices: ")
            # for vertex in object_.bounding_poly.normalized_vertices:
            #     print(f" - ({vertex.x}, {vertex.y})")
            detected_objects.append(object_.name)

    return detected_objects
