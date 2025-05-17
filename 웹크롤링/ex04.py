from PIL import Image

filename = input('파일명 : ')
img = Image.open(filename)
img.show()