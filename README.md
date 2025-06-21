##Tauntaun Live Editor - Community Version (0.4) - A collaborative mission planning tool for DCS World with enhanced features and cross-platform support.

# Community TODO: 

## ✅ Done
- [x] Forked and cloned the original UOAF repo
- [x] Integrated working frontend (`create-react-app`) with backend (`Quart`)
- [x] Built and served frontend (`npm run build`)
- [x] Verified backend works (`camp.py`) and serves frontend on `http://0.0.0.0:8080`
- [x] Committed and pushed to GitHub repo (`main` branch)
- [x] Verified GitHub SSH access and deleted unused `master` branch
- [x] Added cross-platform DCS installation detection (Windows, Linux, macOS)
- [x] Added development mode option for testing without DCS installation

## 🛠️ In Progress / Next Up

### 🔧 Code Hygiene
- [ ] Run `npm i --package-lock-only` on Linux to fix audit error
- [ ] Run `npm audit fix` to patch vulnerable packages
- [ ] Add `.env.example` or `.env.template` with relevant vars if needed
- [ ] Clean up logging noise and outdated Python warnings (e.g. `pkg_resources`)
- [ ] Patch the `tuple index out of range` bug in the PyInstaller flow

## 🧪 Testing & Dev Environment
- [ ] Test mission loading with different `.miz` files in `data/Missions/`
- [ ] Validate UI interactivity (websockets, unit editing, session sync)
- [ ] Confirm frontend build path matches backend static file path
- [ ] Add a dev-friendly startup script (e.g. `start-dev.sh` or `.ps1`)

## 💻 Frontend Refinement Ideas
- [ ] Replace `create-react-app` with Vite for faster dev builds *(optional)*
- [ ] Update design (map UI, colors, logo) to move away from UOAF branding
- [ ] Improve responsiveness / mobile support
- [ ] Add version info / environment tag (dev, prod) to frontend footer

## 📦 Packaging & Deployment
- [ ] Build a working Windows `.exe` with PyInstaller using `camp.spec`
- [ ] Build Linux deployment flow (e.g. `poetry export > requirements.txt`)
- [ ] Consider Docker for cross-platform packaging

## 📁 Repository Clean-Up
- [ ] Add `README.md` section explaining your fork and changes
- [ ] Set up GitHub project board or issues for tracking
- [ ] Confirm branch protection rules (set `main` as default)

## 🧠 Stretch Goals / Ideas
- [ ] Add pilot profiles for persistent data tracking (Loggers integration)
- [ ] Link this to your DCS-Arma Discord bot
- [ ] Add image previews for missions or map overlays in the frontend
- [ ] Add mission template selection or cloning in the UI


## Tauntaun Live Editor

![Screenshot](https://github.com/UOAF/project-tauntaun/raw/v0.1.0/images/screenshot.png)

![Unittests](https://github.com/UOAF/project-tauntaun/workflows/Unittests/badge.svg)

[![Download](https://img.shields.io/github/downloads/UOAF/project-tauntaun/total?label=Download)](https://github.com/UOAF/project-tauntaun/releases)

#### Description
Tauntaun Live Editor is browser based collaborative mission planning tool for DCS events.

#### Installation
#### Windows release
**Use develompent builds** ~~Executable is available under [releases](https://github.com/UOAF/project-tauntaun/releases).~~
    
Develompent builds are available under [actions](https://github.com/UOAF/project-tauntaun/actions/workflows/exe.yml)   
Click the top "Build exe" action and on the bottom of the page there should be a link to the dev build "tauntaun_live_editor_\<long number\>".    
_You need to be logged in to be able to see the download links._    
I recommend checking dev builds if something is missing(e.g. new weapon) or broken after a DCS patch.

#### Configuration
Configuration can be found at
```
Windows: C:/<User>/AppData/Roaming/tauntaun_live_editor/config.json
Linux: ~/.local/share/tauntaun-live-editor/config.json
macOS: ~/Library/Application Support/tauntaun-live-editor/config.json
```
admin_password: password in SHA256 format, default is 1234

#### DCS Installation Detection
The application can automatically detect DCS installations on:
- **Windows**: Common Program Files locations and drive roots (C: through Z:)
- **Linux**: `/opt`, `/usr/local`, Steam installations, and user directories
- **macOS**: `/Applications`, user Applications, and Games directories

For development testing, you can run without a DCS installation by selecting "Development mode" during setup.

#### Run server
```
tauntaun_live_editor.exe
```

#### Join to server
Open https://localhost:8080  
Enter admin mode with right clicking the arrow in the top left corner and enter the admin password. 

#### Wiki / How to use Tauntaun
https://github.com/UOAF/project-tauntaun/wiki

#### Bug reporting and feature requests
Use github issues:
https://github.com/UOAF/project-tauntaun/issues

#### Development
See [Development](doc/Development.md) in the doc directory.

#### License 
GNU Lesser General Public License v3.0

#### Contact
https://github.com/UOAF/project-tauntaun  
https://discord.gg/ZkXCK3y

