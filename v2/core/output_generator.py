"""
Output generator for coordinating the generation of different resume formats.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..utils import FileUtils, VersionManager
from ..generators import MarkdownGenerator, WordGenerator, WebsiteGenerator

class OutputGenerator:
    """Coordinates the generation of multiple output formats for resumes."""
    
    def __init__(self, base_output_dir: str = "profiles"):
        """
        Initialize output generator.
        
        Args:
            base_output_dir: Base directory for all profile outputs
        """
        self.base_output_dir = Path(base_output_dir)
        self.logger = logging.getLogger(__name__)
        
        # Initialize utilities and generators
        self.file_utils = FileUtils()
        self.version_manager = VersionManager()
        self.markdown_generator = MarkdownGenerator()
        self.word_generator = WordGenerator()
        self.website_generator = WebsiteGenerator()
        
    def generate_complete_profile(self, profile_data: Dict[str, Any], 
                                profile_name: str, style_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Generate complete profile with all output formats.
        
        Args:
            profile_data: Profile content and metadata
            profile_name: Name for the profile
            style_analysis: Style analysis from AI processor (optional)
            
        Returns:
            Dictionary mapping format names to output file paths
        """
        try:
            # Generate version and create output directory
            version = self.version_manager.generate_version()
            output_dir = self._create_profile_directory(profile_name, version)
            
            # Store metadata
            metadata = {
                'profile_name': profile_name,
                'version': version,
                'created_at': datetime.now().isoformat(),
                'style_analysis': style_analysis or {},
                'source_documents': profile_data.get('source_documents', [])
            }
            
            output_paths = {}
            
            # Generate markdown file (base format)
            md_path = self.markdown_generator.generate(
                profile_data, output_dir, profile_name, version
            )
            output_paths['markdown'] = str(md_path)
            
            # Generate Word document
            word_path = self.word_generator.generate(
                profile_data, output_dir, profile_name, version, style_analysis
            )
            output_paths['word'] = str(word_path)
            
            # Generate website/HTML
            website_path = self.website_generator.generate(
                profile_data, output_dir, profile_name, version, style_analysis
            )
            output_paths['website'] = str(website_path)
            
            # Save metadata
            metadata_path = output_dir / "metadata.json"
            self.file_utils.save_json(metadata, metadata_path)
            output_paths['metadata'] = str(metadata_path)
            
            self.logger.info(f"Generated complete profile for {profile_name} v{version}")
            return output_paths
            
        except Exception as e:
            self.logger.error(f"Error generating profile: {str(e)}")
            raise Exception(f"Failed to generate complete profile: {str(e)}")
    
    def update_existing_profile(self, old_profile_path: str, updated_content: str, 
                              new_style_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Update an existing profile with new content.
        
        Args:
            old_profile_path: Path to existing markdown profile
            updated_content: New profile content
            new_style_analysis: Updated style analysis (optional)
            
        Returns:
            Dictionary mapping format names to new output file paths
        """
        try:
            # Parse old profile information
            old_path = Path(old_profile_path)
            profile_name, old_version = self._parse_profile_filename(old_path.name)
            
            # Create new version
            new_version = self.version_manager.generate_version()
            output_dir = self._create_profile_directory(profile_name, new_version)
            
            # Prepare profile data
            profile_data = {
                'content': updated_content,
                'profile_name': profile_name,
                'previous_version': old_version,
                'updated_at': datetime.now().isoformat()
            }
            
            # Generate all formats with new content
            return self.generate_complete_profile(
                profile_data, profile_name, new_style_analysis
            )
            
        except Exception as e:
            self.logger.error(f"Error updating profile: {str(e)}")
            raise Exception(f"Failed to update profile: {str(e)}")
    
    def list_profiles(self) -> List[Dict[str, Any]]:
        """
        List all available profiles with their versions.
        
        Returns:
            List of profile information dictionaries
        """
        profiles = []
        
        if not self.base_output_dir.exists():
            return profiles
            
        try:
            for profile_dir in self.base_output_dir.iterdir():
                if profile_dir.is_dir():
                    profile_info = self._get_profile_info(profile_dir)
                    if profile_info:
                        profiles.append(profile_info)
                        
            return sorted(profiles, key=lambda x: x.get('last_updated', ''))
            
        except Exception as e:
            self.logger.error(f"Error listing profiles: {str(e)}")
            return []
    
    def get_profile_versions(self, profile_name: str) -> List[str]:
        """
        Get all versions for a specific profile.
        
        Args:
            profile_name: Name of the profile
            
        Returns:
            List of version strings, sorted by creation time
        """
        profile_dir = self.base_output_dir / profile_name
        
        if not profile_dir.exists():
            return []
            
        versions = []
        for version_dir in profile_dir.iterdir():
            if version_dir.is_dir():
                versions.append(version_dir.name)
                
        return sorted(versions)
    
    def cleanup_old_versions(self, profile_name: str, keep_versions: int = 5) -> List[str]:
        """
        Clean up old versions of a profile, keeping only the most recent ones.
        
        Args:
            profile_name: Name of the profile
            keep_versions: Number of versions to keep
            
        Returns:
            List of removed version directories
        """
        versions = self.get_profile_versions(profile_name)
        
        if len(versions) <= keep_versions:
            return []
            
        # Remove oldest versions
        versions_to_remove = versions[:-keep_versions]
        removed = []
        
        for version in versions_to_remove:
            version_path = self.base_output_dir / profile_name / version
            try:
                self.file_utils.remove_directory(version_path)
                removed.append(version)
                self.logger.info(f"Removed old version: {profile_name}/{version}")
            except Exception as e:
                self.logger.error(f"Failed to remove {version}: {str(e)}")
                
        return removed
    
    def _create_profile_directory(self, profile_name: str, version: str) -> Path:
        """Create directory structure for profile output."""
        output_dir = self.base_output_dir / profile_name / version
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def _parse_profile_filename(self, filename: str) -> tuple:
        """Parse profile filename to extract name and version."""
        # Expected format: {name}.{version}.md
        parts = filename.replace('.md', '').split('.')
        if len(parts) >= 2:
            name = parts[0]
            version = '.'.join(parts[1:])
            return name, version
        else:
            return parts[0], 'unknown'
    
    def _get_profile_info(self, profile_dir: Path) -> Optional[Dict[str, Any]]:
        """Get information about a profile from its directory."""
        try:
            versions = [d.name for d in profile_dir.iterdir() if d.is_dir()]
            if not versions:
                return None
                
            latest_version = sorted(versions)[-1]
            latest_dir = profile_dir / latest_version
            
            # Try to load metadata
            metadata_path = latest_dir / "metadata.json"
            metadata = {}
            if metadata_path.exists():
                metadata = self.file_utils.load_json(metadata_path)
            
            return {
                'name': profile_dir.name,
                'latest_version': latest_version,
                'total_versions': len(versions),
                'last_updated': metadata.get('created_at', 'unknown'),
                'output_dir': str(latest_dir),
                'metadata': metadata
            }
            
        except Exception as e:
            self.logger.error(f"Error getting profile info for {profile_dir}: {str(e)}")
            return None 