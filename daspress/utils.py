"""
Utility functions for daspress
"""

import os
import re


def sanitize_filename(name):
    """
    Sanitize filename by replacing spaces with hyphens
    
    Args:
        name (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    return name.replace(" ", "-")


def ensure_directory_exists(directory_path):
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory_path (str): Path to directory
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except OSError as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def validate_file_exists(file_path):
    """
    Validate if a file exists and is readable
    
    Args:
        file_path (str): Path to file
        
    Returns:
        tuple: (bool, str) - (success, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"File does not exist: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1)  # Try to read one character
        return True, ""
    except PermissionError:
        return False, f"Cannot read file due to permission issue: {file_path}"
    except Exception as e:
        return False, f"Error reading file {file_path}: {e}"


def validate_directory_exists(directory_path):
    """
    Validate if a directory exists
    
    Args:
        directory_path (str): Path to directory
        
    Returns:
        tuple: (bool, str) - (success, error_message)
    """
    if not os.path.exists(directory_path):
        return False, f"Directory does not exist: {directory_path}"
    
    if not os.path.isdir(directory_path):
        return False, f"Path is not a directory: {directory_path}"
    
    return True, ""