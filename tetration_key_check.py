"""
tetration_key_check.py displays the capabilities of a Tetration
API key/secret. The capabilities are displayed as a list. If the key
is invalid, it will display an empty list: []

Keyword arguments:
--tetration: URL of the Tetration instance
--credentials: path to a credentials file
--api_key: Tetration API key
--api_secret: Tetration API secret

The user must supply either a credentials file *OR* the key and secret as
arguments, but not both.

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
import requests.packages.urllib3
from tetpyclient import RestClient


# ============================================================================
# Functions
# ----------------------------------------------------------------------------

def get_key_capability(url, api_key, api_secret):
    """ Returns the capabilities of a given API key as a list

    Keyword arguments:
    url -- https url of the Tetration GUI
    api_key -- Tetration API key to be tested
    api_secret -- Tetration API secret for given API key
    """

    # Each API 'capability' is a key in the following dict and the value for
    # each key is *one* API endpoint that requires *only* that capability to
    # return a successful status code.

    api_map = {
        "user_role_scope_management": "/openapi/v1/roles",
        "flow_inventory_query": "/openapi/v1/flowsearch/dimensions",
        "hw_sensor_management": "/openapi/v1/switches",
        "app_policy_management": "/openapi/v1/applications",
        "sensor_management": "/openapi/v1/sensors",
        "user_data_upload": "/openapi/v1/assets/cmdb/download"
    }

    restclient = RestClient(
        url,
        api_key=api_key,
        api_secret=api_secret,
        verify=False
    )

    requests.packages.urllib3.disable_warnings()

    # step through each capability and test the API endpoint associated with
    # it; if we get a status_code of 200, then add it to the list of
    # capabilities of the API key we are testing

    return_list = []
    for capability, endpoint in api_map.iteritems():

        try:
            resp = restclient.get(endpoint)
            if resp.status_code == 200:
                return_list.append(capability)
        except:
            pass

    return [str(x) for x in return_list]

# ============================================================================
# Main
# ----------------------------------------------------------------------------

# The main part of this script simply disassembles the command-line arguments
# and calls the one function in this script using those arguments.

if __name__ == "__main__":

    # ------------------------------------------------------------------------
    # ARGPARSE
    parser = argparse.ArgumentParser(description='Display capabilities of your API key.')
    parser.add_argument('--tetration', required=True, help="URL of Tetration instance")
    parser.add_argument('--credentials', help="path to credentials file")
    parser.add_argument('--api_key', help="Tetration API key")
    parser.add_argument('--api_secret', help="Tetration API secret")
    args = parser.parse_args()

    # User specifies JSON credentials file *OR* the key/secret discretely
    # Either way, we call the api testing function with key/secret
    if args.credentials:
        creds = json.load(open(args.credentials))
        api_key = creds["api_key"]
        api_secret = creds["api_secret"]
    else:
        api_key = args.api_key
        api_secret = args.api_secret

    print get_key_capability(args.tetration, api_key, api_secret)
