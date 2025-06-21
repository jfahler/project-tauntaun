"""
First Time Setup Module for Tauntaun Live Editor
Handles initial configuration for DCS paths and other settings.
"""

import os
import sys
import json
import pathlib
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
        
        # Check Saved Games (prioritize regular DCS over OpenBeta)
        saved_games = os.path.join(os.environ.get('USERPROFILE', ''), 'Saved Games')
        saved_games_paths = [
            os.path.join(saved_games, "DCS"),  # Regular DCS World (prioritized)
            os.path.join(saved_games, "DCS.openbeta"),  # DCS OpenBeta
            os.path.join(saved_games, "DCS.openbeta_server")  # DCS Server
        ]
        
        for path in saved_games_paths:
            if os.path.exists(path):
                possible_paths.append(path)
        
        # Check common installation directories
        common_paths = [
            "C:\\Program Files\\Eagle Dynamics\\DCS World",
            "C:\\Program Files (x86)\\Eagle Dynamics\\DCS World",
            "C:\\Program Files\\Eagle Dynamics\\DCS World OpenBeta",
            "C:\\Program Files (x86)\\Eagle Dynamics\\DCS World OpenBeta",
            "I:\\DCS World",
            "I:\\DCS World OpenBeta"
        ]
        
        for path in common_paths:
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
            
            while True:
                try:
                    choice = input(f"\nSelect DCS installation (1-{len(possible_paths) + 2}): ").strip()
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
            while True:
                manual_path = input("DCS Path: ").strip()
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
                    if default_missions and os.path.exists(default_missions):
                        config["missions_directory"] = default_missions
                        print(f"✅ Missions directory set to: {default_missions}")
                    else:
                        print("❌ DCS missions folder not found or DCS path not set.")
                        continue
                    break
                elif choice_num == 2:
                    local_missions = "./missions"
                    os.makedirs(local_missions, exist_ok=True)
                    config["missions_directory"] = local_missions
                    print(f"✅ Missions directory set to: {local_missions}")
                    break
                elif choice_num == 3:
                    custom_path = input("Enter custom missions path: ").strip()
                    if custom_path:
                        os.makedirs(custom_path, exist_ok=True)
                        config["missions_directory"] = custom_path
                        print(f"✅ Missions directory set to: {custom_path}")
                    break
                elif choice_num == 4:
                    print("⏭️  Using default missions directory.")
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
        
        print("\n🎉 Setup complete!")
        print("Your configuration has been saved to a local file that won't be shared.")
        print("You can modify these settings later by editing the config file.")
        print("\nStarting Tauntaun Live Editor...")
        print("=" * 50)
        
        return config
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration, running setup if needed."""
        if self.is_first_run():
            return self.run_setup()
        else:
            config = self.load_local_config()
            if config is None:
                print("⚠️  Local config file corrupted. Running setup again...")
                return self.run_setup()
            return config


# Global instance
setup_manager = FirstTimeSetup()


def run_first_time_setup_if_needed() -> Dict[str, Any]:
    """Run first-time setup if needed and return configuration."""
    return setup_manager.get_config()


def get_dcs_directory() -> str:
    """Get the configured DCS directory."""
    config = setup_manager.get_config()
    return config.get("dcs_directory", "")


def get_missions_directory() -> str:
    """Get the configured missions directory."""
    config = setup_manager.get_config()
    return config.get("missions_directory", "")


def detect_dcs_installations():
    """Detect possible DCS installations"""
    installations = []
    
    # Check Saved Games (prioritize regular DCS over OpenBeta)
    saved_games = os.path.join(os.path.expanduser("~"), "Saved Games")
    saved_games_paths = [
        os.path.join(saved_games, "DCS"),  # Regular DCS World (prioritized)
        os.path.join(saved_games, "DCS.openbeta"),  # DCS OpenBeta
        os.path.join(saved_games, "DCS.openbeta_server")  # DCS Server
    ]
    
    for path in saved_games_paths:
        if os.path.exists(path):
            installations.append(path)
    
    # Check common installation directories
    common_paths = [
        "C:\\Program Files\\Eagle Dynamics\\DCS World",
        "C:\\Program Files (x86)\\Eagle Dynamics\\DCS World",
        "C:\\Program Files\\Eagle Dynamics\\DCS World OpenBeta",
        "C:\\Program Files (x86)\\Eagle Dynamics\\DCS World OpenBeta",
        "I:\\DCS World",
        "I:\\DCS World OpenBeta"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            installations.append(path)
    
    return installations 