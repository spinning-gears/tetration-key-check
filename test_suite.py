"""
test_suite.py is used to exercise the get_key_capability function in the
tetration_key_check.py file. It allows the user to specify a JSON file with
many key/secret values and their expected capabilities. This script will step
through each one and compare its actual results to its expected results.

Keyword arguments:
--tetration: URL of the Tetration instance
--credentials: path to a JSON file with multiple credentials

Look at example.JSON for the expected format of the JSON file.

Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Doron Chosnek"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"

# pylint: disable=invalid-name

import json
import argparse

# ------------------------------------------------------------------------
# ARGPARSE
parser = argparse.ArgumentParser(description='Display capabilities of your API key.')
parser.add_argument('--tetration', required=True, help="URL of Tetration instance")
parser.add_argument('--credentials', required=True, help="path to credentials file")
args = parser.parse_args()

# import the primary key checking function
from tetration_key_check import get_key_capability

# step through every credential set in the JSON file and compare the expected
# result to the actual result; display success or failure message
for entry in json.load(open(args.credentials)):
    result = get_key_capability(args.tetration, entry["api_key"], entry["api_secret"])

    if set(result) == set(entry["expect"]):
        msg = "success"
    else:
        msg = "ERROR!"
    
    print "{}: {}".format(entry["api_key"], msg)
