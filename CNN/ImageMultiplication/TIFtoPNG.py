from PIL import Image
import glob

for name in glob.glob('*.tif'):
    im = Image.open(name)
    name = str(name).rstrip(".tif")
    im.save(name + '.png', 'PNG')

for name in glob.glob('*.tiff'):
    im = Image.open(name)
    name = str(name).rstrip(".tiff")
    im.save(name + '.png', 'PNG')

print("Conversion from tif/tiff to png completed!")