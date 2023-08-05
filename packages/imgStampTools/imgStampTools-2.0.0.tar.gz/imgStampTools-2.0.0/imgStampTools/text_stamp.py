import os
import random
import tqdm

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops


def get_stamp_img(angle, w, h, text, color="#8B8B1B", size=30, opacity=0.15):
    FONT = os.path.dirname(__file__) + "/font/simhei.ttf"
    stamp = Image.new(mode='RGBA', size=(w, h))
    draw_table = ImageDraw.Draw(im=stamp)
    draw_table.text(xy=(int(w / 2), int(h / 2)),
                    text=text,
                    fill=color,
                    font=ImageFont.truetype(FONT, size=size))
    del draw_table
    angle = random.randint(1, angle)
    stamp = stamp.rotate(angle)
    stamp = crop_image(stamp)
    set_opacity(stamp, opacity)
    return stamp


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


def im_add_stamp(im, text, color="#8B8B1B", size=30, opacity=0.15, angle=30):
    """给图片对象添加水印"""
    w, h = im.size
    # 获取水印图片对象
    stamp = get_stamp_img(angle, w, h, text, color, size, opacity)
    # 在原图上添加水印大图
    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    width_half = int(w / 2)
    height_half = int(h / 2)
    coorX = random.randint(int(width_half * 0.1), int(width_half * 1.2))
    coorY = random.randint(int(height_half * 0.1), int(height_half * 1.2))

    im.paste(stamp, (coorX, coorY), mask=stamp.split()[3])
    return im


def add_stamp2file(imageFile, text, out="output", color="#8B8B1B", size=30, opacity=0.15, space=75, angle=30):
    name = os.path.basename(imageFile)
    new_name = os.path.join(out, name)
    try:
        im = Image.open(imageFile)
        image = im_add_stamp(im, text, color, size, opacity, angle)
        if not os.path.exists(out):
            os.mkdir(out)
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        image.save(new_name)
        print(new_name, "保存成功。")
    except Exception as e:
        print(new_name, "保存失败。错误信息：", e)


def add_stamp(file, stamp, out="output", color="#8B8B1B", size=30, opacity=0.15, space=75, angle=30):
    if os.path.isdir(file):
        names = os.listdir(file)
        for name in names:
            image_file = os.path.join(file, name)
            add_stamp2file(image_file, stamp, out, color, size, opacity, space, angle)
    else:
        add_stamp2file(file, stamp, out, color, size, opacity, space, angle)


def add_text_stamp(inpath, outpath, text_stamp, text_opacity_list=[0.2, 0.3], text_size_list=[150, 200]):
    for im in tqdm.tqdm(os.listdir(inpath)):
        img_path = os.path.join(inpath, im)
        opacity = random.choice(text_opacity_list)
        size = random.choice(text_size_list)
        add_stamp(file=img_path, out=outpath, stamp=text_stamp, opacity=opacity, angle=30, space=20, size=size,
                  color='#000000')



