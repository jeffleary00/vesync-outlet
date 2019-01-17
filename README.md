# vesync-outlet
Python module to control Vesync WiFi power outlets

## Installation
```
pip3 install vesync-outlet
```

## Usage
```
from vesync_outlet import Vesync

hashpw = hashlib.md5(password.encode('utf-8')).hexdigest()

vesync = Vesync(username, hashpw)
devices, response = vesync.get_outlets()
for d in devices:
  data, response = vesync.turn_on(d['id'])
  data, response = vesync.turn_off(d['id'])
```

## Methods
The methods below return a tuple. The first element is the payload data.
If this entry is None, check results in the response object for errors.

### get_devices()
Get all wifi-switch outlet devices from Vesync api.

Arguments: none
Returns: ( payload, requests.response )

### turn_off(id)
Switch an outlet to OFF.

Arguments: the device ID
Returns: ( payload, requests.response )

### turn_on(id)
Switch an outlet to ON.

Arguments: the device ID
Returns: ( payload, requests.response )
