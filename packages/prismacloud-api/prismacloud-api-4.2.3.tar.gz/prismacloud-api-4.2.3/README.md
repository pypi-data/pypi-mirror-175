# Python SDK for the Prisma Cloud APIs

This project includes a Python SDK for the Prisma Cloud APIs (CSPM, CWPP, and PCCS) in the form of a Python package.
It also includes reference scripts that utilize the SDK.

Major changes with Version 4.0:

* Published as a Python package.
* Uses `~/.prismacloud/` instead of the current working directory as its default configuration file directory.
* Uses `~/.prismacloud/credentials.json` instead of `pc-settings.conf` as its default configuration file.

## Table of Contents

* [Setup](#Setup)
* [Support](#Support)


## Setup

Install the SDK via:

```
pip3 install prismacloud-api
```

### Reference Scripts

Please refer to the example/reference [scripts](https://github.com/PaloAltoNetworks/prismacloud-api-python/tree/main/scripts) directory for script documentation and usage details.

## Support

This project has been developed by Prisma Cloud SEs, it is not Supported by Palo Alto Networks.
Nevertheless, the maintainers will make a best-effort to address issues, and (of course) contributors are encouraged to submit issues and pull requests.
