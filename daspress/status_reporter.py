"""
Status reporting utilities for daspress
"""

import json
import sys
from enum import Enum
from typing import Dict, Any, Optional


class StatusCode(Enum):
    """Status codes for daspress operations"""
    SUCCESS = 0
    ERROR_INVALID_ARGS = 1
    ERROR_FILE_NOT_FOUND = 2
    ERROR_PERMISSION_DENIED = 3
    ERROR_PROCESSING = 4
    ERROR_JEKYLL_SERVER = 5


class StatusReporter:
    """Handle status reporting for daspress operations"""
    
    def __init__(self, verbose: bool = True, json_output: bool = False, debug_mode: bool = False):
        """
        Initialize status reporter
        
        Args:
            verbose (bool): Whether to print verbose messages
            json_output (bool): Whether to output JSON format
            debug_mode (bool): Whether to show debug information
        """
        self.verbose = verbose
        self.json_output = json_output
        self.debug_mode = debug_mode  # ADD THIS LINE
        self.messages = []
    
    
    # def user_info(self, message: str):
    #     """Log user-friendly info message with checkmark"""
    #     if self.verbose and not self.json_output:
    #         print(f"✓ {message}")
        
    #     # Still keep for debugging
    #     self.log(message, "INFO")

    def user_info(self, message: str):
        """Log user-friendly info message with checkmark"""
        if self.verbose and not self.json_output:
            try:
                print(f"✓ {message}")
            except UnicodeEncodeError:
                # Fallback for systems that can't handle Unicode
                print(f"[OK] {message}")
            
        # Still keep for debugging
        self.log(message, "INFO")

    def log(self, message: str, level: str = "INFO"):
        """
        Log a message
        
        Args:
            message (str): Message to log
            level (str): Log level (INFO, WARNING, ERROR, SUCCESS)
        """
        log_entry = {
            "level": level,
            "message": message
        }
        self.messages.append(log_entry)
        
        # REPLACE the existing print logic with this:
        if self.verbose and not self.json_output and self.debug_mode:
            prefix = f"[{level}]" if level != "INFO" else ""
            print(f"{prefix} {message}")
    
    def success(self, message: str):
        """Log a success message"""
        self.log(message, "SUCCESS")
    
    def warning(self, message: str):
        """Log a warning message"""
        self.log(message, "WARNING")
    
    def error(self, message: str):
        """Log an error message"""
        self.log(message, "ERROR")
    
    def report_final_status(self, status_code: StatusCode, summary: str = ""):
        """
        Report final status of operation
        
        Args:
            status_code (StatusCode): Final status code
            summary (str): Summary message
        """
        final_report = {
            "status_code": status_code.value,
            "status_name": status_code.name,
            "summary": summary,
            "messages": self.messages
        }
        
        if self.json_output:
            print(json.dumps(final_report, indent=2))
        else:
            if summary:
                level = "SUCCESS" if status_code == StatusCode.SUCCESS else "ERROR"
                self.log(summary, level)
        
        # Exit with appropriate code for command line usage
        sys.exit(status_code.value)
    
    def get_status_dict(self) -> Dict[str, Any]:
        """
        Get current status as dictionary
        
        Returns:
            dict: Status information
        """
        return {
            "messages": self.messages,
            "message_count": len(self.messages),
            "has_errors": any(msg["level"] == "ERROR" for msg in self.messages),
            "has_warnings": any(msg["level"] == "WARNING" for msg in self.messages)
        }