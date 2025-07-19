import pytest
import os
import yaml  # ADDED
from daspress import DaspressConverter, DaspressConfig

class TestDaspress:
    def test_full_conversion(self):
        """Test complete conversion using sample_data"""
        
        # Get project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Use your existing sample_data paths
        obsidian_dir = os.path.join(project_root, "sample_data", "obsidian")
        obsidian_img_dir = os.path.join(obsidian_dir, "attachments")
        jekyll_root = os.path.join(project_root, "sample_data", "jekyll")
        
        # Create test config using yaml.dump (ROBUST METHOD)
        test_config = {
            'obsidian': {
                'posts_folder': obsidian_dir,
                'images_folder': obsidian_img_dir
            },
            'jekyll': {
                'root_folder': jekyll_root
            }
        }
        
        # Create test config file
        test_config_path = os.path.join(project_root, "tests", "test-config.yaml")
        with open(test_config_path, 'w') as f:
            yaml.dump(test_config, f, default_flow_style=False, indent=2)
        
        # Test conversion using your existing file
        config = DaspressConfig(config_path=test_config_path)
        converter = DaspressConverter(config=config)
        result = converter.convert("My Blog Post 1.md")
        
        # Verify results
        assert result == True
        
        # Check output file exists
        jekyll_posts_dir = os.path.join(jekyll_root, "_posts")
        output_file = os.path.join(jekyll_posts_dir, "My-Blog-Post-1.md")
        assert os.path.exists(output_file)
        
        # Check content was processed
        with open(output_file, 'r') as f:
            content = f.read()
            assert "![" in content and "/assets/images/" in content  # Jekyll format
            assert "![[" not in content   # No Obsidian format left
        
        # Cleanup test config
        os.remove(test_config_path)