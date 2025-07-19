"""
Markdown processing functionality for daspress
This module handles markdown content transformation and image processing
"""

import os
import re
import shutil
from typing import Optional, Dict, Callable
from .utils import sanitize_filename
from .status_reporter import StatusReporter


class MarkdownProcessor:
    """
    Process markdown content for Jekyll conversion
    This class can be extended by users for custom processing
    """
    
    def __init__(self, reporter: Optional[StatusReporter] = None):
        """
        Initialize markdown processor
        
        Args:
            reporter (StatusReporter, optional): Status reporter instance
        """
        self.reporter = reporter or StatusReporter()
        self.image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']
        self.obsidian_img_pattern = r'!\[\[(.*?)\]\]'
        self.images_processed = 0  # Add this line
    
    # def process_content(self, content: str, obsidian_img_dir: str, jekyll_img_dir: str) -> str:
    #     """
    #     Process markdown content - main entry point for processing
        
    #     Args:
    #         content (str): Original markdown content
    #         obsidian_img_dir (str): Source images directory
    #         jekyll_img_dir (str): Destination images directory
            
    #     Returns:
    #         str: Processed markdown content
    #     """
    #     # Process images first
    #     processed_content = self.process_images(content, obsidian_img_dir, jekyll_img_dir)
        
    #     # Apply any additional processing
    #     processed_content = self.apply_custom_processing(processed_content)
        
    #     return processed_content

    def process_content(self, content: str, obsidian_img_dir: str, jekyll_img_dir: str) -> str:
        self.images_processed = 0  # Reset counter
        
        # Process images first
        processed_content = self.process_images(content, obsidian_img_dir, jekyll_img_dir)
        
        # Add this summary
        if self.images_processed > 0:
            self.reporter.user_info(f"Images processed: {self.images_processed} image{'s' if self.images_processed != 1 else ''} copied")
        
        # Apply any additional processing
        processed_content = self.apply_custom_processing(processed_content)
        
        return processed_content
    
    def process_images(self, content: str, obsidian_img_dir: str, jekyll_img_dir: str) -> str:
        """
        Process image links in markdown content
        
        Args:
            content (str): Original markdown content
            obsidian_img_dir (str): Source images directory
            jekyll_img_dir (str): Destination images directory
            
        Returns:
            str: Content with processed image links
        """
        def replace_image_link(match):
            return self._replace_single_image(match, obsidian_img_dir, jekyll_img_dir)
        
        return re.sub(self.obsidian_img_pattern, replace_image_link, content)
    
    def _replace_single_image(self, match, obsidian_img_dir: str, jekyll_img_dir: str) -> str:
        """
        Replace a single image link
        
        Args:
            match: Regex match object
            obsidian_img_dir (str): Source images directory
            jekyll_img_dir (str): Destination images directory
            
        Returns:
            str: Replacement string for the image link
        """
        img_filename = match.group(1)
        
        # Handle images without extensions
        if not os.path.splitext(img_filename)[1]:
            img_filename = self._find_image_with_extension(img_filename, obsidian_img_dir)
            if not img_filename:
                self.reporter.warning(f"Image not found with any known extension: {match.group(1)}")
                return match.group(0)  # Return original if not found
        
        # Check if source image exists
        original_img_path = os.path.join(obsidian_img_dir, img_filename)
        if not os.path.exists(original_img_path):
            self.reporter.warning(f"Image not found: {original_img_path}")
            return match.group(0)  # Return original if not found
        
        # Copy image to Jekyll directory
        sanitized_img_name = sanitize_filename(img_filename)
        jekyll_img_path = os.path.join(jekyll_img_dir, sanitized_img_name)
        
        try:
            shutil.copy2(original_img_path, jekyll_img_path)
            self.images_processed += 1
            self.reporter.log(f"Copied image: {original_img_path} → {jekyll_img_path}")  # Keep debug info
        except Exception as e:
            self.reporter.error(f"Failed to copy image {original_img_path}: {e}")
            return match.group(0)  # Return original if copy failed
        
        # Generate Jekyll-compatible image link
        rel_img_path = f"/assets/images/{sanitized_img_name}"
        return self._generate_jekyll_image_link(rel_img_path, img_filename)
    
    def _find_image_with_extension(self, img_filename: str, obsidian_img_dir: str) -> Optional[str]:
        """
        Find image file with common extensions
        
        Args:
            img_filename (str): Image filename without extension
            obsidian_img_dir (str): Directory to search in
            
        Returns:
            str or None: Filename with extension if found, None otherwise
        """
        for ext in self.image_extensions:
            test_file = img_filename + ext
            test_path = os.path.join(obsidian_img_dir, test_file)
            if os.path.exists(test_path):
                return test_file
        return None
    
    def _generate_jekyll_image_link(self, rel_img_path: str, alt_text: str = "") -> str:
        """
        Generate Jekyll-compatible image link
        Override this method to customize image link format
        
        Args:
            rel_img_path (str): Relative image path
            alt_text (str): Alt text for image
            
        Returns:
            str: Jekyll image link
        """
        alt = alt_text if alt_text else "Image"
        return f"![{alt}]({rel_img_path})"
    
    def apply_custom_processing(self, content: str) -> str:
        """
        Apply custom processing to markdown content
        Override this method to add custom processing logic
        
        Args:
            content (str): Markdown content to process
            
        Returns:
            str: Processed content
        """
        # Base implementation does nothing
        # Users can override this method for custom processing
        return content
    
    def set_image_pattern(self, pattern: str):
        """
        Set custom image pattern for processing
        
        Args:
            pattern (str): Regex pattern for image links
        """
        self.obsidian_img_pattern = pattern
    
    def add_image_extension(self, extension: str):
        """
        Add custom image extension
        
        Args:
            extension (str): File extension (e.g., '.bmp')
        """
        if extension not in self.image_extensions:
            self.image_extensions.append(extension)