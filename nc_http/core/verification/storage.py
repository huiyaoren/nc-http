from abc import abstractmethod, ABC

from nc_http.core.verification.image import SimpleImageCaptcha


class BaseCaptchaStorage(ABC):

    @classmethod
    def create(cls, *args, **kwargs):
        """
        创建验证码
        :return:
        """
        captcha = SimpleImageCaptcha(*args, **kwargs)
        cls.storage(captcha.str)
        return captcha

    @staticmethod
    @abstractmethod
    def storage(captcha_code):
        """
        记录生成的验证码字符
        :param captcha_code:
        :return:
        """

    @staticmethod
    @abstractmethod
    def validate(captcha_code):
        """
        确认验证码正确性
        :param captcha_code:
        :return: str
        """


class SampleCaptchaStorage(BaseCaptchaStorage):
    """
    验证码池样例实现

        * 仅作测试使用，勿用于生产环境
    """
    storage_dict = {}

    @staticmethod
    def storage(captcha_code):
        SampleCaptchaStorage.storage_dict[captcha_code] = True

    @staticmethod
    @abstractmethod
    def validate(captcha_code):
        valid = SampleCaptchaStorage.storage_dict.get(captcha_code)
        if valid:
            del SampleCaptchaStorage.storage_dict[captcha_code]
            return True
        return False


if __name__ == '__main__':
    test_captcha = SampleCaptchaStorage.create()
    is_valid = SampleCaptchaStorage.validate('test_code')
    print(is_valid)
    is_valid = SampleCaptchaStorage.validate(test_captcha.str)
    print(is_valid)
