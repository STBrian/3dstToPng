import glob, os
from PIL.PngImagePlugin import PngInfo
from pathlib import Path

from modules.tex3dst import Texture3dst

root = input("Introduce el nombre de la carpeta raíz: ")

supported = 0
unsupported = 0
for file in glob.iglob(os.path.join(os.path.abspath(f"{root}"), "**/*.3dst"), recursive=True):
    #print(file)
    file_path = Path(file)
    #print(file_path.parent) path
    #print(file_path.stem) filename
    #print(file_path.suffix) extension
    try:
        texture = Texture3dst().open(file)

        metadata = PngInfo()
        metadata.add_text("MipLevel", str(texture.miplevel))
        metadata.add_text("Format", texture.format)
        metadata.add_text("Mode", str(texture.mode))

        texture.flipX()
        png_img = texture.copy(0, 0, texture.width, texture.height)

        #print(os.path.join(file_path.parent, f"{file_path.stem}.png"))
        png_img.save(os.path.join(file_path.parent, f"{file_path.stem}.png"), pnginfo=metadata)
        supported += 1
    except Exception as e: 
        print(f"Found unsupported 3dst texture at: {file}")
        print(e)
        print("Skipping file...")
        unsupported += 1

print("Summary:")
print(f"Supported files converted: {supported}")
print(f"Unsupported files found: {unsupported}")