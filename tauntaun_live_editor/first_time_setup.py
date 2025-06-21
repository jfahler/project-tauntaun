"""
First Time Setup Module for Tauntaun Live Editor
Handles initial configuration for DCS paths and other settings.
"""

import os
import sys
import json
import pathlib
import glob
from pathlib import Path
from typing import Optional, Dict, Any


class FirstTimeSetup:
    """Handles first-time setup and configuration."""
    
    def __init__(self):
        self.local_config_path = Path("local-config.json")
        self.setup_complete = self.local_config_path.exists()
    
    def is_first_run(self) -> bool:
        """Check if this is the first run of the application."""
        return not self.setup_complete
    
    def find_dcs_installations(self) -> list:
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
    
    def validate_dcs_path(self, path: str) -> bool:
        """Validate if a path contains a DCS installation."""
        if not os.path.exists(path):
            return False
        
        # Check for common DCS files/directories
        dcs_indicators = [
            "DCS.exe",
            "bin/DCS.exe",
            "CoreMods",
            "Mods",
            "Scripts"
        ]
        
        for indicator in dcs_indicators:
            if os.path.exists(os.path.join(path, indicator)):
                return True
        
        return False
    
    def save_local_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to local config file."""
        with open(self.local_config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to: {self.local_config_path}")
    
    def load_local_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration from local config file."""
        if not self.local_config_path.exists():
            return None
        
        try:
            with open(self.local_config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def run_setup(self) -> Dict[str, Any]:
        """Run the first-time setup process."""
        print("🎯 Welcome to Tauntaun Live Editor!")
        print("=" * 50)
        print("This appears to be your first time running the application.")
        print("Let's configure your DCS installation path.")
        print()
        
        # Find possible DCS installations
        possible_paths = self.find_dcs_installations()
        
        config = {
            "dcs_directory": "",
            "missions_directory": "",
            "setup_complete": True,
            "setup_version": "1.0"
        }
        
        # DCS Directory Setup
        if possible_paths:
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
                        if self.validate_dcs_path(selected_path):
                            config["dcs_directory"] = selected_path
                            print(f"✅ DCS path set to: {selected_path}")
                        else:
                            print("⚠️  Warning: Selected path doesn't appear to be a valid DCS installation.")
                            confirm = input("Continue anyway? (y/N): ").strip().lower()
                            if confirm == 'y':
                                config["dcs_directory"] = selected_path
                        break
                    elif choice_num == len(possible_paths) + 1:
                        while True:
                            manual_path = input("Enter custom DCS path: ").strip()
                            if manual_path and os.path.exists(manual_path):
                                if self.validate_dcs_path(manual_path):
                                    config["dcs_directory"] = manual_path
                                    print(f"✅ DCS path set to: {manual_path}")
                                else:
                                    print("⚠️  Warning: Path doesn't appear to be a valid DCS installation.")
                                    confirm = input("Continue anyway? (y/N): ").strip().lower()
                                    if confirm == 'y':
                                        config["dcs_directory"] = manual_path
                                break
                            else:
                                print("❌ Invalid path or path doesn't exist. Please try again.")
                    elif choice_num == len(possible_paths) + 2:
                        print("⏭️  Skipping DCS path configuration. Using default detection.")
                        break
                    elif choice_num == len(possible_paths) + 3:
                        print("🧪 Development mode selected. No DCS installation required.")
                        config["dcs_directory"] = ""
                        break
                    else:
                        print("❌ Invalid choice. Please try again.")
                except ValueError:
                    print("❌ Please enter a valid number.")
                except KeyboardInterrupt:
                    print("\n\n👋 Setup cancelled.")
                    sys.exit(1)
        else:
            print("❌ No DCS installations found automatically.")
            print("\nPlease enter your DCS installation path manually:")
            print("(Or press Enter for development mode)")
            while True:
                manual_path = input("DCS Path: ").strip()
                if not manual_path:
                    print("🧪 Development mode selected. No DCS installation required.")
                    config["dcs_directory"] = ""
                    break
                elif manual_path and os.path.exists(manual_path):
                    if self.validate_dcs_path(manual_path):
                        config["dcs_directory"] = manual_path
                        print(f"✅ DCS path set to: {manual_path}")
                    else:
                        print("⚠️  Warning: Path doesn't appear to be a valid DCS installation.")
                        confirm = input("Continue anyway? (y/N): ").strip().lower()
                        if confirm == 'y':
                            config["dcs_directory"] = manual_path
                    break
                else:
                    print("❌ Invalid path or path doesn't exist. Please try again.")
        
        # Missions Directory Setup
        print("\n📁 Missions Directory Setup")
        print("Where would you like to store your missions?")
        
        if config["dcs_directory"]:
            default_missions = os.path.join(config["dcs_directory"], "Missions")
            print(f"1. DCS Missions folder: {default_missions}")
        else:
            default_missions = ""
            print("1. DCS Missions folder: (DCS path not set)")
        
        print("2. Local project folder: ./missions")
        print("3. Custom path")
        print("4. Skip (use default)")
        
        while True:
            try:
                choice = input("\nSelect missions directory (1-4): ").strip()
                choice_num = int(choice)
                
                if choice_num == 1:
                    if config["dcs_directory"]:
                        config["missions_directory"] = default_missions
                        print(f"✅ Missions directory set to: {default_missions}")
                    else:
                        print("❌ DCS path not set. Please set DCS path first.")
                        continue
                    break
                elif choice_num == 2:
                    config["missions_directory"] = "./missions"
                    print("✅ Missions directory set to: ./missions")
                    break
                elif choice_num == 3:
                    while True:
                        custom_path = input("Enter custom missions path: ").strip()
                        if custom_path:
                            if os.path.exists(custom_path) or input("Directory doesn't exist. Create it? (y/N): ").strip().lower() == 'y':
                                if not os.path.exists(custom_path):
                                    os.makedirs(custom_path, exist_ok=True)
                                config["missions_directory"] = custom_path
                                print(f"✅ Missions directory set to: {custom_path}")
                                break
                            else:
                                print("❌ Please enter a valid path.")
                        else:
                            print("❌ Please enter a valid path.")
                elif choice_num == 4:
                    print("⏭️  Skipping missions directory configuration. Using default.")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Setup cancelled.")
                sys.exit(1)
        
        # Save configuration
        self.save_local_config(config)
        print("\n🎉 Setup complete! You can now run the application.")
        
        return config
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration."""
        if self.is_first_run():
            return self.run_setup()
        else:
            return self.load_local_config() or {}


def run_first_time_setup_if_needed() -> Dict[str, Any]:
    """Run first-time setup if needed."""
    setup = FirstTimeSetup()
    return setup.get_config()


def get_dcs_directory() -> str:
    """Get the DCS directory from configuration."""
    config = run_first_time_setup_if_needed()
    return config.get("dcs_directory", "")


def get_missions_directory() -> str:
    """Get the missions directory from configuration."""
    config = run_first_time_setup_if_needed()
    return config.get("missions_directory", "")


def detect_dcs_installations():
    """Detect DCS installations and return a list of paths."""
    setup = FirstTimeSetup()
    return setup.find_dcs_installations() 