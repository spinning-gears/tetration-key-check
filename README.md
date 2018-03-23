# Tetration API key checker

Each Tetration API endpoint requires a specific API "capability" (like a user role). Although one can generate an API key that has all capabilites, best practice dictates creating keys with only the privileges required to perform the task at hand.

It's easy for a user to end up with one or more API keys whose capabilities they're unsure of. The contents of this repository will help determine the capability of any Tetration API key.

## API Capabilties

As of Tetration 2.X, the following capabilities exist in Tetration:
- user_role_scope_management
- flow_inventory_query
- hw_sensor_management
- app_policy_management
- sensor_management
- user_data_upload
- external_integration (this capability is for **alpha** API endpoints in Tetration so this script does not check for this capability)

## Testing one API key

In order to test one API key at a time, you can supply the API key and secret as a JSON credentials file:

```
python tetration_key_check.py --tetration https://example.com --credentials api_credentials.json
```

Or you can supply the API key and secret as command-line arguments:

```python
python tetration_key_check.py --tetration https://example.com --api_key XXXX --api_secret YYYY
```

## Testing many API keys

`test_suite.py` was created in order to validate the functionality of the script that tests one API key/secret at a time. This tests multiple key/secret pairs (stored in a JSON file) against their *expected* values. I don't expect most people to run `test_suite.py` but included it here for completeness.

```python
python test_suite.py --tetration https://example.com --credentials example.json
```

The JSON file specifying multiple API key/secret pairs follows the format below. In this example, there are two API key/secret pairs in the file. The first one is expected to have one capability while the second one is expected to have three capabilities.

```json
[
    {
        "api_key": "abc",
        "api_secret": "def",
        "expect": [
            "user_role_scope_management"
        ]
    },
    {
        "api_key": "ghi",
        "api_secret": "jkl",
        "expect": [
            "flow_inventory_query",
            "app_policy_management",
            "hw_sensor_management"
        ]
    }
]
```

The test suite would check each API key/secret pair against Tetration and display a success or failure message if the capabilities of that key/secret did not **exactly** match the *expected* values in the JSON file.