import os
from .common import *

try:
    import environment
except ImportError:
    pass

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT") or "development"

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "testing":
    from .testing import *
else:
    from .development import *

try:
    from .local import *
except ImportError:
    pass