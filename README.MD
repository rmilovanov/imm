# Image Manipulations #

imm is a simple library for image files manipulations like bulk resize, bluring, grayscaling, copying, png-to-jpg convertion etc.
It requires PIL or Pillow

### Usage ###

*First you have to install [Pillow](https://pypi.python.org/pypi/Pillow/2.2.1)*

`pip install Pillow`


*Than download [imm.py](https://github.com/rmilovanov/imm/blob/master/imm.py) to your project directory*
```
cd /path/to/my-project
wget https://raw.githubusercontent.com/rmilovanov/imm/master/imm.py
```

*You can use curl instead of wget*
```
cd /path/to/my-project
curl https://raw.githubusercontent.com/rmilovanov/imm/master/imm.py > imm.py
```

Now you can use it in your project:
```Python
import imm
...
imm.convert_image_file_to_jpg('mypicture.png')
...
```

Pull requests are welcome
