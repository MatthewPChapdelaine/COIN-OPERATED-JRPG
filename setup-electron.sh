#!/bin/bash

# COIN:OPERATED JRPG - Electron Migration Setup Script
# Converts Python text-based JRPG to Electron desktop app with procedural graphics

set -e

PROJECT_ROOT="$(pwd)"
BACKUP_DIR="$PROJECT_ROOT/.backup_$(date +%s)"

echo "================================================"
echo "COIN:OPERATED JRPG - Electron Migration"
echo "================================================"
echo ""
echo "Project root: $PROJECT_ROOT"
echo "Backup location: $BACKUP_DIR"
echo ""

# Backup existing Python code
echo "📦 Backing up existing Python codebase..."
mkdir -p "$BACKUP_DIR"
if [ -d "$PROJECT_ROOT/src" ]; then
    cp -r "$PROJECT_ROOT/src" "$BACKUP_DIR/src-python"
fi
if [ -f "$PROJECT_ROOT/play.py" ]; then
    cp "$PROJECT_ROOT/play.py" "$BACKUP_DIR/"
fi
echo "✓ Backup complete"
echo ""

# Create new directory structure
echo "📁 Creating new Electron project structure..."
mkdir -p "$PROJECT_ROOT/electron/main"
mkdir -p "$PROJECT_ROOT/electron/renderer"
mkdir -p "$PROJECT_ROOT/electron/renderer/game"
mkdir -p "$PROJECT_ROOT/electron/renderer/assets"
mkdir -p "$PROJECT_ROOT/electron/renderer/assets/sprites"
mkdir -p "$PROJECT_ROOT/electron/renderer/assets/animations"
mkdir -p "$PROJECT_ROOT/python-core"
mkdir -p "$PROJECT_ROOT/dist"

# Move Python code to python-core for reference/conversion
echo "🐍 Organizing Python game engine code..."
if [ -d "$PROJECT_ROOT/src" ]; then
    cp -r "$PROJECT_ROOT/src"/* "$PROJECT_ROOT/python-core/" 2>/dev/null || true
fi
echo ""

# Create Electron main process
echo "⚡ Creating Electron main process..."
cat > "$PROJECT_ROOT/electron/main/index.js" << 'EOF'
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 896,
    icon: path.join(__dirname, '../assets/icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
    }
  });

  const startUrl = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '../../build/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC for game state and save management
ipcMain.handle('save-game', async (event, saveData) => {
  // Save game implementation
  return { success: true };
});

ipcMain.handle('load-game', async (event, saveSlot) => {
  // Load game implementation
  return { success: true };
});
EOF

# Create preload script
echo "🔒 Creating preload script..."
cat > "$PROJECT_ROOT/electron/main/preload.js" << 'EOF'
const { contextBridge, ipcMain } = require('electron');

contextBridge.exposeInMainWorld('api', {
  saveGame: (data) => ipcMain.invoke('save-game', data),
  loadGame: (slot) => ipcMain.invoke('load-game', slot),
  openDevTools: () => ipcMain.invoke('open-devtools'),
});
EOF

# Create React renderer entry point
echo "⚛️  Creating React renderer..."
cat > "$PROJECT_ROOT/electron/renderer/index.js" << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

# Create main App component
echo "📱 Creating main App component..."
cat > "$PROJECT_ROOT/electron/renderer/App.js" << 'EOF'
import React, { useState, useEffect } from 'react';
import GameCanvas from './components/GameCanvas';
import GameUI from './components/GameUI';
import './styles/App.css';

export default function App() {
  const [gameState, setGameState] = useState(null);
  const [gameRunning, setGameRunning] = useState(false);

  useEffect(() => {
    // Initialize game on mount
    setGameState({
      currentScene: 'title',
      player: null,
      inventory: [],
    });
  }, []);

  return (
    <div className="app">
      <GameCanvas gameState={gameState} setGameState={setGameState} />
      <GameUI gameState={gameState} />
    </div>
  );
}
EOF

# Create GameCanvas component for procedural rendering
echo "🎨 Creating procedural graphics component..."
cat > "$PROJECT_ROOT/electron/renderer/components/GameCanvas.js" << 'EOF'
import React, { useEffect, useRef } from 'react';
import ProceduralRenderer from '../game/ProceduralRenderer';

export default function GameCanvas({ gameState, setGameState }) {
  const canvasRef = useRef(null);
  const rendererRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    rendererRef.current = new ProceduralRenderer(canvasRef.current, {
      width: 512,
      height: 448,
      pixelSize: 2,
    });

    // Game loop
    const gameLoop = () => {
      if (rendererRef.current && gameState) {
        rendererRef.current.render(gameState);
      }
      requestAnimationFrame(gameLoop);
    };

    gameLoop();

    return () => {
      if (rendererRef.current) {
        rendererRef.current.destroy();
      }
    };
  }, [gameState]);

  return (
    <canvas
      ref={canvasRef}
      className="game-canvas"
      width={1024}
      height={896}
    />
  );
}
EOF

# Create GameUI component for dialogue and menus
cat > "$PROJECT_ROOT/electron/renderer/components/GameUI.js" << 'EOF'
import React from 'react';

export default function GameUI({ gameState }) {
  return (
    <div className="game-ui">
      <div className="hud">
        <div className="status-panel">
          {/* Character status display */}
        </div>
        <div className="dialogue-panel">
          {/* Dialogue and narrative text */}
        </div>
        <div className="menu-panel">
          {/* Menu options */}
        </div>
      </div>
    </div>
  );
}
EOF

