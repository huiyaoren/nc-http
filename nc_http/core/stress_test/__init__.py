import json
import subprocess

import requests
from locust import HttpUser, task, between


class SwaggerJsonUrlNotFound(Exception):
    """缺少 swagger json url 定义"""


class SwaggerApiParser:
    def __init__(self, json_url=None):
        self.json_url = json_url
        self.api_list = None

    @property
    def content(self):
        """
        :return: [
            ('get', '/application'),
            ('post', '/application'),
        ]
        """
        if not self.api_list:
            self.api_list = self._parse_api()

        return self.api_list

    def _parse_api(self):
        if not self.json_url:
            raise SwaggerJsonUrlNotFound

        swagger_dict = json.loads(requests.get(self.json_url).text)
        if swagger_dict.get('host'):
            print('host: {}'.format(swagger_dict['host']))
        if swagger_dict.get('asePath'):
            print('asePath: {}'.format(swagger_dict['asePath']))

        if not swagger_dict.get('paths'):
            return []

        result = []
        for path, methods in swagger_dict['paths'].items():
            for method in methods:
                result.append((method, path))

        return result


TEST_JSON_URL = 'http://localhost:7071/apispec_1.json'


class StressTest(HttpUser):
    wait_time = between(1, 2)
    parser = SwaggerApiParser(TEST_JSON_URL)

    @task
    def index_page(self):
        for method, uri in self.parser.content:
            run = getattr(self.client, method)
            run(uri)

    @staticmethod
    def run_locust(file_name=None):
        file_name = file_name or __file__
        subprocess.run(['locust', '-f', file_name])


if __name__ == '__main__':
    StressTest.run_locust()

'''
# sample.py

class SampleStressTest(StressTest):
    parser = SwaggerApiParser('http://localhost:7071/apispec_1.json')

if __name__ == '__main__':
    SampleStressTest.run_locust()
'''
