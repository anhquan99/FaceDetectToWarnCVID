from PIL import Image, ExifTags
import cv2
import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_PATH, "images")

# for orientation in ExifTags.TAGS.keys():
#     # if ExifTags.TAGS[orientation]=='Orientation':
#     #     break
#     for root , dirs, files in os.walk(image_dir):
#         for file in files:
#             if file.endswith("png") or file.endswith("jpg"):
#                 path = os.path.join(root, file)
#                 image = Image.open(path)
#                 print(path)
#                 metaData = image._getexif()
#                 print(metaData)
# try:
#     exif=dict(image.getexif().items())
#     if exif[orientation] == 3:
#         image=image.rotate(180, expand=True)
#     elif exif[orientation] == 6:
#         image=image.rotate(270, expand=True)
#     elif exif[orientation] == 8:
#         image=image.rotate(90, expand=True)
#     image.save(path)
#     image.close()
#     print("success")
# except(Exception):
#     print("failed")
#     pass

# try:
#     filepath = os.path.join(image_dir, "3.jpg")
#     image=Image.open(filepath)
#     image.show()

#     # for orientation in ExifTags.TAGS.keys():
#     #     if ExifTags.TAGS[orientation]=='Orientation':
#     #         break

#     exif=dict(image._getexif().items())

#     if exif[orientation] == 3:
#         image=image.rotate(180, expand=True)
#     elif exif[orientation] == 6:
#         image=image.rotate(270, expand=True)
#     elif exif[orientation] == 8:
#         image=image.rotate(90, expand=True)

#     image.save(filepath)
#     image.close()
# except (AttributeError, KeyError, IndexError):
#     # cases: image don't have getexif
#     pass
print(image_dir)
for file in os.listdir(image_dir):
    if file.endswith("png") or file.endswith("jpg"):
        print("name:", file)
        image = Image.open(os.path.join(image_dir, file))
        print(image)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = dict(image.getexif().items())
            print(exif[orientation])
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
            image.save(os.path.join(image_dir, file))
            image.close()
            print("success")
        except(Exception):
            print("failed")
            pass
# image = Image.open(os.path.join(image_dir, file.name))
