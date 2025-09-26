# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
from setuptools import setup, find_packages

from ppocr.version import __version__


def get_requirements(filename="requirements.txt"):
    """
    get requirements list from a file
    """
    with open(filename, 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires


def get_py_version():
    """
    get python version
    """
    py_version = sys.version.split(' ')[0]
    py_version = '.'.join(py_version.split('.')[:2])
    return py_version


def get_paddle_version(requires):
    """
    get paddle version
    """
    paddle_version = ""
    for require in requires:
        if "paddlepaddle" in require:
            if ">=" in require:
                paddle_version = require.split(">=")[-1]
            elif "==" in require:
                paddle_version = require.split("==")[-1]
    return paddle_version


def get_long_description():
    """
    get long description from README.md
    """
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    return long_description


py_version = get_py_version()
requires = get_requirements()
paddle_version = get_paddle_version(requires)

paddle_whl = f"paddlepaddle-gpu=={paddle_version}"
if os.environ.get('PPOCR_INSTALL_CPU', "").lower() in ["true", "1"]:
    paddle_whl = f"paddlepaddle=={paddle_version}"

# all requires
all_requires = [paddle_whl] + requires

setup(
    name='paddleocr',
    version=__version__.replace('-', ''),
    author="PaddleOCR Contributors",
    author_email="paddle-dev@baidu.com",
    license='Apache 2.0',
    url="https://github.com/PaddlePaddle/PaddleOCR",
    description="Awesome OCR toolkits based on PaddlePaddle (practical ultra lightweight OCR system, support 80+ languages recognition, provide data annotation and synthesis tools, support training and deployment among server, mobile, embedded and IoT devices)",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=all_requires,
    python_requires=f'>=3.7',
    classifiers=[
        f'Programming Language :: Python :: {py_version}',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'paddleocr=ppocr.cli:main',
        ],
    })