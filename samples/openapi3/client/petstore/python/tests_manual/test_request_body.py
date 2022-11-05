# coding: utf-8

"""
    OpenAPI Petstore

    This spec is mainly for testing Petstore server and contains fake endpoints, models. Please do not use this for any other purpose. Special characters: \" \\  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

import collections
import json
import unittest

from petstore_api import api_client, exceptions, schemas

ParamTestCase = collections.namedtuple('ParamTestCase', 'payload expected_serialization')


class TestParameter(unittest.TestCase):

    def test_throws_exception_when_content_is_invalid_size(self):
        with self.assertRaises(ValueError):
            api_client.RequestBody(
                content={}
            )

    def test_content_json_serialization(self):
        payloads = [
            None,
            1,
            3.14,
            'blue',
            'hello world',
            '',
            True,
            False,
            [],
            ['blue', 'black', 'brown'],
            {},
            dict(R=100, G=200, B=150),
        ]
        for payload in payloads:
            request_body = api_client.RequestBody(
                content={'application/json': api_client.MediaType(schema=schemas.AnyTypeSchema)}
            )
            serialization = request_body.serialize(payload, 'application/json')
            self.assertEqual(
                serialization,
                dict(body=json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode('utf-8'))
            )

    def test_content_multipart_form_data_serialization(self):
        payload = dict(
            some_null=None,
            some_bool=True,
            some_str='a',
            some_int=1,
            some_float=3.14,
            some_list=[],
            some_dict={},
            some_bytes=b'abc'
        )
        request_body = api_client.RequestBody(
            content={'multipart/form-data': api_client.MediaType(schema=schemas.AnyTypeSchema)}
        )
        serialization = request_body.serialize(payload, 'multipart/form-data')
        self.assertEqual(
            serialization,
            dict(
                fields=(
                    api_client.RequestField(
                        name='some_null', data='null', headers={
                            'Content-Type': 'application/json',
                            "Content-Disposition": "form-data; name=\"some_null\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_bool', data='true', headers={
                            'Content-Type': 'application/json',
                            "Content-Disposition": "form-data; name=\"some_bool\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_str', data='a', headers={
                            'Content-Type': 'text/plain',
                            "Content-Disposition": "form-data; name=\"some_str\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_int', data='1', headers={
                            'Content-Type': 'application/json',
                            "Content-Disposition": "form-data; name=\"some_int\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_float', data='3.14', headers={
                            'Content-Type': 'application/json',
                            "Content-Disposition": "form-data; name=\"some_float\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_list', data='[]', headers={
                            'Content-Type': 'application/json',
                            "Content-Disposition": "form-data; name=\"some_list\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_dict', data='{}', headers={
                            'Content-Type': 'application/json',
                            "Content-Disposition": "form-data; name=\"some_dict\"",
                            "Content-Location": None
                        }),
                    api_client.RequestField(
                        name='some_bytes', data=b'abc', headers={
                            'Content-Type': 'application/octet-stream',
                            "Content-Disposition": "form-data; name=\"some_bytes\"",
                            "Content-Location": None
                        })
                )
            )
        )

    def test_throws_error_for_nonexistant_content_type(self):
        request_body = api_client.RequestBody(
            content={'application/json': api_client.MediaType(schema=schemas.AnyTypeSchema)}
        )
        with self.assertRaises(KeyError):
            request_body.serialize(None, 'abc/def')

    def test_throws_error_for_not_implemented_content_type(self):
        request_body = api_client.RequestBody(
            content={
                'application/json': api_client.MediaType(schema=schemas.AnyTypeSchema),
                'text/css': api_client.MediaType(schema=schemas.AnyTypeSchema)
            }
        )
        with self.assertRaises(NotImplementedError):
            request_body.serialize(None, 'text/css')

    def test_application_x_www_form_urlencoded_serialization(self):
        payload = dict(
            some_null=None,
            some_str='hi there',
            some_int=1,
            some_float=3.14,
            some_list=[],
            some_dict={},
        )
        content_type = 'application/x-www-form-urlencoded'
        request_body = api_client.RequestBody(
            content={content_type: api_client.MediaType(schema=schemas.AnyTypeSchema)}
        )
        serialization = request_body.serialize(payload, content_type)
        self.assertEqual(
            serialization,
            dict(body='some_str=hi%20there&some_int=1&some_float=3.14')
        )

        serialization = request_body.serialize({}, content_type)
        self.assertEqual(
            serialization,
            dict(body='')
        )

        invalid_payloads = [
            dict(some_bool=True),
            dict(some_bytes=b'abc'),
            dict(some_list_with_data=[0]),
            dict(some_dict_with_data={'a': 'b'}),
        ]
        for invalid_payload in invalid_payloads:
            with self.assertRaises(exceptions.ApiValueError):
                request_body.serialize(invalid_payload, content_type)


if __name__ == '__main__':
    unittest.main()