"""
Command line interface for daspress
"""

import argparse
import sys
import os
from typing import Optional

# Set UTF-8 encoding for the entire process
os.environ['PYTHONIOENCODING'] = 'utf-8'

from .converter import DaspressConverter
from .config import DaspressConfig
from .status_reporter import StatusReporter, StatusCode
from . import __version__

def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        prog='daspress',
        description='Convert Obsidian posts to Jekyll format'
    )
    
    # Clean subcommand structure - no mixing with backward compatibility
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Interactive setup wizard')
    
    # Convert command (Feature 1: Convert only)
    convert_parser = subparsers.add_parser('convert', help='Convert Obsidian post to Jekyll')
    convert_parser.add_argument('blog_name', help='Name of the blog post file')
    
    # Local command (Feature 2: Convert + local server)
    local_parser = subparsers.add_parser('local', help='Convert and start local Jekyll server')
    local_parser.add_argument('blog_name', help='Name of the blog post file')
    
    # Remote command (Feature 3: Convert + git publish)
    remote_parser = subparsers.add_parser('remote', help='Convert and publish to git repository')
    remote_parser.add_argument('blog_name', help='Name of the blog post file')
    
    # Both command (Feature 4: Convert + local + remote)
    both_parser = subparsers.add_parser('both', help='Convert, run locally and publish remotely')
    both_parser.add_argument('blog_name', help='Name of the blog post file')
    
    # Global options (apply to all commands)
    parser.add_argument('--config', type=str, help='Path to custom config file')
    parser.add_argument('--json', action='store_true', help='Output status in JSON format')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress verbose output')
    parser.add_argument('--debug', action='store_true', help='Show detailed debug information')
    parser.add_argument('--version', action='version', version=f'daspress {__version__}')
    
    return parser



def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup status reporter
    reporter = StatusReporter(
        verbose=not args.quiet,
        json_output=args.json,
        debug_mode=args.debug
    )   
    
    # Handle setup command
    if args.command == 'setup':
        config = DaspressConfig(
            config_path=args.config,
            reporter=reporter
        )
        
        if config.interactive_setup():
            reporter.report_final_status(
                StatusCode.SUCCESS,
                "Setup completed successfully"
            )
        else:
            reporter.report_final_status(
                StatusCode.ERROR_PROCESSING,
                "Setup failed"
            )
        return
    
    # All other commands need blog_name and config
    blog_name = args.blog_name
    
    # Setup config and converter
    config = DaspressConfig(
        config_path=args.config,
        reporter=reporter
    )
    
    converter = DaspressConverter(
        config=config,
        reporter=reporter
    )
    
    # Determine publishing mode based on command
    publishing_modes = {
        'convert': 'convert_only',
        'local': 'local_only', 
        'remote': 'remote_only',
        'both': 'both'
    }
    
    publishing_mode = publishing_modes.get(args.command, 'convert_only')
    
    # Perform conversion with publishing
    try:
        success = converter.convert_and_publish(
            blog_name=blog_name,
            publishing_mode=publishing_mode
        )
        
        if success:
            reporter.report_final_status(
                StatusCode.SUCCESS,
                f"Successfully processed '{blog_name}' with mode '{args.command}'"
            )
        else:
            reporter.report_final_status(
                StatusCode.ERROR_PROCESSING,
                f"Failed to process '{blog_name}'"
            )
            
    except KeyboardInterrupt:
        reporter.report_final_status(
            StatusCode.ERROR_PROCESSING,
            "Process interrupted by user"
        )
    except Exception as e:
        reporter.report_final_status(
            StatusCode.ERROR_PROCESSING,
            f"Unexpected error: {e}"
        )

if __name__ == '__main__':
    main()