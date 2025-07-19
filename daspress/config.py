"""
Configuration management for daspress
"""

import os
import yaml
from typing import Dict, Optional, Tuple
from .status_reporter import StatusReporter


class DaspressConfig:
    """Handle configuration file for daspress"""
    
    def __init__(self, config_path: Optional[str] = None, reporter: Optional[StatusReporter] = None):
        """
        Initialize config handler
        
        Args:
            config_path (str, optional): Path to config file
            reporter (StatusReporter, optional): Status reporter instance
        """
        self.reporter = reporter or StatusReporter()
        self.config_path = config_path or self._get_default_config_path()
        self.config_data = {}
    
    def load_config(self) -> bool:
        """
        Load configuration from file
        
        Returns:
            bool: True if config loaded successfully
        """
        if not os.path.exists(self.config_path):
            return self._create_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f) or {}
            
            if self._validate_config():
                self.reporter.user_info("Configuration loaded")
                self.reporter.log(f"Configuration loaded from: {self.config_path}")  # Keep debug info
                return True
            else:
                return False
                
        except yaml.YAMLError as e:
            self.reporter.error(f"Invalid YAML in config file: {e}")
            return False
        except Exception as e:
            self.reporter.error(f"Failed to load config file: {e}")
            return False
    
    def _create_default_config(self) -> bool:
        """Create default configuration file"""
        default_config = {
            'obsidian': {
                'posts_folder': '/path/to/your/obsidian/posts',
                'images_folder': '/path/to/your/obsidian/posts/attachments'
            },
            'jekyll': {
                'root_folder': '/path/to/your/jekyll/blog'
            }
        }
        # ... rest stays the same
    
    def _validate_config(self) -> bool:
        """Validate configuration structure and paths"""
        # Check required sections (same as before)
        if 'obsidian' not in self.config_data:
            self.reporter.error("Config missing 'obsidian' section")
            return False
        
        if 'jekyll' not in self.config_data:
            self.reporter.error("Config missing 'jekyll' section")
            return False
        
        # Check required fields - UPDATED
        required_fields = {
            'obsidian': ['posts_folder', 'images_folder'],
            'jekyll': ['root_folder']  # Only root_folder now
        }
        
        for section, fields in required_fields.items():
            for field in fields:
                if field not in self.config_data[section]:
                    self.reporter.error(f"Config missing '{section}.{field}' field")
                    return False
                
                path = self.config_data[section][field]
                if not path or path.startswith('/path/to/'):
                    self.reporter.error(f"Please update '{section}.{field}' with your actual path")
                    return False
        
        # Validate paths exist
        obsidian_posts = self.config_data['obsidian']['posts_folder']
        obsidian_images = self.config_data['obsidian']['images_folder']
        jekyll_root = self.config_data['jekyll']['root_folder']
        
        if not os.path.exists(obsidian_posts):
            self.reporter.error(f"Obsidian posts folder does not exist: {obsidian_posts}")
            return False
        
        if not os.path.exists(obsidian_images):
            self.reporter.error(f"Obsidian images folder does not exist: {obsidian_images}")
            return False
        
        if not os.path.exists(jekyll_root):
            self.reporter.error(f"Jekyll root folder does not exist: {jekyll_root}")
            return False
        
        # NEW: Validate Jekyll structure
        return self._validate_jekyll_structure(jekyll_root)
    
    def get_obsidian_posts_folder(self) -> str:
        """Get obsidian posts folder path"""
        return self.config_data['obsidian']['posts_folder']
    
    def get_obsidian_images_folder(self) -> str:
        """Get obsidian images folder path"""
        return self.config_data['obsidian']['images_folder']
    
    def get_jekyll_posts_folder(self) -> str:
        """Get jekyll posts folder path"""
        return self.config_data['jekyll']['posts_folder']
    
    def get_jekyll_images_folder(self) -> str:
        """Get jekyll images folder path"""
        return self.config_data['jekyll']['images_folder']
    
    def _get_default_config_path(self) -> str:
        """
        Get default config file path
        
        Returns:
            str: Default config file path
        """
        # Try current directory first, then user home
        current_dir_config = os.path.join(os.getcwd(), 'daspress-config.yaml')
        if os.path.exists(current_dir_config):
            return current_dir_config
        
        home_dir = os.path.expanduser('~')
        return os.path.join(home_dir, '.daspress', 'config.yaml')
    
    def get_config_path(self) -> str:
        """Get current config file path"""
        return self.config_path
    

    def _validate_jekyll_structure(self, jekyll_root: str) -> bool:
        """Validate Jekyll blog structure"""
        posts_dir = os.path.join(jekyll_root, '_posts')
        assets_dir = os.path.join(jekyll_root, 'assets')
        images_dir = os.path.join(jekyll_root, 'assets', 'images')
        
        if not os.path.exists(posts_dir):
            self.reporter.error(f"Jekyll _posts folder not found: {posts_dir}")
            return False
        
        if not os.path.exists(assets_dir):
            self.reporter.warning(f"Jekyll assets folder not found, will create: {assets_dir}")
            os.makedirs(assets_dir, exist_ok=True)
        
        if not os.path.exists(images_dir):
            self.reporter.warning(f"Jekyll images folder not found, will create: {images_dir}")
            os.makedirs(images_dir, exist_ok=True)
        
        return True

    def get_jekyll_root_folder(self) -> str:
        """Get jekyll root folder path"""
        return self.config_data['jekyll']['root_folder']

    def get_jekyll_posts_folder(self) -> str:
        """Get jekyll posts folder path - auto-calculated"""
        return os.path.join(self.get_jekyll_root_folder(), '_posts')

    def get_jekyll_images_folder(self) -> str:
        """Get jekyll images folder path - auto-calculated"""
        return os.path.join(self.get_jekyll_root_folder(), 'assets', 'images')

    def interactive_setup(self) -> bool:
        """Run interactive setup wizard"""
        self.reporter.log("Welcome to daspress! Let's set up your publishing pipeline.")
        
        # Get Obsidian posts folder
        obsidian_posts = input("\n1. Where is your Obsidian posts folder?\n   → ").strip()
        if not os.path.exists(obsidian_posts):
            self.reporter.error(f"Folder does not exist: {obsidian_posts}")
            return False
        
        # Auto-detect or ask for images folder
        obsidian_images = os.path.join(obsidian_posts, 'attachments')
        if os.path.exists(obsidian_images):
            self.reporter.log(f"Found images folder: {obsidian_images}")
        else:
            obsidian_images = input(f"\n2. Where is your Obsidian images folder? ({obsidian_images})\n   → ").strip()
            if not obsidian_images:
                obsidian_images = os.path.join(obsidian_posts, 'attachments')
        
        # Get Jekyll root folder
        jekyll_root = input("\n3. Where is your Jekyll blog root directory?\n   → ").strip()
        if not os.path.exists(jekyll_root):
            self.reporter.error(f"Folder does not exist: {jekyll_root}")
            return False
        
        # Create config
        self.config_data = {
            'obsidian': {
                'posts_folder': obsidian_posts,
                'images_folder': obsidian_images
            },
            'jekyll': {
                'root_folder': jekyll_root
            }
        }
        
        # Validate and save
        if self._validate_config():
            try:
                config_dir = os.path.dirname(self.config_path)
                if config_dir:
                    os.makedirs(config_dir, exist_ok=True)
                
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.config_data, f, default_flow_style=False, indent=2)
                
                self.reporter.success(f"✅ Configuration saved to: {self.config_path}")
                self.reporter.log("\n🔧 OBSIDIAN SETUP:")
                self.reporter.log("Add this command to Obsidian Shell Commands:")
                self.reporter.log('  Command: daspress "{{file_name}}" --serve')
                self.reporter.log("✨ You're ready! Use the button in Obsidian to publish.")
                return True
                
            except Exception as e:
                self.reporter.error(f"Failed to save config: {e}")
                return False
        
        return False