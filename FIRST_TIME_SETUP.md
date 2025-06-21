# First-Time Setup Guide

## 🎯 Overview

Tauntaun Live Editor now includes a **first-time setup system** that automatically prompts for DCS installation paths and saves them to a secure local configuration file.

## 🔒 Security Features

- **Local Configuration**: Settings are saved to `local-config.json` in the project root
- **Git Ignored**: The config file is automatically excluded from version control
- **User Privacy**: Your DCS paths are never shared or committed to the repository

## 🚀 First Run Experience

When you run the application for the first time, you'll see:

```
🎯 Welcome to Tauntaun Live Editor!
==================================================
This appears to be your first time running the application.
Let's configure your DCS installation path.

🔍 Found possible DCS installations:
  1. I:/DCS World OpenBeta
  2. C:/Users/jfahl/Saved Games/DCS.openbeta
  3. Enter custom path
  4. Skip (use default detection)

Select DCS installation (1-4): 
```

## 📁 Configuration Options

### DCS Installation Path
The setup will automatically detect common DCS installations:
- **Program Files locations**: `C:/Program Files/Eagle Dynamics/DCS World*`
- **Custom drives**: `I:/DCS World OpenBeta`, `D:/DCS World`, etc.
- **Saved Games**: `%USERPROFILE%/Saved Games/DCS*`

### Missions Directory
Choose where to store your missions:
1. **DCS Missions folder**: Uses the missions folder in your DCS installation
2. **Local project folder**: Creates a `./missions` folder in the project
3. **Custom path**: Specify any directory you prefer
4. **Skip**: Use default detection

## 🔧 Manual Configuration

If you need to modify settings later, you can:

### Edit the Config File
```json
{
  "dcs_directory": "I:/DCS World OpenBeta",
  "missions_directory": "./missions",
  "setup_complete": true,
  "setup_version": "1.0"
}
```

### Reset Setup
Delete the `local-config.json` file to trigger setup again:
```bash
rm local-config.json
```

## 🧪 Testing the Setup

Run the test script to verify everything works:
```bash
python test-setup.py
```

## 📋 File Structure

```
project-tauntaun/
├── local-config.json          # Your local settings (gitignored)
├── tauntaun_live_editor/
│   ├── first_time_setup.py    # Setup system
│   ├── util.py                # Updated to use local config
│   └── camp.py                # Main application
├── test-setup.py              # Test script
└── .gitignore                 # Excludes local-config.json
```

## 🎉 Benefits

- **User-Friendly**: Guided setup process
- **Secure**: Local configuration only
- **Flexible**: Multiple DCS installation detection
- **Robust**: Fallback to default detection
- **Maintainable**: Easy to modify and extend

## 🔄 Migration from Old System

If you were using the old configuration system:
1. The new system will automatically detect your existing settings
2. Your old config will be used as a fallback
3. You can gradually migrate to the new local config

## 🛠️ Troubleshooting

### Setup Not Running
- Ensure `local-config.json` doesn't exist
- Check that `first_time_setup.py` is in the correct location

### DCS Not Detected
- Verify your DCS installation path
- Check that the path contains `DCS.exe`, `CoreMods`, or `Mods`
- Use the "Enter custom path" option

### Config File Issues
- Delete `local-config.json` to reset
- Check file permissions
- Verify JSON syntax is valid

---

**Happy Mission Planning!** 🛩️ 