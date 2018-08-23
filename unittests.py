import unittest
import imm
import os


class TestLib(unittest.TestCase):

    def setup(self):
        pass

    def test_nothing(self):
        self.assertEqual(True, True)

    def test_is_jpg(self):
        wrong = imm.is_jpg('images/input/longboard.png')
        right = imm.is_jpg('images/input/tesla.jpg')
        self.assertEqual(wrong, False)
        self.assertEqual(right, True, 'is_jpg  FAILED')

    def test_is_valid_jpg(self):
        wrong = imm.is_valid_jpg('images/input/longboard.png')
        right = imm.is_valid_jpg('images/input/tesla.jpg')
        self.assertEqual(wrong, False)
        self.assertEqual(right, True, 'is_valid_jpg  FAILED')

    def test_is_png(self):
        png = imm.is_png('images/input/longboard.png')
        jpg = imm.is_png('images/input/tesla.jpg')
        self.assertEqual(png, True)
        self.assertEqual(jpg, False, 'is_png  FAILED')

    def test_is_valid_png(self):
        png = imm.is_valid_png('images/input/longboard.png')
        jpg = imm.is_valid_png('images/input/tesla.jpg')
        self.assertEqual(png, True)
        self.assertEqual(jpg, False, 'id_valid_jpg  FAILED')

    def test_get_dimensions(self):
        image_file = 'images/input/longboard.png'
        dimensions = imm.get_dimensions(image_file)
        right_dims = (1280, 720)
        self.assertEqual(dimensions, right_dims)

    def test_cut_area_around(self):
        test_image = 'images/input/longboard.png'
        output_file = 'images/test/longboard.jpg'
        print imm.get_dimensions(test_image)
        boxx = 1000
        boxy = 600
        box_width = 620
        box_height = 620
        imm.cut_area_around(
            test_image, boxx, boxy, box_width, box_height, output_file)
        res_w, res_h = imm.get_dimensions(output_file)
        self.assertEqual(res_w, 590)
        self.assertEqual(res_h, 430)
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
    os.rmdir('images/test')
