import unittest

from nc_http.core.verification.storage import SampleCaptchaStorage


class VerificationTestCase(unittest.TestCase):

    def test_storage(self):
        captcha = SampleCaptchaStorage.create()
        is_valid = SampleCaptchaStorage.validate('test_code')
        self.assertEqual(is_valid, False)
        is_valid = SampleCaptchaStorage.validate(captcha.str)
        self.assertEqual(is_valid, True)


if __name__ == '__main__':
    unittest.main()
