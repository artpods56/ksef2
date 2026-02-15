import base64
import json
from os import urandom

from ksef2 import FormSchema
from ksef2.infra.mappers.session import OpenOnlineSessionMapper

key = urandom(32)
iv = urandom(16)

# No need to actually encrypt anything - we just want to test serialization
encrypted_key = base64.b64encode(urandom(256)).decode()
body = OpenOnlineSessionMapper.map_request(encrypted_key, iv, FormSchema.FA3)

dumped = body.model_dump()
print("mode=python:", json.dumps(dumped, indent=2, default=str))

dumped_json = body.model_dump(mode="json")
print("mode=json:", json.dumps(dumped_json, indent=2, default=str))

# Check IV specifically
iv_value = dumped["encryption"]["initializationVector"]
print(f"\nIV in payload: {iv_value}")
print(f"IV type: {type(iv_value)}")

try:
    if isinstance(iv_value, bytes):
        decoded = iv_value
    else:
        decoded = base64.b64decode(iv_value)
    print(f"IV decoded length: {len(decoded)} bytes")
except Exception as e:
    print(f"IV decode error: {e}")

# Compare with original
print(f"\nOriginal IV (base64): {base64.b64encode(iv).decode()}")
print(f"Original IV length: {len(iv)} bytes")
