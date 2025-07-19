"""
Entry point for running daspress as a module
"""

import sys
import os

# Enhanced UTF-8 handling for both standalone and package modes
def setup_utf8_encoding():
    """Setup UTF-8 encoding for both development and bundled environments"""
    
    # Set environment variables (works for subprocess calls)
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # Additional fix for PyInstaller bundled executable
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle - need aggressive UTF-8 setup
        try:
            import io
            
            # Wrap stdout/stderr with UTF-8 encoding
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer, 
                    encoding='utf-8', 
                    errors='replace',
                    line_buffering=True
                )
            
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer, 
                    encoding='utf-8', 
                    errors='replace',
                    line_buffering=True
                )
        except Exception:
            # If UTF-8 setup fails, continue with default encoding
            pass

# Setup encoding before any other imports
setup_utf8_encoding()

try:
    from .cli import main
except ImportError:
    from daspress.cli import main  # Fixed: full module path

if __name__ == '__main__':
    main()


# """
# Entry point for running daspress as a module
# """

# import os
# # Set UTF-8 encoding before importing anything else
# os.environ['PYTHONIOENCODING'] = 'utf-8'

# try:
#     from .cli import main
# except ImportError:
#     from daspress.cli import main  # Fixed: full module path

# if __name__ == '__main__':
#     main()