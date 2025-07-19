"""
daspress Pro - Complete blog publishing system
Convert Obsidian posts to Jekyll format with premium features
"""

__version__ = "2.0.0"  
__author__ = "Shuvangkar Das"
__description__ = "Complete Obsidian to Jekyll blog publishing system"

from .converter import DaspressConverter
from .markdown_processor import MarkdownProcessor
from .status_reporter import StatusReporter
from .config import DaspressConfig

__all__ = ['DaspressConverter', 'MarkdownProcessor', 'StatusReporter', 'DaspressConfig']


# """
# daspress Pro - Complete blog publishing system
# Convert Obsidian posts to Jekyll format with premium features
# """

# __version__ = "1.0.0"
# __author__ = "Your Name"
# __description__ = "Complete Obsidian to Jekyll blog publishing system with premium features"
# __license__ = "Proprietary"

# # Pro version identifier
# __pro_version__ = True

# from .converter import DaspressConverter
# from .markdown_processor import MarkdownProcessor
# from .status_reporter import StatusReporter
# from .config import DaspressConfig

# __all__ = ['DaspressConverter', 'MarkdownProcessor', 'StatusReporter', 'DaspressConfig']

# def is_pro_version():
#     """Check if this is the Pro version"""
#     return __pro_version__

# def get_version_info():
#     """Get version information"""
#     return {
#         'version': __version__,
#         'pro': __pro_version__,
#         'author': __author__,
#         'description': __description__
#     }