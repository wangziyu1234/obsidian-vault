import sys
from PIL import Image

# usage: crop.py <src> <outdir> <prefix> <nbands>
def main():
    src, outdir, prefix, nbands = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    im = Image.open(src).convert("L")
    w, h = im.size
    bh = h // nbands
    for i in range(nbands):
        top = i * bh
        bot = (i + 1) * bh if i < nbands - 1 else h
        crop = im.crop((0, top, w, bot))
        # upscale 2x
        crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
        out = f"{outdir}/{prefix}_{i+1:02d}.png"
        crop.save(out)
        print(out, crop.size)

if __name__ == "__main__":
    main()
