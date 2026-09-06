import sys
from PIL import Image

# usage: crop2.py <src> <out> <left> <top> <right> <bottom> [scale]
def main():
    src, out = sys.argv[1], sys.argv[2]
    l, t, r, b = map(int, sys.argv[3:7])
    scale = float(sys.argv[7]) if len(sys.argv) > 7 else 2.0
    im = Image.open(src).convert("L")
    crop = im.crop((l, t, r, b))
    crop = crop.resize((int(crop.width*scale), int(crop.height*scale)), Image.LANCZOS)
    crop.save(out)
    print(out, crop.size)

if __name__ == "__main__":
    main()
