#!/usr/bin/env python3
"""
DCS Path Setup Script for Tauntaun Live Editor
This script helps you configure the DCS installation path.
"""

import os
import sys
import pathlib
from pathlib import Path

def get_config_path():
    """Get the config file path."""
    home = pathlib.Path.home()
    if sys.platform == "win32":
        datadir = home / "AppData/Roaming"
    elif sys.platform == "linux":
        datadir = home / ".local/share"
    elif sys.platform == "darwin":
        datadir = home / "Library/Application Support"
    else:
        raise Exception(f'Unsupported OS {sys.platform}')
    
    return datadir / "tauntaun-live-editor" / "config.json"

def find_dcs_installations():
    """Find possible DCS installations."""
    possible_paths = []
    
    # Common installation paths
    common_paths = [
        "C:/Program Files/Eagle Dynamics/DCS World",
        "C:/Program Files/Eagle Dynamics/DCS World OpenBeta",
        "D:/Program Files/Eagle Dynamics/DCS World",
        "D:/Program Files/Eagle Dynamics/DCS World OpenBeta",
        "E:/Program Files/Eagle Dynamics/DCS World",
        "E:/Program Files/Eagle Dynamics/DCS World OpenBeta",
        "I:/DCS World OpenBeta",
        "I:/DCS World"
    ]
    
    # Check common paths
    for path in common_paths:
        if os.path.exists(path):
            possible_paths.append(path)
    
    # Check Saved Games
    saved_games = os.path.join(os.environ.get('USERPROFILE', ''), 'Saved Games')
    saved_games_paths = [
        os.path.join(saved_games, "DCS"),
        os.path.join(saved_games, "DCS.openbeta"),
        os.path.join(saved_games, "DCS.openbeta_server")
    ]
    
    for path in saved_games_paths:
        if os.path.exists(path):
            possible_paths.append(path)
    
    return possible_paths

def update_config(dcs_path):
    """Update the config file with the DCS path."""
    config_path = get_config_path()
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read existing config or create default
    if config_path.exists():
        with open(config_path, 'r') as f:
            import json
            config = json.load(f)
    else:
        config = {
            "admin_password": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4",
            "autosave": True,
            "default_coalition": "",
            "default_mission": "",
            "missions_directory": "",
            "port": 8080,
            "dcs_directory": ""
        }
    
    # Update DCS directory
    config["dcs_directory"] = dcs_path
    
    # Write config
    with open(config_path, 'w') as f:
        import json
        json.dump(config, f, indent=2)
    
    print(f"✅ Config updated! DCS path set to: {dcs_path}")
    print(f"📁 Config file location: {config_path}")

def main():
    print("🎯 DCS Path Setup for Tauntaun Live Editor")
    print("=" * 50)
    
    # Find possible DCS installations
    possible_paths = find_dcs_installations()
    
    if not possible_paths:
        print("❌ No DCS installations found automatically.")
        print("\nPlease enter your DCS installation path manually:")
        manual_path = input("DCS Path: ").strip()
        if manual_path and os.path.exists(manual_path):
            update_config(manual_path)
        else:
            print("❌ Invalid path or path doesn't exist.")
        return
    
    print("🔍 Found possible DCS installations:")
    for i, path in enumerate(possible_paths, 1):
        print(f"  {i}. {path}")
    
    print(f"  {len(possible_paths) + 1}. Enter custom path")
    print(f"  {len(possible_paths) + 2}. Skip (use default detection)")
    
    while True:
        try:
            choice = input(f"\nSelect DCS installation (1-{len(possible_paths) + 2}): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(possible_paths):
                selected_path = possible_paths[choice_num - 1]
                update_config(selected_path)
                break
            elif choice_num == len(possible_paths) + 1:
                manual_path = input("Enter custom DCS path: ").strip()
                if manual_path and os.path.exists(manual_path):
                    update_config(manual_path)
                else:
                    print("❌ Invalid path or path doesn't exist.")
                break
            elif choice_num == len(possible_paths) + 2:
                print("⏭️  Skipping DCS path configuration. Using default detection.")
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n👋 Setup cancelled.")
            break

if __name__ == "__main__":
    main() 