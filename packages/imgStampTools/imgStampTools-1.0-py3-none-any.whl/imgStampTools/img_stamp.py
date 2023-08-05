import os
import tqdm
import random
from PIL import Image, ImageEnhance, ImageChops


def crop_image(im):
    bg = Image.new(mode='RGBA', size=im.size)
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def set_opacity(im, opacity):
    assert 0 <= opacity <= 1
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def im_add_stamp(im, img, opacity=0.15, angle=30):
    stamp = Image.open(img)
    stamp_w, stamp_h = stamp.size
    stamp = stamp.resize((stamp_w * 2, stamp_h * 2), Image.ANTIALIAS)
    w, h = im.size
    stamp2 = Image.new(mode='RGBA', size=(w, h))
    stamp2.paste(stamp, (500, 500))
    angle = random.randint(1, angle)
    stamp2 = stamp2.rotate(angle)
    stamp2 = crop_image(stamp2)
    set_opacity(stamp2, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    width_half = int(w / 2)
    height_half = int(h / 2)
    coorX = random.randint(int(width_half * 0.1), int(width_half * 1.2))
    coorY = random.randint(int(height_half * 0.1), int(height_half * 1.2))
    im.paste(stamp2, (coorX, coorY), mask=stamp2.split()[3])
    return im


def add_stamp2file(imageFile, img, out="output", opacity=0.15, angle=30):
    name = os.path.basename(imageFile)
    new_name = os.path.join(out, name)
    try:
        im = Image.open(imageFile)
        image = im_add_stamp(im, img, opacity, angle)
        if not os.path.exists(out):
            os.mkdir(out)
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        image.save(new_name)
        print(new_name, "保存成功。")
    except Exception as e:
        print(new_name, "保存失败。错误信息：", e)


def add_stamp(file, stamp, out="output", opacity=0.15, angle=30):
    if os.path.isdir(file):
        names = os.listdir(file)
        for name in names:
            image_file = os.path.join(file, name)
            add_stamp2file(image_file, stamp, out, opacity, angle)
    else:
        add_stamp2file(file, stamp, out, opacity, angle)


def add_img_stamp(inpath, outpath, stamppath, img_opacity_list=[0.2, 0.4]):
    for im in tqdm.tqdm(os.listdir(inpath)):
        img_path = os.path.join(inpath, im)
        opacity = random.choice(img_opacity_list)
        add_stamp(file=img_path, out=outpath, stamp=stamppath, opacity=opacity, angle=30)



