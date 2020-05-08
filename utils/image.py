import os
import sys
import math
import shutil
import copy
import struct
import re
import random
import time


from frameworks.utils.log import Log
from frameworks.utils.fs import FileUtils
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True

COMPRESS_TYPE_NORMAL = 1      # only compress size
COMPRESS_TYPE_PVR = 2    # compress to platform only
COMPRESS_TYPE_ETC1 = 3    # compress to platform only
COMPRESS_TYPE_PVR2CCZ = 4    # compress to pvr2ccz

TEMPLATE_PATH = "%s/../template" % os.path.split(__file__)[0]


class ImageUtils(object):
    """do something for images"""

    def __init__(self):
        super(ImageUtils, self).__init__()

    @staticmethod
    def resize(path, size):
        try:
            img = Image.open(img_path)
            (width, height) = img.size
            new_width = 200
            new_height = height * new_width / width
            out = img.resize((new_width, new_height))
            ext = os.path.splitext(img_path)[1]
            new_file_name = '%s%s' % ('small', ext)
            out.save(new_file_name)

        except Exception:
            Log.w("resize error")

    @staticmethod
    def get_noalpha_rect(self, img):
        # noaphlal_left
        noaphla_rect = {"left": 0, "up": 0, "right": 0, "bottom": 0}
        size = img.size
        # print size, "================"
        # left
        is_break = False
        # print "left================"
        for x in xrange(0, size[0]):
            for y in xrange(0, size[1]):
                # print x, y
                pixel = img.getpixel((x, y))
                if pixel[3] != 0:
                    noaphla_rect["left"] = x
                    is_break = True
                    break
            if is_break:
                break

        # right
        # print "right================"
        is_break = False
        for x in xrange(size[0] - 1, -1, -1):
            for y in xrange(0, size[1]):
                # print x, y
                pixel = img.getpixel((x, y))
                if pixel[3] != 0:
                    noaphla_rect["right"] = x
                    is_break = True
                    break
            if is_break:
                break

        # up
        # print "up================"
        is_break = False
        for x in xrange(0, size[1]):
            for y in xrange(0, size[0]):
                # print y, x
                pixel = img.getpixel((y, x))
                if pixel[3] != 0:
                    noaphla_rect["up"] = x
                    is_break = True
                    break
            if is_break:
                break

        # bottom
        # print "bottom================"
        is_break = False
        for x in xrange(size[1] - 1, -1, -1):
            for y in xrange(0, size[0]):
                # print y, x
                pixel = img.getpixel((y, x))
                if pixel[3] != 0:
                    noaphla_rect["bottom"] = x
                    is_break = True
                    break
            if is_break:
                break
        return noaphla_rect

    @staticmethod
    def split_rgb_alpha(path):
        (str_file, str_ext) = os.path.splitext(path)
        img = Image.open(path)
        (w, h) = img.size
        h = h * 2
        r, g, b, a = img.split()

        imgRGB = Image.merge("RGB", (r, g, b))

        imgNew = Image.new("RGB", (w, h), (0, 0, 0))
        imgNew.paste(imgRGB, (0, 0))
        imgNew.paste(a, (0, h / 2))

        str_out_path = '%s.%s' % (str_file, "jpg")
        imgNew.save(str_out_path)
        imgNew.close()
        return str_out_path

    @staticmethod
    def split_r_g_b_alpha(path):
        (str_file, str_ext) = os.path.splitext(path)
        img = Image.open(path)
        (w, h) = img.size
        w = w * 2
        h = h * 2
        r = Image.new("RGB", (w / 2, h / 2))
        g = Image.new("RGB", (w / 2, h / 2))
        b = Image.new("RGB", (w / 2, h / 2))
        a = Image.new("RGB", (w / 2, h / 2))

        for x in xrange(0, w / 2):
            for y in xrange(0, h / 2):
                pixel = img.getpixel((x, y))
                # print pixel
                # print pixel[0] >> 5
                # print (pixel[0] & 31) >> 2
                # print pixel[0] & 3
                # print "========================="
                r.putpixel(
                    (x, y), (pixel[0] & 224,  (pixel[0] & 28) << 3,  (pixel[0] & 3) << 5))
                g.putpixel(
                    (x, y), (pixel[1] & 224,  (pixel[1] & 28) << 3,  (pixel[1] & 3) << 5))
                b.putpixel(
                    (x, y), (pixel[2] & 224,  (pixel[2] & 28) << 3,  (pixel[2] & 3) << 5))
                a.putpixel(
                    (x, y), (pixel[3] & 224,  (pixel[3] & 28) << 3,  (pixel[3] & 3) << 5))

                # print r.getpixel((x,y))
                # print g.getpixel((x,y))
                # print b.getpixel((x,y))
                # print a.getpixel((x,y))

        imgNew = Image.new("RGB", (w, h))
        imgNew.paste(r, (0, 0))
        imgNew.paste(g, (w / 2 + 1, 0))
        imgNew.paste(b, (0, h / 2 + 1))
        imgNew.paste(a, (w / 2 + 1, h / 2 + 1))
        imgNew.save('%s.%s' % (str_file, "jpg"))
        return imgNew

    @staticmethod
    def modify_image_colors(path):
        Log.e(path)
        img = Image.open(path)
        Log.e(img)
        (w, h) = img.size
        count_map = {}
        type_map = {}

        def gen_key(pixel):
            if type(pixel) == int:
                return "%s" % pixel
            elif len(pixel) == 1:
                return "%s" % pixel[0]
            elif len(pixel) == 3:
                return "%s_%s_%s" % (pixel[0], pixel[1], pixel[2])
            elif len(pixel) == 4:
                return "%s_%s_%s_%s" % (pixel[0], pixel[1], pixel[2], pixel[3])

        for x in range(0, w):
            for y in range(0, h):
                # Log.e("%s %s = %s" % (x, y, img.getpixel((x, y))))
                pixel = img.getpixel((x, y))
                key = gen_key(pixel)
                if key not in count_map:
                    count_map[key] = 0
                count_map[key] += 1

        def modify(pixel):
            if type(pixel) == int:
                return pixel
            elif len(pixel) == 3:
                r = random.randint(0, 2)
                if r == 0:
                    return (min(pixel[0] + 1, 255), pixel[1], pixel[2])
                if r == 1:
                    return (pixel[0], min(pixel[1] + 1, 255), pixel[2])
                if r == 2:
                    return (pixel[0], pixel[1], min(pixel[2] + 1, 255))
            elif len(pixel) == 4:
                r = random.randint(0, 2)
                if r == 0:
                    return (min(pixel[0] + 1, 255), pixel[1], pixel[2], pixel[3])
                if r == 1:
                    return (pixel[0], min(pixel[1] + 1, 255), pixel[2], pixel[3])
                if r == 2:
                    return (pixel[0], pixel[1], min(pixel[2] + 1, 255), pixel[3])
            else:
                return pixel

        keys = []
        for var in count_map.keys():
            keys.append(var)

        for i in range(0, 3):
            k = random.choice(keys)
            if k not in type_map:
                colors = []
                for c in k.split("_"):
                    colors.append(int(c))

                type_map[k] = tuple(modify(colors))

        for x in range(0, w):
            for y in range(0, h):
                # print x, y
                pixel = img.getpixel((x, y))
                key = gen_key(pixel)
                if key in type_map:
                    img.putpixel((x, y), type_map[key])

        img.save(path)
