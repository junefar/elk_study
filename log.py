# -*- coding: utf-8 -*-
# ----------------------------
# @File    : log.py
# @Date    : 2021-03-24
# @Author  : jf.l
# ----------------------------


import logging
import logstash
import sys

host = 'localhost'

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.DEBUG)
test_logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))

test_logger.error('python-logstash: test logstash error message.')
test_logger.info('python-logstash: test logstash info message.')
test_logger.warning('python-logstash: test logstash warning message.')

extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
test_logger.info('python-logstash: test extra fields', extra=extra)
