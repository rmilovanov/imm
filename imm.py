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
    im = Image.open(original_image_file)

    width, height = im.size
    ratio = min(float(maxw) / int(width), float(maxh) / int(height))
    size = int(width * ratio), int(height * ratio)

    basewidth = maxw
    wpercent = (basewidth/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im = im.resize((basewidth,hsize), Image.ANTIALIAS)
    #print size
    #im.resize(size, Image.ANTIALIAS)
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



#print is_valid_png('toyota.png')
#convert_image_file_to_jpg('toyota.png')
#print is_valid_jpg('toyota.jpg')

#png_files = get_valid_pngs('img_dev')

#for png_file in png_files:
    #print png_file

#test_folder = 'img_dev'
#cats = sort_images(test_folder)
#for category in cats:
#    for t_file in cats[category]:
#        print category + " : " + t_file

#img1 = Image.open("1.jpg").transpose(Image.FLIP_LEFT_RIGHT)
#img1.save("1_left_right.jpg")
#img2 = Image.open("1.jpg").transpose(Image.FLIP_TOP_BOTTOM)
#img2.save("1_up_down.jpg")
#img3 = Image.open("1.jpg").transpose(Image.BILINEAR)
#img3.save("1_bil.jpg")
#img4 = Image.open("1.jpg")
#image_file = img4.convert('1') # convert image to black and white
#mage_file.save('1_monochrome.png')

#img5 = Image.open('1.jpg').convert('LA')
#img5.save('1_grayscale.png')
#img6 = Image.open('1_grayscale.png').convert('RGB')
#img6.save('1_grayscale.jpg','jpeg')
