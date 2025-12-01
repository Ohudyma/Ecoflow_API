
# Ecoflow_Delta2_Max_API

Python module to get and set parameters for Ecoflow Delta 2 Max and Ecoflow E2000
## Supported Python Versions

This library supports the following Python implementations:

* Python 3.10
* Python 3.11

Lower versions did not checked.

## Installation

Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a package manager for Python.

```bash
  pip3 install Ecoflow_Delta2_Max_API
  #or
  poetry add git+https://github.com/Ohudyma/Ecoflow_Delta2_Max_API
```
    
## Usage
### API Credentials
The Ecoflow client needs your Ecoflow API credentials. 
You can obtain access_key and secret_key on the page https://developer-eu.ecoflow.com/us/security and then pass these directly to the constructor.
Serial number - you can get from Ecoflow device package.

### Make a Call 
```javascript
import Ecoflow_Delta2_Max_API

access_key = "*********"
secret_Key  = "*********"
DEVICE_SN = "*********"
#Disable/enable logs (0 - disable, 1 - enable)
log_lvl = "1"

request_data_get = {"sn": DEVICE_SN,
                    "params": {
                        "quotas": ["pd.soc",
                                   "inv.SlowChgWatts",
                                   "bms_bmsStatus.cycSoh",
                                   "bms_bmsInfo.soh",
                                   "inv.inputWatts",
                                   "pd.invOutWatts",
                                   "pd.chgDsgState",
                                   "bms_emsStatus.chgRemainTime", 
                                   "bms_emsStatus.dsgRemainTime"
                                   ]
                               }
                    }

request_data_set = {"id": 123,
                    "version": "1.0",
                    "sn": DEVICE_SN,
                    "moduleType": 3,
                    "operateType": "acChgCfg",
                    "params": {"fastChgWatts": 2400,
                               "slowChgWatts": 500,
                               "chgPauseFlag": 0}
                    }

api = Ecoflow_Delta2_Max_API(sn=DEVICE_SN, access_key=access_key, secret_key=secret_Key, log_lvl=log_lvl)

#Get all device parameters (request_data=None)
resp_get_all_device_quotas = api.get_all_device_quotas(request_data=None)
print(resp_get_all_device_quotas)

#Get some device device parameters from dict request_data_get
resp_get_device_quotas = api.get_device_quotas(request_data=request_data_get)
print(resp_get_device_quotas)

#Set parameters on the device (change input power in example)
resp_set_device_quota = api.set_device_quota(request_data=request_data_set)
print(resp_set_device_quota)
```


## Donation

You can support the developer with a donation:

PayPal - will update later

Monobank - 4441 1144 1446 0376


## Feedback

If you have any feedback, please reach out to us at oleksii.hudyma@gmail.com


