# Version 0.2.1
## Bug Fixes
* Fixes a race condition where Future.set_result would raise InvalidStateError if another producer set a result already
## Added
* Changelog to pypi long description

# Version 0.2.0
## Added
* Adds `IPC.on_error` handler for when a handler errors out. Takes error as first argument and message (the request data) as second

# Version 0.1.0
## Added
* required_identity kwarg on `IPC.get` and `IPC.publish`
* added more comments to examples
* added basic logging


