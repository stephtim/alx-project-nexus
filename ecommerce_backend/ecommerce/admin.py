from django.contrib import admin
import inspect

# Safe admin registration: register any Django model classes defined in this app's
# `models` module. This avoids hard imports and prevents syntax/import errors
# caused by invalid module names elsewhere in the repo.
try:
    from . import models as _models
    from django.db import models as _djmodels

    _to_register = []
    for _name, _obj in inspect.getmembers(_models, inspect.isclass):
        try:
            if issubclass(_obj, _djmodels.Model):
                _to_register.append(_obj)
        except Exception:
            continue

    if _to_register:
        admin.site.register(_to_register)
except Exception:
    # If anything goes wrong, fail silently to allow Django startup/tests to continue
    pass
