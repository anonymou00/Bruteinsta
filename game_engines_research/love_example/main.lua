-- Simple 2D Platformer Example for 256MB VRAM
-- This demonstrates basic LÖVE functionality with minimal VRAM usage

local player = {
    x = 100,
    y = 300,
    width = 32,
    height = 32,
    speed = 200,
    jumpSpeed = -400,
    velocityY = 0,
    onGround = false
}

local platforms = {
    {x = 0, y = 500, width = 800, height = 100},
    {x = 200, y = 400, width = 100, height = 20},
    {x = 400, y = 350, width = 100, height = 20},
    {x = 600, y = 300, width = 100, height = 20}
}

local gravity = 800
local gameState = "playing" -- "playing", "paused", "gameover"

function love.load()
    -- Set window size (smaller for better performance)
    love.window.setMode(800, 600)
    love.window.setTitle("256MB VRAM Game Example")
    
    -- Load minimal assets
    font = love.graphics.newFont(14)
    love.graphics.setFont(font)
end

function love.update(dt)
    if gameState ~= "playing" then return end
    
    -- Handle input
    if love.keyboard.isDown('left') or love.keyboard.isDown('a') then
        player.x = player.x - player.speed * dt
    end
    if love.keyboard.isDown('right') or love.keyboard.isDown('d') then
        player.x = player.x + player.speed * dt
    end
    if love.keyboard.isDown('space') and player.onGround then
        player.velocityY = player.jumpSpeed
        player.onGround = false
    end
    
    -- Apply gravity
    player.velocityY = player.velocityY + gravity * dt
    player.y = player.y + player.velocityY * dt
    
    -- Check collisions with platforms
    player.onGround = false
    for _, platform in ipairs(platforms) do
        if checkCollision(player, platform) then
            if player.velocityY > 0 then
                player.y = platform.y - player.height
                player.velocityY = 0
                player.onGround = true
            end
        end
    end
    
    -- Keep player in bounds
    if player.x < 0 then player.x = 0 end
    if player.x > love.graphics.getWidth() - player.width then 
        player.x = love.graphics.getWidth() - player.width 
    end
    
    -- Check if player fell off
    if player.y > love.graphics.getHeight() then
        gameState = "gameover"
    end
end

function love.draw()
    -- Clear with dark background (easier on GPU)
    love.graphics.setColor(0.1, 0.1, 0.2)
    love.graphics.rectangle('fill', 0, 0, love.graphics.getWidth(), love.graphics.getHeight())
    
    -- Draw platforms
    love.graphics.setColor(0.3, 0.6, 0.3)
    for _, platform in ipairs(platforms) do
        love.graphics.rectangle('fill', platform.x, platform.y, platform.width, platform.height)
    end
    
    -- Draw player
    love.graphics.setColor(1, 1, 1)
    love.graphics.rectangle('fill', player.x, player.y, player.width, player.height)
    
    -- Draw UI
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Use A/D or Arrow Keys to move, Space to jump", 10, 10)
    love.graphics.print("FPS: " .. love.timer.getFPS(), 10, 30)
    love.graphics.print("VRAM-friendly game example", 10, 50)
    
    if gameState == "gameover" then
        love.graphics.setColor(1, 0, 0)
        love.graphics.print("GAME OVER - Press R to restart", 300, 250)
    end
    
    if gameState == "paused" then
        love.graphics.setColor(1, 1, 0)
        love.graphics.print("PAUSED - Press P to resume", 300, 250)
    end
end

function love.keypressed(key)
    if key == 'escape' then
        love.event.quit()
    elseif key == 'r' and gameState == "gameover" then
        resetGame()
    elseif key == 'p' then
        if gameState == "playing" then
            gameState = "paused"
        elseif gameState == "paused" then
            gameState = "playing"
        end
    end
end

function checkCollision(rect1, rect2)
    return rect1.x < rect2.x + rect2.width and
           rect1.x + rect1.width > rect2.x and
           rect1.y < rect2.y + rect2.height and
           rect1.y + rect1.height > rect2.y
end

function resetGame()
    player.x = 100
    player.y = 300
    player.velocityY = 0
    player.onGround = false
    gameState = "playing"
end