# Create ProceduralRenderer engine
echo "🎮 Creating procedural renderer engine..."
cat > "$PROJECT_ROOT/electron/renderer/game/ProceduralRenderer.js" << 'EOF'
export default class ProceduralRenderer {
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.width = options.width || 512;
    this.height = options.height || 448;
    this.pixelSize = options.pixelSize || 1;
    this.frame = 0;
    this.animationSeed = 0;
  }

  render(gameState) {
    // Clear canvas
    this.ctx.fillStyle = '#000';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Render based on current scene
    if (gameState.currentScene === 'title') {
      this.renderTitle();
    } else if (gameState.currentScene === 'game') {
      this.renderGameplay(gameState);
    }

    this.frame++;
  }

  renderTitle() {
    this.ctx.fillStyle = '#0f0';
    this.ctx.font = 'bold 24px monospace';
    this.ctx.fillText('COIN:OPERATED JRPG', 50, 100);
    this.ctx.font = '16px monospace';
    this.ctx.fillText('Press START to begin', 50, 200);
  }

  renderGameplay(gameState) {
    // Render game world, characters, UI
    this.ctx.fillStyle = '#1a1a1a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Render procedural sprites and world
    if (gameState.player) {
      this.renderCharacter(gameState.player, 256, 224);
    }
  }

  renderCharacter(character, x, y) {
    // Procedural character sprite generation
    const seed = character.id || 0;
    const spriteData = this.generateCharacterSprite(seed, 32, 32);
    this.drawSprite(spriteData, x, y);
  }

  generateCharacterSprite(seed, width, height) {
    // Generate SNES-style pixel art procedurally
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    for (let i = 0; i < width * height; i++) {
      const hash = this.seededRandom(seed + i) * 255;
      ctx.fillStyle = `rgb(${hash}, ${hash * 0.7}, 100)`;
      ctx.fillRect((i % width) * 2, Math.floor(i / width) * 2, 2, 2);
    }

    return canvas;
  }

  drawSprite(sprite, x, y) {
    this.ctx.drawImage(sprite, x, y);
  }

  seededRandom(seed) {
    const x = Math.sin(seed) * 10000;
    return x - Math.floor(x);
  }

  destroy() {
    // Cleanup
  }
}
EOF

# Create styles
echo "🎨 Creating stylesheets..."
mkdir -p "$PROJECT_ROOT/electron/renderer/styles"

cat > "$PROJECT_ROOT/electron/renderer/styles/index.css" << 'EOF'
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #000;
  font-family: 'Arial', sans-serif;
  overflow: hidden;
}

#root {
  width: 100vw;
  height: 100vh;
}
EOF

cat > "$PROJECT_ROOT/electron/renderer/styles/App.css" << 'EOF'
.app {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #000;
}

.game-canvas {
  flex: 1;
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  display: block;
  margin: 0 auto;
}

.game-ui {
  background-color: #1a1a1a;
  color: #0f0;
  font-family: 'Courier New', monospace;
  padding: 10px;
  min-height: 150px;
}

.hud {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
}

.status-panel,
.dialogue-panel,
.menu-panel {
  border: 2px solid #0f0;
  padding: 10px;
  background-color: #000;
  color: #0f0;
}
EOF

