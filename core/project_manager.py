# core/project_manager.py
"""
Project Manager - handles saving and loading project state to/from JSON files.
"""

import json
import os
from datetime import datetime

class ProjectManager:
    """Save and load project data."""

    @staticmethod
    def save_project(filepath, project_data):
        """
        Save project data to a JSON file.

        Args:
            filepath: Path to save the JSON file.
            project_data: Dictionary containing all project data.
        """
        # Add metadata
        project_data['_metadata'] = {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'app': 'Beat & Lyrics Generator'
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        return True

    @staticmethod
    def load_project(filepath):
        """
        Load project data from a JSON file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            Dictionary containing project data.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data