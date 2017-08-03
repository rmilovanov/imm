#
#  Updated:  03-Aug-2017
#

from PIL import Image
import os
import imghdr
import os
import json
from subprocess import call
import shlex
from os import listdir
from os.path import isfile, join
import shutil
import re
import ntpath


def is_jpg(some_file):
    result = False
    if imghdr.what(some_file) == 'jpeg':
        result = True
    return result


def is_png(some_file):
    result = False
    if imghdr.what(some_file) == 'png':
        result = True
    return result


def is_valid_image(some_file):
    result = True
    try:
        im = Image.open(some_file)
        im.close()
    except IOError:
        result = False
    return result


def is_valid_jpg(some_file):
    result = False
    if is_valid_image(some_file) and is_jpg(some_file):
        result = True
    return result


def is_valid_png(some_file):
    result = False
    if is_valid_image(some_file) and is_png(some_file):
        result = True
    return result


def make_white_bg_transparent(img_file):
    img = Image.open(img_file)
    os.remove(img_file)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] > 253 and item[1] > 253 and item[2] > 253:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    new_file_name = os.path.splitext(img_file)[0]+'.png'
    img.save(new_file_name, "PNG")
    return new_file_name

def convert_image_file_to_jpg(img_file):
    """
    Creates JPEG file from any image file
    img_file : String
        The name of source file
    """
    img = Image.open(img_file).convert('RGB')
    os.remove(img_file)
    new_file_name = os.path.splitext(img_file)[0]+'.jpg'
    img.save(new_file_name, 'jpeg')
    return new_file_name


def convert_image_file_to_png(img_file):
    """
    Creates PNG file from any image file
    img_file : String
        The name of source file
    """
    img = Image.open(img_file)
    os.remove(img_file)
    new_file_name = os.path.splitext(img_file)[0]+'.png'
    img.save(new_file_name, 'png')
    return new_file_name


def get_files_names_in_folder(some_folder):
    return [f for f in listdir(some_folder) if isfile(join(some_folder, f))]


def get_subfolders(some_folder):
    return [f for f in listdir(some_folder) if isdir(join(some_folder, f))]


def get_files_in_folder(some_folder):
    result = []
    for this_file in get_files_names_in_folder(some_folder):
        this_file_path = some_folder + "/" + this_file
        result.append(this_file_path)
    return result


def get_valid_pngs(some_folder):
    result = []
    all_files = get_files_names_in_folder(some_folder)
    for this_file in all_files:
        file_path = some_folder + "/" + this_file
        if is_valid_png(file_path):
            result.append(file_path)
    return result


def sort_images(some_folder):
    result = {'jpg': [], 'png': [], 'None': []}
    for some_file in get_files_in_folder(some_folder):
        if is_valid_image(some_file):
            if is_jpg(some_file):
                result['jpg'].append(some_file)
            else:
                if is_png(some_file):
                    result['png'].append(some_file)
                else:
                    result['None'].append(some_file)
        else:
            result['None'].append(some_file)
    return result


def get_file_name_from_path(some_path):
    return ntpath.basename(some_path)


def rotated_copy(original_image_file, folder_to_store, rotation_angle):
    img_pre = Image.open(original_image_file)
    img = img_pre.rotate(rotation_angle, expand=True)
    original_name_ext_cut = os.path.splitext(get_file_name_from_path(original_image_file))[0]
    new_img_name = folder_to_store + "/" + original_name_ext_cut + "_" + str(rotation_angle) + ".jpg"
    img.save(new_img_name)
    return new_img_name


def rotated_copies(original_image_file, folder_to_store, rotation_angles):
    result = []
    for some_angle in rotation_angles:
        result.append(rotated_copy(original_image_file, folder_to_store, some_angle))
    return result


def mirror_top_bottom_copy(original_image_file, folder_to_store):
    img = Image.open(original_image_file).transpose(Image.FLIP_TOP_BOTTOM)
    original_name_ext_cut = os.path.splitext(get_file_name_from_path(original_image_file))[0]
    new_img_name = folder_to_store + "/" + original_name_ext_cut + "_ft" + ".jpg"
    img.save(new_img_name)
    return new_img_name


def grayscale_copy(original_image_file, folder_to_store):
    img = Image.open(original_image_file).convert('LA').convert('RGB')
    original_name_ext_cut = os.path.splitext(get_file_name_from_path(original_image_file))[0]
    new_img_name = folder_to_store + "/" + original_name_ext_cut + "_gs" + ".jpg"
    img.save(new_img_name, 'jpeg')
    return new_img_name


def monochrome_copy(original_image_file, folder_to_store):
    img = Image.open(original_image_file).convert('1').convert('RGB')
    original_name_ext_cut = os.path.splitext(get_file_name_from_path(original_image_file))[0]
    new_img_name = folder_to_store + "/" + original_name_ext_cut + "_mc" + ".jpg"
    img.save(new_img_name, 'jpeg')
    return new_img_name


def resize_file(original_image_file, output_image_file, maxw, maxh):
    """
    Creates resized image file from given one
    original_image_file : String
        The name of source file
    output_image_file : String
        The name of file to save the result
    maxw :
        Max allowed width
    maxw :
        Max allowed height
    """
    im = Image.open(original_image_file)
    width, height = im.size
    ratio = min(float(maxw) / int(width), float(maxh) / int(height))
    im = im.resize((int(width*ratio),int(height*ratio)), Image.ANTIALIAS)
    im.save(output_image_file, "JPEG")
    return output_image_file


def put_into_rect(original_image_file, output_image_file, rw, rh):
    im = Image.open(original_image_file)
    width, height = im.size
    ratio = min(float(rw) / int(width), float(rh) / int(height))
    im = im.resize((int(width*ratio),int(height*ratio)), Image.ANTIALIAS)

    resim = Image.new('RGB', (rw, rh), (255, 255, 255))
    width, height = im.size
    offset = ((rw - width) / 2, (rh - height) / 2)
    resim.paste(im, offset)
    resim.save(output_image_file, "JPEG")
    return output_image_file
