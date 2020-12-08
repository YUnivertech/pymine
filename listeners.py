def onTilePlaceEvent( func ):
    def inner():
        status = func()
    return inner()

def onTileBreakEvent( func ):
    def inner():
        status = func()
    return inner()

def onTileAlterEvent( func ):
    def inner():
        status = func()
    return inner()

def windowResizeEvent( func ):
    def inner():
        status = func()
    return inner()

def entitySpawnEvent( func ):
    def inner():
        status = func()
    return inner()

def entityDespawnEvent( func ):
    def inner():
        status = func()
    return inner()

def entityMovementEvent( func ):
    def inner():
        status = func()
    return inner()
