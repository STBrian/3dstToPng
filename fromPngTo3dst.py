import glob, os
from PIL import Image
from pathlib import Path

from modules.tex3dst import Texture3dst

root = input("Introduce el nombre de la carpeta raíz: ")

supported = 0
unsupported = 0
for file in glob.iglob(os.path.join(os.path.abspath(f"{root}"), "**/*.png"), recursive=True):
    #print(file)
    file_path = Path(file)
    #print(file_path.parent) path
    #print(file_path.stem) filename
    #print(file_path.suffix) extension
    try:
        png_img = Image.open(file)
        png_w, png_h = png_img.size
        metadata = png_img.text
        if "MipLevel" in metadata and "Format" in metadata and "Mode" in metadata:
            texture = Texture3dst().new(png_w, png_h, int(metadata["MipLevel"]), metadata["Format"])
        else:
            print("Missing metadata info in png, trying to get from original texture")
            original_texture_path = os.path.join(file_path.parent, f"{file_path.stem}.3dst")
            if os.path.exists(original_texture_path):
                original_texture = Texture3dst().open(original_texture_path)
                miplevel = original_texture.miplevel
                tex_format = original_texture.format
            else:
                print("Caution: No original file found, using default. It is preferred to use original values so as not to cause problems with the game.")
                miplevel = 1
                tex_format = "rgba8"
            texture = Texture3dst().new(png_w, png_h, miplevel, tex_format)
        texture.paste(png_img, 0, 0)
        texture.flipX()
        texture.convertData()
        #print(os.path.join(file_path.parent, f"{file_path.stem}.3dst"))
        texture.export(os.path.join(file_path.parent, f"{file_path.stem}.3dst"))
        supported += 1
    except Exception as e: 
        print(f"Error while opening: {file}")
        print(e)
        print("Skipping file...")
        unsupported += 1

print("Summary:")
print(f"Images converted: {supported}")
print(f"Fails: {unsupported}")