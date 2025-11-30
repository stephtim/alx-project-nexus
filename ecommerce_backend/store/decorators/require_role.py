from functools import wraps
from django.http import HttpResponseForbidden

def require_role(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not user or not user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            if not user.userrole_set.filter(role__name=role_name).exists():
                return HttpResponseForbidden("Insufficient role")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
