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
    
    # Common installation paths by platform
    if sys.platform == "win32":
        # Windows paths
        common_paths = [
            "C:/Program Files/Eagle Dynamics/DCS World",
            "C:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "D:/Program Files/Eagle Dynamics/DCS World",
            "D:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "E:/Program Files/Eagle Dynamics/DCS World",
            "E:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "F:/Program Files/Eagle Dynamics/DCS World",
            "F:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "G:/Program Files/Eagle Dynamics/DCS World",
            "G:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "H:/Program Files/Eagle Dynamics/DCS World",
            "H:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "I:/Program Files/Eagle Dynamics/DCS World",
            "I:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "J:/Program Files/Eagle Dynamics/DCS World",
            "J:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "K:/Program Files/Eagle Dynamics/DCS World",
            "K:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "L:/Program Files/Eagle Dynamics/DCS World",
            "L:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "M:/Program Files/Eagle Dynamics/DCS World",
            "M:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "N:/Program Files/Eagle Dynamics/DCS World",
            "N:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "O:/Program Files/Eagle Dynamics/DCS World",
            "O:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "P:/Program Files/Eagle Dynamics/DCS World",
            "P:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "Q:/Program Files/Eagle Dynamics/DCS World",
            "Q:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "R:/Program Files/Eagle Dynamics/DCS World",
            "R:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "S:/Program Files/Eagle Dynamics/DCS World",
            "S:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "T:/Program Files/Eagle Dynamics/DCS World",
            "T:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "U:/Program Files/Eagle Dynamics/DCS World",
            "U:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "V:/Program Files/Eagle Dynamics/DCS World",
            "V:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "W:/Program Files/Eagle Dynamics/DCS World",
            "W:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "X:/Program Files/Eagle Dynamics/DCS World",
            "X:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "Y:/Program Files/Eagle Dynamics/DCS World",
            "Y:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            "Z:/Program Files/Eagle Dynamics/DCS World",
            "Z:/Program Files/Eagle Dynamics/DCS World OpenBeta",
            # Also check root of drives
            "C:/DCS World",
            "C:/DCS World OpenBeta",
            "D:/DCS World",
            "D:/DCS World OpenBeta",
            "E:/DCS World",
            "E:/DCS World OpenBeta",
            "F:/DCS World",
            "F:/DCS World OpenBeta",
            "G:/DCS World",
            "G:/DCS World OpenBeta",
            "H:/DCS World",
            "H:/DCS World OpenBeta",
            "I:/DCS World",
            "I:/DCS World OpenBeta",
            "J:/DCS World",
            "J:/DCS World OpenBeta",
            "K:/DCS World",
            "K:/DCS World OpenBeta",
            "L:/DCS World",
            "L:/DCS World OpenBeta",
            "M:/DCS World",
            "M:/DCS World OpenBeta",
            "N:/DCS World",
            "N:/DCS World OpenBeta",
            "O:/DCS World",
            "O:/DCS World OpenBeta",
            "P:/DCS World",
            "P:/DCS World OpenBeta",
            "Q:/DCS World",
            "Q:/DCS World OpenBeta",
            "R:/DCS World",
            "R:/DCS World OpenBeta",
            "S:/DCS World",
            "S:/DCS World OpenBeta",
            "T:/DCS World",
            "T:/DCS World OpenBeta",
            "U:/DCS World",
            "U:/DCS World OpenBeta",
            "V:/DCS World",
            "V:/DCS World OpenBeta",
            "W:/DCS World",
            "W:/DCS World OpenBeta",
            "X:/DCS World",
            "X:/DCS World OpenBeta",
            "Y:/DCS World",
            "Y:/DCS World OpenBeta",
            "Z:/DCS World",
            "Z:/DCS World OpenBeta"
        ]
    elif sys.platform == "linux":
        # Linux paths
        common_paths = [
            "/opt/DCS World",
            "/opt/DCS World OpenBeta",
            "/usr/local/DCS World",
            "/usr/local/DCS World OpenBeta",
            "/home/*/DCS World",
            "/home/*/DCS World OpenBeta",
            "/home/*/Games/DCS World",
            "/home/*/Games/DCS World OpenBeta",
            "/home/*/.steam/steam/steamapps/common/DCSWorld",
            "/home/*/.steam/steam/steamapps/common/DCSWorldOpenBeta"
        ]
    elif sys.platform == "darwin":
        # macOS paths
        common_paths = [
            "/Applications/DCS World.app",
            "/Applications/DCS World OpenBeta.app",
            "/Users/*/Applications/DCS World.app",
            "/Users/*/Applications/DCS World OpenBeta.app",
            "/Users/*/Games/DCS World.app",
            "/Users/*/Games/DCS World OpenBeta.app"
        ]
    else:
        common_paths = []
    
    # Check common paths
    for path in common_paths:
        if "*" in path:
            # Handle wildcard paths
            import glob
            expanded_paths = glob.glob(path)
            for expanded_path in expanded_paths:
                if os.path.exists(expanded_path):
                    possible_paths.append(expanded_path)
        else:
            if os.path.exists(path):
                possible_paths.append(path)
    
    # Check Saved Games (Windows) or equivalent directories
    if sys.platform == "win32":
        saved_games = os.path.join(os.environ.get('USERPROFILE', ''), 'Saved Games')
        saved_games_paths = [
            os.path.join(saved_games, "DCS"),
            os.path.join(saved_games, "DCS.openbeta"),
            os.path.join(saved_games, "DCS.openbeta_server")
        ]
    elif sys.platform == "linux":
        home = os.path.expanduser("~")
        saved_games_paths = [
            os.path.join(home, ".config/DCS"),
            os.path.join(home, ".config/DCS.openbeta"),
            os.path.join(home, ".local/share/DCS"),
            os.path.join(home, ".local/share/DCS.openbeta")
        ]
    elif sys.platform == "darwin":
        home = os.path.expanduser("~")
        saved_games_paths = [
            os.path.join(home, "Library/Application Support/DCS"),
            os.path.join(home, "Library/Application Support/DCS.openbeta"),
            os.path.join(home, "Documents/DCS"),
            os.path.join(home, "Documents/DCS.openbeta")
        ]
    else:
        saved_games_paths = []
    
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
    print(f"  {len(possible_paths) + 3}. Development mode (no DCS installation required)")
    
    while True:
        try:
            choice = input(f"\nSelect DCS installation (1-{len(possible_paths) + 3}): ").strip()
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
            elif choice_num == len(possible_paths) + 3:
                print("🧪 Development mode selected. No DCS installation required.")
                update_config("")
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