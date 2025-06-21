#!/usr/bin/env python3
"""
Test script for the first-time setup system.
"""

import os
import sys
from pathlib import Path

# Add the tauntaun_live_editor directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tauntaun_live_editor'))

from tauntaun_live_editor.first_time_setup import FirstTimeSetup

def test_setup():
    """Test the first-time setup system."""
    print("🧪 Testing First-Time Setup System")
    print("=" * 40)
    
    # Create a test instance
    setup = FirstTimeSetup()
    
    # Test if it's first run
    is_first = setup.is_first_run()
    print(f"First run: {is_first}")
    
    # Test DCS installation detection
    print("\n🔍 Testing DCS installation detection...")
    possible_paths = setup.find_dcs_installations()
    print(f"Found {len(possible_paths)} possible DCS installations:")
    for path in possible_paths:
        print(f"  - {path}")
    
    # Test path validation
    print("\n✅ Testing path validation...")
    if possible_paths:
        test_path = possible_paths[0]
        is_valid = setup.validate_dcs_path(test_path)
        print(f"Path '{test_path}' is valid: {is_valid}")
    
    # Test config loading/saving
    print("\n💾 Testing config loading/saving...")
    
    # Use the first detected DCS installation or a generic fallback
    dcs_path = possible_paths[0] if possible_paths else "C:/Program Files/Eagle Dynamics/DCS World"
    test_config = {
        "dcs_directory": dcs_path,
        "missions_directory": "./missions",
        "setup_complete": True,
        "setup_version": "1.0"
    }
    
    setup.save_local_config(test_config)
    loaded_config = setup.load_local_config()
    
    if loaded_config:
        print("✅ Config saved and loaded successfully")
        print(f"  DCS Directory: {loaded_config.get('dcs_directory', 'Not set')}")
        print(f"  Missions Directory: {loaded_config.get('missions_directory', 'Not set')}")
    else:
        print("❌ Config loading failed")
    
    print("\n🎉 Setup system test complete!")

if __name__ == "__main__":
    test_setup() 