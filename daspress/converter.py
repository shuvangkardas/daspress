"""
Main converter class for daspress
"""

import os
import shutil
import subprocess
from typing import Optional, Dict, Any



from .utils import (
    sanitize_filename, 
    ensure_directory_exists, 
    validate_file_exists, 
    validate_directory_exists
)
from .status_reporter import StatusReporter, StatusCode
from .markdown_processor import MarkdownProcessor
from .config import DaspressConfig


class DaspressConverter:
    """
    Main converter class for Obsidian to Jekyll conversion
    """
    
    def __init__(self, 
                 config: Optional[DaspressConfig] = None,
                 reporter: Optional[StatusReporter] = None,
                 markdown_processor: Optional[MarkdownProcessor] = None):
        """
        Initialize the converter
        
        Args:
            config (DaspressConfig, optional): Configuration instance
            reporter (StatusReporter, optional): Status reporter instance
            markdown_processor (MarkdownProcessor, optional): Markdown processor instance
        """
        self.reporter = reporter or StatusReporter()
        self.config = config or DaspressConfig(reporter=self.reporter)
        self.markdown_processor = markdown_processor or MarkdownProcessor(self.reporter)
    
    def convert(self, blog_name: str, start_server: bool = False) -> bool:
        """
        Convert Obsidian post to Jekyll format
        
        Args:
            blog_name (str): Name of the blog post file
            start_server (bool): Whether to start Jekyll server after conversion
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Load configuration
            if not self.config.load_config():
                return False
            
            # Validate inputs
            if not self._validate_inputs(blog_name):
                return False
            
            # Setup paths
            paths = self._setup_paths(blog_name)
            
            # Create necessary directories
            if not self._create_directories(paths):
                return False
            
            # Process the conversion
            if not self._process_conversion(paths):
                return False
            
            self.reporter.success(f"Conversion completed successfully: {paths['jekyll_md_path']}")
            
            # Start Jekyll server if requested
            if start_server:
                self._start_jekyll_server()
            
            return True
            
        except Exception as e:
            self.reporter.error(f"Unexpected error during conversion: {e}")
            return False
    
    def _validate_inputs(self, blog_name: str) -> bool:
        """
        Validate input parameters
        
        Args:
            blog_name (str): Name of the blog post file
            
        Returns:
            bool: True if inputs are valid
        """
        # Validate blog name
        if not blog_name or blog_name.strip() == "":
            self.reporter.error("Blog name cannot be empty")
            return False
        
        return True
    
    def _setup_paths(self, blog_name: str) -> Dict[str, str]:
        """
        Setup all required paths for conversion using config
        
        Args:
            blog_name (str): Name of the blog post file OR full path
            
        Returns:
            dict: Dictionary containing all paths
        """
        # Check if blog_name is already a full path (from Obsidian)
        if os.path.isabs(blog_name) and os.path.exists(blog_name):
            # Full path provided (from Obsidian {{file_path:absolute}})
            obsidian_md_path = blog_name
            actual_filename = os.path.basename(blog_name)
        else:
            # Relative path (original behavior for unit tests)
            obsidian_posts_dir = self.config.get_obsidian_posts_folder()
            obsidian_md_path = os.path.join(obsidian_posts_dir, blog_name)
            actual_filename = blog_name
        
        # Source paths from config
        obsidian_img_dir = self.config.get_obsidian_images_folder()
        
        # Destination paths from config - use actual filename for Jekyll
        jekyll_post_name = sanitize_filename(actual_filename)
        jekyll_img_dir = self.config.get_jekyll_images_folder()
        jekyll_post_dir = self.config.get_jekyll_posts_folder()
        jekyll_md_path = os.path.join(jekyll_post_dir, jekyll_post_name)
        
        return {
            'obsidian_md_path': obsidian_md_path,
            'obsidian_img_dir': obsidian_img_dir,
            'jekyll_img_dir': jekyll_img_dir,
            'jekyll_post_dir': jekyll_post_dir,
            'jekyll_md_path': jekyll_md_path
        }

        


    
    def _create_directories(self, paths: Dict[str, str]) -> bool:
        """
        Create necessary directories
        
        Args:
            paths (dict): Dictionary containing paths
            
        Returns:
            bool: True if directories created successfully
        """
        # Ensure Jekyll directories exist
        if not ensure_directory_exists(paths['jekyll_img_dir']):
            self.reporter.error(f"Failed to create Jekyll images directory: {paths['jekyll_img_dir']}")
            return False
        
        if not ensure_directory_exists(paths['jekyll_post_dir']):
            self.reporter.error(f"Failed to create Jekyll posts directory: {paths['jekyll_post_dir']}")
            return False
        
        # Validate obsidian images directory exists
        is_valid, error_msg = validate_directory_exists(paths['obsidian_img_dir'])
        if not is_valid:
            self.reporter.error(error_msg)
            return False
        
        return True
    
    
    def _process_conversion(self, paths: Dict[str, str]) -> bool:
        """
        Process the actual conversion
        
        Args:
            paths (dict): Dictionary containing paths
            
        Returns:
            bool: True if conversion successful
        """
        # Validate source markdown file
        is_valid, error_msg = validate_file_exists(paths['obsidian_md_path'])
        if not is_valid:
            self.reporter.error(error_msg)
            return False
        
        # Copy markdown file to Jekyll directory
        try:
            shutil.copy2(paths['obsidian_md_path'], paths['jekyll_md_path'])
            filename = os.path.basename(paths['obsidian_md_path'])
            self.reporter.user_info(f"Blog post: \"{filename}\" copied")
            self.reporter.log(f"Copied blog post: {paths['obsidian_md_path']} → {paths['jekyll_md_path']}")  # Keep debug info
        except Exception as e:
            self.reporter.error(f"Failed to copy blog post: {e}")
            return False
        
        # Read the copied markdown file
        try:
            with open(paths['jekyll_md_path'], 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.reporter.error(f"Failed to read copied markdown file: {e}")
            return False
        
        # Process markdown content
        try:
            processed_content = self.markdown_processor.process_content(
                content, 
                paths['obsidian_img_dir'], 
                paths['jekyll_img_dir']
            )
        except Exception as e:
            self.reporter.error(f"Failed to process markdown content: {e}")
            return False
        
        # Write processed content back to file
        try:
            with open(paths['jekyll_md_path'], 'w', encoding='utf-8') as f:
                f.write(processed_content)
            self.reporter.log(f"Processed markdown content saved to: {paths['jekyll_md_path']}")
        except Exception as e:
            self.reporter.error(f"Failed to write processed content: {e}")
            return False
        
        return True
    
    

    def _start_jekyll_server(self):
        """Start Jekyll server in Jekyll directory"""
        try:
            jekyll_root = self.config.get_jekyll_root_folder()
            self.reporter.user_info("Starting Jekyll server...")
            self.reporter.user_info("Server will be available at: http://localhost:4000")
            self.reporter.log("Press Ctrl+C to stop the server")
            
            subprocess.run(
                "bundle exec jekyll serve", 
                cwd=jekyll_root,
                shell=True,
                check=True
            )
            self.reporter.success("Jekyll server stopped")
            
        except subprocess.CalledProcessError as e:
            self.reporter.error(f"Failed to start Jekyll server: {e}")
        except KeyboardInterrupt:
            self.reporter.user_info("Jekyll server stopped by user")
        except Exception as e:
            self.reporter.error(f"Unexpected error starting Jekyll server: {e}")


        
    def set_config_path(self, config_path: str):
        """
        Set custom config file path
        
        Args:
            config_path (str): Path to config file
        """
        self.config = DaspressConfig(config_path, self.reporter)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the converter
        
        Returns:
            dict: Status information
        """
        return self.reporter.get_status_dict()
    

    def convert_and_publish(self, blog_name: str, publishing_mode: str = "convert_only") -> bool:
        """
        Convert Obsidian post to Jekyll format with publishing options
        
        Args:
            blog_name (str): Name of the blog post file
            publishing_mode (str): One of: convert_only, local_only, remote_only, both
            
        Returns:
            bool: True if operation successful, False otherwise
        """
        try:
            # Load configuration
            if not self.config.load_config():
                return False
            
            # Validate inputs
            if not self._validate_inputs(blog_name):
                return False
            
            # Setup paths
            paths = self._setup_paths(blog_name)
            
            # Create necessary directories
            if not self._create_directories(paths):
                return False
            
            # Process the conversion
            if not self._process_conversion(paths):
                return False
            
            self.reporter.success(f"Conversion completed: {paths['jekyll_md_path']}")
            
            # Handle publishing based on mode
            return self._handle_publishing_mode(publishing_mode)
            
        except Exception as e:
            self.reporter.error(f"Unexpected error during conversion: {e}")
            return False
        


    def _handle_publishing_mode(self, publishing_mode: str) -> bool:
        """
        Handle publishing based on mode
        
        Args:
            publishing_mode (str): Publishing mode
            
        Returns:
            bool: True if publishing successful
        """
        if publishing_mode == "convert_only":
            self.reporter.log("Conversion complete. No publishing requested.")
            return True
            
        elif publishing_mode == "local_only":
            # Give immediate feedback
            self.reporter.user_info("Conversion completed")
            self.reporter.user_info("Starting Jekyll server in background...")
            self.reporter.user_info("Server will be available at http://localhost:4000 in 30-60 seconds")
            
            # Start Jekyll and return immediately (don't wait)
            self._start_jekyll_truly_background()
            return True
            
        elif publishing_mode == "remote_only":
            self.reporter.log("Publishing to remote repository...")
            return self._publish_to_git()
            
        elif publishing_mode == "both":
            # Give immediate feedback like local_only
            self.reporter.user_info("Conversion completed")
            self.reporter.user_info("Starting Jekyll server in background...")
            self.reporter.user_info("Server will be available at http://localhost:4000 in 30-60 seconds")
            self.reporter.user_info("Publishing to remote repository...")
            
            # Start Jekyll truly in background (no waiting)
            self._start_jekyll_truly_background()
            
            # Publish to git
            return self._publish_to_git()
            
        else:
            self.reporter.error(f"Unknown publishing mode: {publishing_mode}")
            return False

    def _start_jekyll_truly_background(self):
        """Start Jekyll and return immediately - no waiting"""
        try:
            if self._is_jekyll_running():
                self.reporter.user_info("Jekyll server already running")
                return True
            
            jekyll_root = self.config.get_jekyll_root_folder()
            subprocess.Popen(
                "bundle exec jekyll serve",
                cwd=jekyll_root,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Return immediately - don't wait for startup
            return True
            
        except Exception as e:
            self.reporter.error(f"Failed to start Jekyll: {e}")
            return False

    def _start_jekyll_server_background(self):
        """Start Jekyll server with smart detection and user feedback"""
        try:
            jekyll_root = self.config.get_jekyll_root_folder()
            
            # Phase 1: Smart Detection
            self.reporter.user_info("Checking for existing Jekyll server...")
            
            if self._is_jekyll_running():
                self.reporter.user_info("Jekyll server already running")
                self.reporter.user_info("🌐 Available at: http://localhost:4000")
                self._open_browser()
                return True
            
            # Phase 2: Start with feedback
            self.reporter.user_info("Starting Jekyll server...")
            
            process = subprocess.Popen(
                "bundle exec jekyll serve",
                cwd=jekyll_root,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Phase 3: Monitor startup (10 second timeout)
            import time
            start_time = time.time()
            server_ready = False
            
            while time.time() - start_time < 10:  # 10 second timeout
                if process.poll() is not None:
                    # Process ended unexpectedly
                    self.reporter.error("Jekyll server failed to start")
                    return False
                
                if self._is_jekyll_running():
                    server_ready = True
                    break
                
                time.sleep(0.5)  # Check every 500ms
            
            if server_ready:
                self.reporter.user_info("Jekyll server started successfully")
                self.reporter.user_info("🌐 Available at: http://localhost:4000")
                self._open_browser()
                return True
            else:
                self.reporter.error("Jekyll server startup timed out")
                process.terminate()
                return False
                
        except Exception as e:
            self.reporter.error(f"Failed to start Jekyll server: {e}")
            return False
        



    def _is_jekyll_running(self, port: int = 4000) -> bool:
        """Check if Jekyll server is already running on the specified port"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # 1 second timeout
                result = sock.connect_ex(('localhost', port))
                return result == 0  # 0 means connection successful (port in use)
        except Exception:
            return False
        

    def _open_browser(self):
        """Open browser to Jekyll server (with error handling)"""
        try:
            import webbrowser
            webbrowser.open('http://localhost:4000')
            self.reporter.log("Browser opened to http://localhost:4000")
        except Exception as e:
            self.reporter.log(f"Could not open browser automatically: {e}")
            # Not an error - user can open manually



    def _publish_to_git(self) -> bool:
        """Publish to git repository"""
        try:
            jekyll_root = self.config.get_jekyll_root_folder()
            
            # Add all changes
            self.reporter.log("Adding files to git staging...")
            subprocess.run("git add .", cwd=jekyll_root, shell=True, check=True, 
                        capture_output=True, text=True)
            
            # Check if there's anything to commit
            result = subprocess.run("git diff --cached --quiet", cwd=jekyll_root, shell=True)
            
            if result.returncode == 0:
                # No changes to commit
                self.reporter.user_info("Repository already up to date - no changes to publish")
                self.reporter.log("No changes to commit - files already up to date")
                return True
            
            # Commit changes
            self.reporter.log("Committing changes...")
            commit_result = subprocess.run('git commit -m "Published blog post"', 
                                        cwd=jekyll_root, shell=True, check=True,
                                        capture_output=True, text=True)
            self.reporter.user_info("Changes committed to local repository")
            self.reporter.log(f"Commit output: {commit_result.stdout.strip()}")
            
            # Push to remote
            self.reporter.log("Pushing to remote repository...")
            push_result = subprocess.run("git push", cwd=jekyll_root, shell=True, check=True,
                                    capture_output=True, text=True)
            self.reporter.user_info("Blog post published to GitHub")
            
            # Show git push details only in debug mode
            if push_result.stdout.strip():
                self.reporter.log(f"Push output: {push_result.stdout.strip()}")
            if push_result.stderr.strip():
                self.reporter.log(f"Push details: {push_result.stderr.strip()}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.reporter.error(f"Git publishing failed: {e}")
            return False
        except Exception as e:
            self.reporter.error(f"Unexpected error during git publishing: {e}")
            return False