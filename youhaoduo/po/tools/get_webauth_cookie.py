#!/usr/bin/env python
# -*- coding: utf-8 -*-



import redis
from loguru import logger
import json
import requests
import re
import base64


def get_cookies():
    cookies = {'webauth_at': 'X2AvOx4RyaEcXiqNmqeIc+heXWKA3NvVolHRowylxoy4vsGn1V7MxsUcJ7CaqmDLRjGHBYr6XSAUpTIil9Snn404glwHqjaluEyWMJpgwkp95oIw7s6Q4MhBApsvMY1jqVkHyA=='}
    return cookies


def get_cookies_mod():
    cookies = {'webauth_at': 'X2AvX8tTYpMQ9HnFjg9htuJ4UIGHDOnl0creqxozFW+BMoxj8wWImLoYGzLjeHmk2pMUcPpF4zadX6L+3XuAEcys71ePvgTU7mdqBOx9BjFDnInuS4bNZoyvUwVy00XRFh5T2w==; path=/; secure; HttpOnly'}
    return cookies

