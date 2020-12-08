import pyglet

ball_image = pyglet.image.load('HelloWorld\Resources\Default\grass.png')
window = pyglet.window.Window(width = 400, height = 300, resizable = True, vsync=False)
fpsDisplay = pyglet.window.FPSDisplay(window=window)

positions = []
for i in range(3000):
    x, y = (i%50) * 24, 24*(i//50)
    positions.append([x, y])

@window.event
def on_draw():
    window.clear()
    render()
    fpsDisplay.draw()
    
def update(dt):
    for pair in positions:
        pair[0] += 1
        pair[1] += 1

def render():
    for position in positions:
        ball_image.blit(position[0], position[1])
        
pyglet.clock.schedule_interval(update, 0.01) 
pyglet.app.run()