# Create package.json template
echo "📦 Creating package.json..."
cat > "$PROJECT_ROOT/package.json" << 'EOF'
{
  "name": "coin-operated-jrpg",
  "version": "2.0.0",
  "description": "COIN:OPERATED JRPG - A narrative-driven JRPG with procedural graphics",
  "main": "electron/main/index.js",
  "homepage": "./",
  "author": "Matthew P. Chapdelaine",
  "license": "MIT",
  "scripts": {
    "react-start": "react-scripts start",
    "react-build": "react-scripts build",
    "electron-start": "electron .",
    "start": "concurrently \"npm run react-start\" \"wait-on http://localhost:3000 && npm run electron-start\"",
    "build": "npm run react-build && electron-builder",
    "build-deb": "electron-builder --linux deb",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "dependencies": {
    "electron-is-dev": "^2.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "concurrently": "^7.0.0",
    "electron": "^latest",
    "electron-builder": "^24.0.0",
    "react-scripts": "5.0.0",
    "wait-on": "^7.0.0"
  },
  "build": {
    "appId": "com.loporian.coinjrpg",
    "productName": "COIN:OPERATED JRPG",
    "files": [
      "build/**/*",
      "electron/**/*",
      "node_modules/**/*"
    ],
    "linux": {
      "target": ["deb"],
      "category": "Game"
    },
    "deb": {
      "depends": [],
      "category": "games"
    }
  },
  "homepage": "./"
}
EOF

# Create HTML template
echo "🌐 Creating HTML template..."
mkdir -p "$PROJECT_ROOT/public"
cat > "$PROJECT_ROOT/public/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>COIN:OPERATED JRPG</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #000;
    }
  </style>
</head>
<body>
  <div id="root"></div>
</body>
</html>
EOF

# Create .gitignore additions
echo "🔒 Updating .gitignore..."
if [ ! -f "$PROJECT_ROOT/.gitignore" ]; then
    touch "$PROJECT_ROOT/.gitignore"
fi

cat >> "$PROJECT_ROOT/.gitignore" << 'EOF'

# Electron
dist/
build/
node_modules/
.cache/

# Development
.env.local
.env.development.local

# Backups
.backup_*
EOF

# Create migration guide
echo "📖 Creating migration guide..."
cat > "$PROJECT_ROOT/MIGRATION_GUIDE.md" << 'EOF'
# Python to Electron Migration Guide

## What Changed

Your Python text-based JRPG has been restructured for Electron:

### Python Code Backup
- Original Python code backed up in `python-core/`
- Reference for converting game logic to JavaScript

### New Structure
```
electron/
├── main/              # Electron main process
├── renderer/          # React renderer
│   ├── components/    # React components
│   ├── game/          # Game engine (JS port)
│   ├── styles/        # CSS styles
│   └── App.js         # Main app component
```

## Next Steps

1. **Port Game Logic to JavaScript**
   - Convert `src/core/` classes to JavaScript/TypeScript
   - Port combat system to JavaScript
   - Convert dialogue/quest system

2. **Integrate Story Content**
   - Export dialogue trees from Python to JSON
   - Create dialogue manager component
   - Port quest system

3. **Procedural Generation**
   - Implement character sprite generation in ProceduralRenderer
   - Add animation system
   - Create world rendering

4. **Install Dependencies**
   ```bash
   npm install
   ```

5. **Run Development**
   ```bash
   npm start
   ```

6. **Build .deb Package**
   ```bash
   npm run build-deb
   ```

## Key Files to Port

- `src/core/character.py` → `electron/renderer/game/Character.js`
- `src/systems/combat.py` → `electron/renderer/game/CombatSystem.js`
- `src/systems/dialogue.py` → `electron/renderer/game/DialogueSystem.js`
- `src/content/` → `electron/renderer/game/content/` (JSON format)

## Notes

- Procedural graphics are rendered via Canvas in `ProceduralRenderer.js`
- Game state managed via React hooks
- Save system uses Electron IPC
- All graphics generated procedurally - no image files needed
EOF

echo ""
echo "================================================"
echo "✓ Migration setup complete!"
echo "================================================"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Review your Python code in python-core/"
echo "2. Update README if needed"
echo "3. Read MIGRATION_GUIDE.md for conversion steps"
echo ""
echo "4. Install Node dependencies:"
echo "   npm install"
echo ""
echo "5. Start development:"
echo "   npm start"
echo ""
echo "6. Build Linux .deb package:"
echo "   npm run build-deb"
echo ""
echo "Your Python code backup is in: $BACKUP_DIR"
echo ""
