try:
    from .views import *
except ImportError:
    # Fallback si el directorio views/ no existe aún
    pass