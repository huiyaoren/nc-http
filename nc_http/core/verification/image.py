import random
import string
from io import BytesIO

from captcha.image import ImageCaptcha


class SimpleImageCaptcha:
    """
    图片验证码
    """

    def __init__(self, width=150, height=50, captcha_length=4, characters=string.digits, *args, **kwargs):
        self.__width = width
        self.__height = height
        self.__captcha_length = captcha_length
        self.__characters = characters

        self.__str = ''.join([random.choice(characters) for _ in range(captcha_length)])

        generator = ImageCaptcha(width=self.__width, height=self.__height, *args, **kwargs)
        self.__image = generator.create_captcha_image(
            chars=self.__str,
            color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            background=(255, 255, 255)
        )

    @property
    def str(self):
        return self.__str

    @property
    def image(self):
        return self.__image

    @property
    def image_handler(self):
        output = BytesIO()
        self.__image.save(output, 'png')
        output.seek(0)
        return output
