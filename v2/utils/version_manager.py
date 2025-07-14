"""
Version management for resume profiles.
"""

import logging
from datetime import datetime
from typing import List, Optional, Tuple
import re

class VersionManager:
    """Manages versioning for resume profiles."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_version(self, timestamp: Optional[datetime] = None) -> str:
        """
        Generate a new version string based on timestamp.
        
        Args:
            timestamp: Optional timestamp (defaults to now)
            
        Returns:
            Version string in format v{YYYYMMDDHHMM}
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        version = f"v{timestamp.strftime('%Y%m%d%H%M')}"
        self.logger.info(f"Generated version: {version}")
        return version
    
    def parse_version(self, version_string: str) -> Optional[datetime]:
        """
        Parse version string to extract timestamp.
        
        Args:
            version_string: Version string (e.g., "v202401011200")
            
        Returns:
            Datetime object if parsing successful, None otherwise
        """
        try:
            # Remove 'v' prefix if present
            version_clean = version_string.lstrip('v')
            
            # Parse timestamp (format: YYYYMMDDHHMM)
            if len(version_clean) == 12 and version_clean.isdigit():
                timestamp = datetime.strptime(version_clean, '%Y%m%d%H%M')
                return timestamp
            else:
                self.logger.warning(f"Invalid version format: {version_string}")
                return None
                
        except ValueError as e:
            self.logger.error(f"Error parsing version {version_string}: {str(e)}")
            return None
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """
        Compare two version strings.
        
        Args:
            version1: First version string
            version2: Second version string
            
        Returns:
            -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        timestamp1 = self.parse_version(version1)
        timestamp2 = self.parse_version(version2)
        
        if timestamp1 is None or timestamp2 is None:
            # Fallback to string comparison
            if version1 < version2:
                return -1
            elif version1 > version2:
                return 1
            else:
                return 0
        
        if timestamp1 < timestamp2:
            return -1
        elif timestamp1 > timestamp2:
            return 1
        else:
            return 0
    
    def sort_versions(self, versions: List[str], reverse: bool = False) -> List[str]:
        """
        Sort list of version strings.
        
        Args:
            versions: List of version strings
            reverse: If True, sort in descending order
            
        Returns:
            Sorted list of version strings
        """
        try:
            # Parse timestamps for sorting
            version_pairs = []
            for version in versions:
                timestamp = self.parse_version(version)
                if timestamp:
                    version_pairs.append((timestamp, version))
                else:
                    # Fallback for unparseable versions
                    version_pairs.append((datetime.min, version))
            
            # Sort by timestamp
            version_pairs.sort(key=lambda x: x[0], reverse=reverse)
            
            return [version for _, version in version_pairs]
            
        except Exception as e:
            self.logger.error(f"Error sorting versions: {str(e)}")
            # Fallback to string sorting
            return sorted(versions, reverse=reverse)
    
    def get_latest_version(self, versions: List[str]) -> Optional[str]:
        """
        Get the latest version from a list.
        
        Args:
            versions: List of version strings
            
        Returns:
            Latest version string, or None if list is empty
        """
        if not versions:
            return None
            
        sorted_versions = self.sort_versions(versions, reverse=True)
        return sorted_versions[0]
    
    def is_valid_version(self, version_string: str) -> bool:
        """
        Check if version string is valid.
        
        Args:
            version_string: Version string to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self.parse_version(version_string) is not None
    
    def get_version_info(self, version_string: str) -> dict:
        """
        Get detailed information about a version.
        
        Args:
            version_string: Version string
            
        Returns:
            Dictionary with version information
        """
        timestamp = self.parse_version(version_string)
        
        if timestamp:
            return {
                'version': version_string,
                'timestamp': timestamp.isoformat(),
                'date': timestamp.strftime('%Y-%m-%d'),
                'time': timestamp.strftime('%H:%M'),
                'year': timestamp.year,
                'month': timestamp.month,
                'day': timestamp.day,
                'hour': timestamp.hour,
                'minute': timestamp.minute,
                'is_valid': True
            }
        else:
            return {
                'version': version_string,
                'timestamp': None,
                'date': None,
                'time': None,
                'year': None,
                'month': None,
                'day': None,
                'hour': None,
                'minute': None,
                'is_valid': False
            }
    
    def generate_next_version(self, current_versions: List[str]) -> str:
        """
        Generate next version ensuring it's newer than all existing versions.
        
        Args:
            current_versions: List of existing version strings
            
        Returns:
            New version string
        """
        if not current_versions:
            return self.generate_version()
            
        # Get latest existing version
        latest_version = self.get_latest_version(current_versions)
        if not latest_version:
            return self.generate_version()
            
        latest_timestamp = self.parse_version(latest_version)
        current_time = datetime.now()
        
        # Ensure new version is at least 1 minute newer
        if latest_timestamp and current_time <= latest_timestamp:
            new_timestamp = latest_timestamp.replace(minute=latest_timestamp.minute + 1)
            return self.generate_version(new_timestamp)
        else:
            return self.generate_version(current_time)
    
    def cleanup_versions(self, versions: List[str], keep_count: int = 5) -> Tuple[List[str], List[str]]:
        """
        Determine which versions to keep and which to remove.
        
        Args:
            versions: List of all version strings
            keep_count: Number of versions to keep
            
        Returns:
            Tuple of (versions_to_keep, versions_to_remove)
        """
        if len(versions) <= keep_count:
            return versions, []
            
        sorted_versions = self.sort_versions(versions, reverse=True)
        versions_to_keep = sorted_versions[:keep_count]
        versions_to_remove = sorted_versions[keep_count:]
        
        self.logger.info(f"Cleanup: keeping {len(versions_to_keep)}, removing {len(versions_to_remove)}")
        
        return versions_to_keep, versions_to_remove
    
    def get_timestamp(self, format_string: str = "%Y-%m-%d %H:%M") -> str:
        """
        Get current timestamp as formatted string.
        
        Args:
            format_string: Format for the timestamp (default: "%Y-%m-%d %H:%M")
            
        Returns:
            Formatted timestamp string
        """
        return datetime.now().strftime(format_string) 