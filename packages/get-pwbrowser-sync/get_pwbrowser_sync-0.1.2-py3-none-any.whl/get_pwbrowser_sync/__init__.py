"""Init."""
__version__ = "0.1.2"
from .get_pwbrowser_sync import get_pwbrowser_sync
from .get_pwbrowser_sync import loop

# from .get_pwbrowser_async import get_pwbrowser as get_pwbrowser_async

# import nest_asyncio
# nest_asyncio.apply()

__all__ = [
    "get_pwbrowser_sync",
    "loop",
]
