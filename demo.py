import imm


images = imm.get_files_in_folder('images/input')

for image_file in images:
    print image_file
    output_file = image_file.replace("input", "output")
    imm.resize_file(image_file, output_file, 400, 300)
    imm.make_white_bg_transparent(output_file)
