import pyglet

ball_image = pyglet.image.load('HelloWorld\Resources\Default\grass.png')
window = pyglet.window.Window(width = 400, height = 300, resizable = True, vsync=False)
fpsDisplay = pyglet.window.FPSDisplay(window=window)
batch = pyglet.graphics.Batch()

ball_sprites = []
for i in range(3000):
    x, y = (i%50) * 24, 24*(i//50)
    ball_sprites.append(pyglet.sprite.Sprite(ball_image, x, y, batch=batch))

@window.event
def on_draw():
    window.clear()
    batch.draw()
    fpsDisplay.draw()
    
def update(dt):
    for i in range(3000):
        pos = ball_sprites[i].position
        ball_sprites[i].update(x = pos[0]+1, y = pos[1]+1)    
        
pyglet.clock.schedule_interval(update, 0.01) 
pyglet.app.run()
