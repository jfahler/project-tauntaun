# DCS Mission Planner - Server Bot Integration

## 🎯 Overview

This DCS Mission Planner has been enhanced with a **gateway page** that allows users to upload their `.miz` files before entering the collaborative mission editor. This makes it perfect for integration with DCS Server Bot environments.

## 🚀 Quick Start

### 1. Start the Server

**Windows:**
```batch
start-server.bat
```

**Linux/Mac:**
```bash
./start-server.sh
```

**Manual:**
```bash
poetry run python tauntaun_live_editor/camp.py
```

### 2. Access the Gateway

Open your browser and navigate to:
```
http://localhost:8080
```

## 📋 User Flow

### Gateway Page (`/`)
1. **Welcome Screen** - Users see a beautiful landing page
2. **File Upload** - Drag & drop or click to upload `.miz` files
3. **Validation** - Server validates the mission file
4. **Redirect** - Users are taken to the main editor

### Editor Page (`/editor`)
1. **Mission Loaded** - The uploaded mission is ready for editing
2. **Collaborative Editing** - Multiple users can edit simultaneously
3. **Real-time Sync** - Changes are broadcast to all connected users
4. **Export** - Save changes back to `.miz` format

## 🔧 DCS Server Bot Integration

### Configuration Options

The server can be configured for different deployment scenarios:

#### 1. **Standalone Mode** (Default)
- Gateway page at root (`/`)
- Editor at `/editor`
- Perfect for direct access

#### 2. **Reverse Proxy Mode**
- Can be placed behind nginx/apache
- Configure proxy to forward requests
- Set appropriate headers for WebSocket support

#### 3. **Docker Deployment**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry install
EXPOSE 8080
CMD ["poetry", "run", "python", "tauntaun_live_editor/camp.py"]
```

### Environment Variables

Create a `.env` file for configuration:
```env
# Server Configuration
HOST=0.0.0.0
PORT=8080

# Admin Password (SHA256 hash)
ADMIN_PASSWORD=03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4

# Mission Directory
MISSION_DIR=/path/to/missions

# Upload Directory
UPLOAD_DIR=/path/to/uploads
```

## 🌐 Network Configuration

### Port Configuration
- **Default Port**: 8080
- **WebSocket**: Same port (upgraded connection)
- **Static Files**: Served from same port

### Firewall Rules
```bash
# Allow incoming connections
sudo ufw allow 8080/tcp

# For production, consider using a reverse proxy
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## 📁 File Structure

```
project-tauntaun/
├── tauntaun_live_editor/
│   ├── data/
│   │   ├── web/
│   │   │   ├── index.html          # Gateway page
│   │   │   ├── editor.html         # Editor page
│   │   │   └── static/             # React app assets
│   │   ├── uploads/                # Uploaded missions
│   │   └── Missions/               # Default missions
│   └── server/
│       └── server.py               # Web server
├── start-server.bat                # Windows startup
├── start-server.sh                 # Linux startup
└── DCS_SERVER_BOT_INTEGRATION.md   # This file
```

## 🔒 Security Considerations

### File Upload Security
- ✅ File extension validation (`.miz` only)
- ✅ Secure filename handling
- ✅ Upload directory isolation
- ✅ File size limits (configurable)

### Access Control
- ✅ Admin password protection
- ✅ Session management
- ✅ WebSocket authentication

### Production Recommendations
- 🔒 Use HTTPS in production
- 🔒 Implement rate limiting
- 🔒 Add file scanning for malware
- 🔒 Regular security updates

## 🐛 Troubleshooting

### Common Issues

#### 1. **Upload Fails**
```
Error: "Upload failed. Please try again."
```
**Solution**: Check file permissions on upload directory

#### 2. **Mission Won't Load**
```
Error: "Failed to load mission"
```
**Solution**: Verify the .miz file is valid and not corrupted

#### 3. **WebSocket Connection Issues**
```
Error: "Network error. Please check your connection."
```
**Solution**: Ensure port 8080 is open and not blocked by firewall

#### 4. **Admin Access Denied**
```
Error: "Invalid admin password"
```
**Solution**: Check the admin password hash in config.json

### Log Files
- **Application Logs**: Check console output
- **Error Logs**: Look for `[ERROR]` entries
- **Debug Logs**: Enable debug mode for detailed logging

## 📊 Monitoring

### Health Check Endpoint
```
GET /health
```
Returns server status and basic metrics.

### Metrics to Monitor
- Active WebSocket connections
- Upload success/failure rates
- Mission load times
- Memory usage
- CPU usage

## 🔄 Updates and Maintenance

### Regular Maintenance
1. **Update Dependencies**: `poetry update`
2. **Clear Uploads**: Remove old uploaded files
3. **Backup Missions**: Backup important mission files
4. **Log Rotation**: Manage log file sizes

### Version Updates
1. Pull latest changes: `git pull`
2. Update dependencies: `poetry install`
3. Restart server
4. Test functionality

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review server logs for error details
- Ensure all dependencies are up to date
- Verify network configuration

## 🎉 Success Stories

This mission planner has been successfully integrated with:
- ✅ DCS Server Bot environments
- ✅ Community mission planning sessions
- ✅ Training mission creation
- ✅ Campaign mission editing

---

**Happy Mission Planning!** 🛩️ 