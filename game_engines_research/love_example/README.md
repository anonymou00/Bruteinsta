# LÖVE 2D Platformer Example

A simple 2D platformer game built with LÖVE (Love2D) designed to run efficiently on systems with 256MB VRAM.

## Features

- **Minimal VRAM usage** (~50-80MB)
- **Simple 2D platformer mechanics**
- **Collision detection**
- **Basic physics (gravity, jumping)**
- **Game states (playing, paused, game over)**
- **Performance monitoring (FPS display)**

## Requirements

- **LÖVE 11.x** or later
- **256MB VRAM** (or more)
- **Any modern operating system** (Windows, macOS, Linux)

## Installation

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install love
```

### Linux (Arch)
```bash
sudo pacman -S love
```

### macOS
```bash
brew install love
```

### Windows
Download from https://love2d.org/

## Running the Game

1. **Navigate to the game directory:**
   ```bash
   cd love_example
   ```

2. **Run with LÖVE:**
   ```bash
   love .
   ```

   Or on Windows:
   ```bash
   love.exe .
   ```

## Controls

- **A/D** or **Arrow Keys**: Move left/right
- **Space**: Jump
- **P**: Pause/Resume
- **R**: Restart (when game over)
- **Escape**: Quit

## Game Mechanics

- **Movement**: Smooth left/right movement
- **Jumping**: Jump only when on ground
- **Physics**: Realistic gravity and collision
- **Platforms**: Multiple platforms to jump on
- **Game Over**: Fall off the bottom to lose

## Performance Features

This game is optimized for low VRAM systems:

- **No textures**: Uses simple geometric shapes
- **Minimal assets**: Only loads a small font
- **Efficient rendering**: Simple draw calls
- **Small window**: 800x600 resolution
- **Dark background**: Easier on GPU

## Expected Performance

- **VRAM Usage**: 50-80MB
- **Frame Rate**: 60 FPS on most systems
- **CPU Usage**: Very low
- **Memory**: <100MB total

## Customization

### Adding More Platforms
Edit the `platforms` table in `main.lua`:
```lua
local platforms = {
    {x = 0, y = 500, width = 800, height = 100},
    {x = 200, y = 400, width = 100, height = 20},
    -- Add more platforms here
}
```

### Changing Player Properties
Modify the `player` table:
```lua
local player = {
    x = 100,
    y = 300,
    width = 32,
    height = 32,
    speed = 200,        -- Movement speed
    jumpSpeed = -400,   -- Jump strength
    -- ...
}
```

### Adjusting Physics
Change these values:
```lua
local gravity = 800  -- Gravity strength
```

## Troubleshooting

### Game Won't Start
- Ensure LÖVE is properly installed
- Check that you're in the correct directory
- Verify all files are present

### Low Frame Rate
- Close other applications
- Reduce system graphics settings
- Check if your GPU drivers are updated

### Out of Memory
- Close background applications
- Restart your computer
- Check available system RAM

## Learning Resources

- [LÖVE Documentation](https://love2d.org/wiki/)
- [LÖVE Tutorials](https://love2d.org/wiki/Tutorials)
- [LÖVE Forums](https://love2d.org/forums/)

## Next Steps

After running this example:

1. **Experiment** with the code
2. **Add features** like enemies or collectibles
3. **Learn more** about LÖVE development
4. **Create your own game** using these concepts

## License

This example is provided as-is for educational purposes. Feel free to modify and use in your own projects.