import sqlite3, bz2, os

class Serializer:
    def __init__( self, target ):
        self.name = "Worlds/" + target + '.db'
        if not os.path.isdir("Worlds"): os.mkdir("Worlds")
        self.conn = sqlite3.connect( self.name )
        c = self.conn.cursor()
        try:
            # Create Table
            c.execute( '''CREATE TABLE terrain(keys INTEGER NOT NULL PRIMARY KEY, list TEXT, local TEXT, entity TEXT)''' )
            self.conn.commit()
            c.execute( '''CREATE TABLE player(playername TEXT NOT NULL PRIMARY KEY, pickledplayer TEXT)''' )
            self.conn.commit()
        except Exception as e:
            pass

    def __setitem__( self, key, t ):
        c = self.conn.cursor()
        try:
            # Save string at new key location
            c.execute( '''INSERT INTO terrain (keys, list, local) VALUES (?,?,?)''', ( key, bz2.compress( t[0] ), bz2.compress( t[1] ) ) )
            self.conn.commit()
        except Exception as e:
            # Update string at existing key
            c.execute( 'UPDATE terrain SET list =?, local =?  WHERE keys=?', ( bz2.compress( t[0] ), bz2.compress( t[1] ), key ) )
            self.conn.commit()

    def __getitem__(self, key):
        c = self.conn.cursor()
        c.execute('''SELECT list FROM terrain WHERE keys=?''', (key,))
        li = c.fetchone()
        c.execute('''SELECT local FROM terrain WHERE keys=?''', (key,))
        lo = c.fetchone()
        self.conn.commit()
        try:
            li = bz2.decompress( li[0] )
            lo = bz2.decompress( lo[0] )
            return li, lo
        except Exception as e:
            return None

    def setEntity(self, key, li):
        c = self.conn.cursor()
        # Update string at existing key
        c.execute('UPDATE terrain SET entity =?, WHERE keys=?', (bz2.compress(li), key))
        self.conn.commit()

    def getEntity(self, key):
        c = self.conn.cursor()
        c.execute('''SELECT entity FROM terrain WHERE keys=?''', (key,))
        li = c.fetchone()
        try:
            li = bz2.decompress( li )
            return li
        except Exception as e:
            return None

    def savePlayer( self, name, pickled ):
        c = self.conn.cursor()
        try:
            # Save pickledplayer at new playername
            c.execute( '''INSERT INTO player (playername, pickledplayer) VALUES (?,?)''', ( name, bz2.compress( pickled ) ) )
            self.conn.commit()
        except Exception as e:
            # Update pickledplayer at existing playername
            c.execute( 'UPDATE player SET pickledplayer =?  WHERE playername=?', ( bz2.compress( pickled ), name ) )
            self.conn.commit()

    def loadPlayer( self, name ):
        c = self.conn.cursor()
        c.execute( '''SELECT pickledplayer FROM player WHERE playername=?''', ( name, ) )
        res = c.fetchone()
        self.conn.commit()
        try:
            return bz2.decompress( res[0] )
        except Exception as e:
            return res

    def stop( self ):
        self.conn.close( )
