#serializer
import sqlite3,  bz2

#noiseModules
## Built-In Modules
from enum import Enum
import math
from sortedcontainers import SortedDict, SortedList
from functools import lru_cache
## Pip-Installed Modules
# import numpy as np

class Serializer:

    def __init__( self, target ):
        self.name  =  "Worlds/" + target + '.db'
        self.conn  =  sqlite3.connect( self.name )
        c = self.conn.cursor()
        try:
            ## Create Table
            c.execute( '''CREATE TABLE terrain(keys INTEGER NOT NULL PRIMARY KEY, list TEXT, local TEXT, entity TEXT)''' )
            self.conn.commit()
            c.execute( '''CREATE TABLE player(playername TEXT NOT NULL PRIMARY KEY, pickledplayer TEXT)''' )
            self.conn.commit()

        except Exception as e:
            # print(e)
            pass

    ## Save method
    def __setitem__( self, key, t ):

        """
            Saves/Updates the string at a particular key location.
            Requires the key as an int and chunkObj as UTF-8 string.
        """

        c = self.conn.cursor()
        try:
            ## Save string at new key location
            c.execute( '''INSERT INTO terrain (keys, list, local) VALUES (?,?,?)''', ( key, bz2.compress( t[0] ), bz2.compress( t[1] ) ) )
            self.conn.commit()

        except Exception as e:
            # print(e)
            ## Update string at existing key
            c.execute( 'UPDATE terrain SET list =?, local =?  WHERE keys=?', ( bz2.compress( t[0] ), bz2.compress( t[1] ), key ) )
            self.conn.commit()

    ## Load method
    def __getitem__(self, key):
        """
            Retrieves the string stored at a particular key location.
            Requires the key as an int.
            Returns the string at the key's location (if key is present) or None
        """
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
            # print(e)
            return None

    def setEntity(self, key, li):
        c = self.conn.cursor()
        ## Update string at existing key
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
            # print(e)
            return None

    def savePlayer( self, name, pickled ):

        """
            Saves/Updates the pickledplayer at a particular playername.
            Requires the name as a string and pickled as UTF-8 string.
        """
        c = self.conn.cursor()
        try:
            ## Save pickledplayer at new playername
            c.execute( '''INSERT INTO player (playername, pickledplayer) VALUES (?,?)''', ( name, bz2.compress( pickled ) ) )
            self.conn.commit()

        except Exception as e:
            # print(e)
            ## Update pickledplayer at existing playername
            c.execute( 'UPDATE player SET pickledplayer =?  WHERE playername=?', ( bz2.compress( pickled ), name ) )
            self.conn.commit()

    def loadPlayer( self, name ):

        """
            Retrieves the pickledplayer stored at a particular playername.
            Requires the name as a string.
            Returns the pickledplayer at the playername's location (if present) or None
        """
        c = self.conn.cursor()
        c.execute( '''SELECT pickledplayer FROM player WHERE playername=?''', ( name, ) )
        res = c.fetchone()
        self.conn.commit()

        try:
            return bz2.decompress( res[0] )
        except Exception as e:
            # print(e)
            return res

    def stop( self ):
        self.conn.close( )

vector = [
    -0.763874, -0.596439, -0.246489, 0.0, 0.396055, 0.904518, -0.158073, 0.0,
    -0.499004, -0.8665, -0.0131631, 0.0, 0.468724, -0.824756, 0.316346, 0.0,
    0.829598, 0.43195, 0.353816, 0.0, -0.454473, 0.629497, -0.630228, 0.0,
    -0.162349, -0.869962, -0.465628, 0.0, 0.932805, 0.253451, 0.256198, 0.0,
    -0.345419, 0.927299, -0.144227, 0.0,    -0.715026, -0.293698, -0.634413, 0.0,
    -0.245997, 0.717467, -0.651711, 0.0,    -0.967409, -0.250435, -0.037451, 0.0,
    0.901729, 0.397108, -0.170852, 0.0,    0.892657, -0.0720622, -0.444938, 0.0,
    0.0260084, -0.0361701, 0.999007, 0.0,    0.949107, -0.19486, 0.247439, 0.0,
    0.471803, -0.807064, -0.355036, 0.0,    0.879737, 0.141845, 0.453809, 0.0,
    0.570747, 0.696415, 0.435033, 0.0,    -0.141751, -0.988233, -0.0574584, 0.0,
    -0.58219, -0.0303005, 0.812488, 0.0,    -0.60922, 0.239482, -0.755975, 0.0,
    0.299394, -0.197066, -0.933557, 0.0,    -0.851615, -0.220702, -0.47544, 0.0,
    0.848886, 0.341829, -0.403169, 0.0,    -0.156129, -0.687241, 0.709453, 0.0,
    -0.665651, 0.626724, 0.405124, 0.0,    0.595914, -0.674582, 0.43569, 0.0,
    0.171025, -0.509292, 0.843428, 0.0,    0.78605, 0.536414, -0.307222, 0.0,
    0.18905, -0.791613, 0.581042, 0.0,    -0.294916, 0.844994, 0.446105, 0.0,
    0.342031, -0.58736, -0.7335, 0.0,    0.57155, 0.7869, 0.232635, 0.0,
    0.885026, -0.408223, 0.223791, 0.0,    -0.789518, 0.571645, 0.223347, 0.0,
    0.774571, 0.31566, 0.548087, 0.0,    -0.79695, -0.0433603, -0.602487, 0.0,
    -0.142425, -0.473249, -0.869339, 0.0,    -0.0698838, 0.170442, 0.982886, 0.0,
    0.687815, -0.484748, 0.540306, 0.0,    0.543703, -0.534446, -0.647112, 0.0,
    0.97186, 0.184391, -0.146588, 0.0,    0.707084, 0.485713, -0.513921, 0.0,
    0.942302, 0.331945, 0.043348, 0.0,    0.499084, 0.599922, 0.625307, 0.0,
    -0.289203, 0.211107, 0.9337, 0.0,    0.412433, -0.71667, -0.56239, 0.0,
    0.87721, -0.082816, 0.47291, 0.0,    -0.420685, -0.214278, 0.881538, 0.0,
    0.752558, -0.0391579, 0.657361, 0.0,    0.0765725, -0.996789, 0.0234082, 0.0,
    -0.544312, -0.309435, -0.779727, 0.0,    -0.455358, -0.415572, 0.787368, 0.0,
    -0.874586, 0.483746, 0.0330131, 0.0,    0.245172, -0.0838623, 0.965846, 0.0,
    0.382293, -0.432813, 0.81641, 0.0,    -0.287735, -0.905514, 0.311853, 0.0,
    -0.667704, 0.704955, -0.239186, 0.0,    0.717885, -0.464002, -0.518983, 0.0,
    0.976342, -0.214895, 0.0240053, 0.0,    -0.0733096, -0.921136, 0.382276, 0.0,
    -0.986284, 0.151224, -0.0661379, 0.0,    -0.899319, -0.429671, 0.0812908, 0.0,
    0.652102, -0.724625, 0.222893, 0.0,    0.203761, 0.458023, -0.865272, 0.0,
    -0.030396, 0.698724, -0.714745, 0.0,    -0.460232, 0.839138, 0.289887, 0.0,
    -0.0898602, 0.837894, 0.538386, 0.0,    -0.731595, 0.0793784, 0.677102, 0.0,
    -0.447236, -0.788397, 0.422386, 0.0,    0.186481, 0.645855, -0.740335, 0.0,
    -0.259006, 0.935463, 0.240467, 0.0,    0.445839, 0.819655, -0.359712, 0.0,
    0.349962, 0.755022, -0.554499, 0.0,    -0.997078, -0.0359577, 0.0673977, 0.0,
    -0.431163, -0.147516, -0.890133, 0.0,    0.299648, -0.63914, 0.708316, 0.0,
    0.397043, 0.566526, -0.722084, 0.0,    -0.502489, 0.438308, -0.745246, 0.0,
    0.0687235, 0.354097, 0.93268, 0.0,    -0.0476651, -0.462597, 0.885286, 0.0,
    -0.221934, 0.900739, -0.373383, 0.0,    -0.956107, -0.225676, 0.186893, 0.0,
    -0.187627, 0.391487, -0.900852, 0.0,    -0.224209, -0.315405, 0.92209, 0.0,
    -0.730807, -0.537068, 0.421283, 0.0,    -0.0353135, -0.816748, 0.575913, 0.0,
    -0.941391, 0.176991, -0.287153, 0.0,    -0.154174, 0.390458, 0.90762, 0.0,
    -0.283847, 0.533842, 0.796519, 0.0,    -0.482737, -0.850448, 0.209052, 0.0,
    -0.649175, 0.477748, 0.591886, 0.0,    0.885373, -0.405387, -0.227543, 0.0,
    -0.147261, 0.181623, -0.972279, 0.0,    0.0959236, -0.115847, -0.988624, 0.0,
    -0.89724, -0.191348, 0.397928, 0.0,    0.903553, -0.428461, -0.00350461, 0.0,
    0.849072, -0.295807, -0.437693, 0.0,    0.65551, 0.741754, -0.141804, 0.0,
    0.61598, -0.178669, 0.767232, 0.0,    0.0112967, 0.932256, -0.361623, 0.0,
    -0.793031, 0.258012, 0.551845, 0.0,    0.421933, 0.454311, 0.784585, 0.0,
    -0.319993, 0.0401618, -0.946568, 0.0,    -0.81571, 0.551307, -0.175151, 0.0,
    -0.377644, 0.00322313, 0.925945, 0.0,    0.129759, -0.666581, -0.734052, 0.0,
    0.601901, -0.654237, -0.457919, 0.0,    -0.927463, -0.0343576, -0.372334, 0.0,
    -0.438663, -0.868301, -0.231578, 0.0,    -0.648845, -0.749138, -0.133387, 0.0,
    0.507393, -0.588294, 0.629653, 0.0,    0.726958, 0.623665, 0.287358, 0.0,
    0.411159, 0.367614, -0.834151, 0.0,    0.806333, 0.585117, -0.0864016, 0.0,
    0.263935, -0.880876, 0.392932, 0.0,    0.421546, -0.201336, 0.884174, 0.0,
    -0.683198, -0.569557, -0.456996, 0.0,    -0.117116, -0.0406654, -0.992285, 0.0,
    -0.643679, -0.109196, -0.757465, 0.0,    -0.561559, -0.62989, 0.536554, 0.0,
    0.0628422, 0.104677, -0.992519, 0.0,    0.480759, -0.2867, -0.828658, 0.0,
    -0.228559, -0.228965, -0.946222, 0.0,    -0.10194, -0.65706, -0.746914, 0.0,
    0.0689193, -0.678236, 0.731605, 0.0,    0.401019, -0.754026, 0.52022, 0.0,
    -0.742141, 0.547083, -0.387203, 0.0,    -0.00210603, -0.796417, -0.604745, 0.0,
    0.296725, -0.409909, -0.862513, 0.0,    -0.260932, -0.798201, 0.542945, 0.0,
    -0.641628, 0.742379, 0.192838, 0.0,    -0.186009, -0.101514, 0.97729, 0.0,
    0.106711, -0.962067, 0.251079, 0.0,    -0.743499, 0.30988, -0.592607, 0.0,
    -0.795853, -0.605066, -0.0226607, 0.0,    -0.828661, -0.419471, -0.370628, 0.0,
    0.0847218, -0.489815, -0.8677, 0.0,    -0.381405, 0.788019, -0.483276, 0.0,
    0.282042, -0.953394, 0.107205, 0.0,    0.530774, 0.847413, 0.0130696, 0.0,
    0.0515397, 0.922524, 0.382484, 0.0,    -0.631467, -0.709046, 0.313852, 0.0,
    0.688248, 0.517273, 0.508668, 0.0,    0.646689, -0.333782, -0.685845, 0.0,
    -0.932528, -0.247532, -0.262906, 0.0,    0.630609, 0.68757, -0.359973, 0.0,
    0.577805, -0.394189, 0.714673, 0.0,    -0.887833, -0.437301, -0.14325, 0.0,
    0.690982, 0.174003, 0.701617, 0.0,    -0.866701, 0.0118182, 0.498689, 0.0,
    -0.482876, 0.727143, 0.487949, 0.0,    -0.577567, 0.682593, -0.447752, 0.0,
    0.373768, 0.0982991, 0.922299, 0.0,    0.170744, 0.964243, -0.202687, 0.0,
    0.993654, -0.035791, -0.106632, 0.0,    0.587065, 0.4143, -0.695493, 0.0,
    -0.396509, 0.26509, -0.878924, 0.0,    -0.0866853, 0.83553, -0.542563, 0.0,
    0.923193, 0.133398, -0.360443, 0.0,    0.00379108, -0.258618, 0.965972, 0.0,
    0.239144, 0.245154, -0.939526, 0.0,    0.758731, -0.555871, 0.33961, 0.0,
    0.295355, 0.309513, 0.903862, 0.0,    0.0531222, -0.91003, -0.411124, 0.0,
    0.270452, 0.0229439, -0.96246, 0.0,    0.563634, 0.0324352, 0.825387, 0.0,
    0.156326, 0.147392, 0.976646, 0.0,    -0.0410141, 0.981824, 0.185309, 0.0,
    -0.385562, -0.576343, -0.720535, 0.0,    0.388281, 0.904441, 0.176702, 0.0,
    0.945561, -0.192859, -0.262146, 0.0,    0.844504, 0.520193, 0.127325, 0.0,
    0.0330893, 0.999121, -0.0257505, 0.0,    -0.592616, -0.482475, -0.644999, 0.0,
    0.539471, 0.631024, -0.557476, 0.0,    0.655851, -0.027319, -0.754396, 0.0,
    0.274465, 0.887659, 0.369772, 0.0,    -0.123419, 0.975177, -0.183842, 0.0,
    -0.223429, 0.708045, 0.66989, 0.0,    -0.908654, 0.196302, 0.368528, 0.0,
    -0.95759, -0.00863708, 0.288005, 0.0,    0.960535, 0.030592, 0.276472, 0.0,
    -0.413146, 0.907537, 0.0754161, 0.0,    -0.847992, 0.350849, -0.397259, 0.0,
    0.614736, 0.395841, 0.68221, 0.0,    -0.503504, -0.666128, -0.550234, 0.0,
    -0.268833, -0.738524, -0.618314, 0.0,    0.792737, -0.60001, -0.107502, 0.0,
    -0.637582, 0.508144, -0.579032, 0.0,    0.750105, 0.282165, -0.598101, 0.0,
    -0.351199, -0.392294, -0.850155, 0.0,    0.250126, -0.960993, -0.118025, 0.0,
    -0.732341, 0.680909, -0.0063274, 0.0,    -0.760674, -0.141009, 0.633634, 0.0,
    0.222823, -0.304012, 0.926243, 0.0,    0.209178, 0.505671, 0.836984, 0.0,
    0.757914, -0.56629, -0.323857, 0.0,    -0.782926, -0.339196, 0.52151, 0.0,
    -0.462952, 0.585565, 0.665424, 0.0,    0.61879, 0.194119, -0.761194, 0.0,
    0.741388, -0.276743, 0.611357, 0.0,    0.707571, 0.702621, 0.0752872, 0.0,
    0.156562, 0.819977, 0.550569, 0.0,    -0.793606, 0.440216, 0.42, 0.0,
    0.234547, 0.885309, -0.401517, 0.0,    0.132598, 0.80115, -0.58359, 0.0,
    -0.377899, -0.639179, 0.669808, 0.0,    -0.865993, -0.396465, 0.304748, 0.0,
    -0.624815, -0.44283, 0.643046, 0.0,    -0.485705, 0.825614, -0.287146, 0.0,
    -0.971788, 0.175535, 0.157529, 0.0,    -0.456027, 0.392629, 0.798675, 0.0,
    -0.0104443, 0.521623, -0.853112, 0.0,    -0.660575, -0.74519, 0.091282, 0.0,
    -0.0157698, -0.307475, -0.951425, 0.0,    -0.603467, -0.250192, 0.757121, 0.0,
    0.506876, 0.25006, 0.824952, 0.0,    0.255404, 0.966794, 0.00884498, 0.0,
    0.466764, -0.874228, -0.133625, 0.0,    0.475077, -0.0682351, -0.877295, 0.0,
    -0.224967, -0.938972, -0.260233, 0.0,    -0.377929, -0.814757, -0.439705, 0.0,
    -0.305847, 0.542333, -0.782517, 0.0,    0.26658, -0.902905, -0.337191, 0.0,
    0.0275773, 0.322158, -0.946284, 0.0,    0.0185422, 0.716349, 0.697496, 0.0,
    -0.20483, 0.978416, 0.0273371, 0.0,    -0.898276, 0.373969, 0.230752, 0.0,
    -0.00909378, 0.546594, 0.837349, 0.0,    0.6602, -0.751089, 0.000959236, 0.0,
    0.855301, -0.303056, 0.420259, 0.0,    0.797138, 0.0623013, -0.600574, 0.0,
    0.48947, -0.866813, 0.0951509, 0.0,    0.251142, 0.674531, 0.694216, 0.0,
    -0.578422, -0.737373, -0.348867, 0.0,    -0.254689, -0.514807, 0.818601, 0.0,
    0.374972, 0.761612, 0.528529, 0.0,    0.640303, -0.734271, -0.225517, 0.0,
    -0.638076, 0.285527, 0.715075, 0.0,    0.772956, -0.15984, -0.613995, 0.0,
    0.798217, -0.590628, 0.118356, 0.0,    -0.986276, -0.0578337, -0.154644, 0.0,
    -0.312988, -0.94549, 0.0899272, 0.0,    -0.497338, 0.178325, 0.849032, 0.0,
    -0.101136, -0.981014, 0.165477, 0.0,    -0.521688, 0.0553434, -0.851339, 0.0,
    -0.786182, -0.583814, 0.202678, 0.0,    -0.565191, 0.821858, -0.0714658, 0.0,
    0.437895, 0.152598, -0.885981, 0.0,    -0.92394, 0.353436, -0.14635, 0.0,
    0.212189, -0.815162, -0.538969, 0.0,    -0.859262, 0.143405, -0.491024, 0.0,
    0.991353, 0.112814, 0.0670273, 0.0,    0.0337884, -0.979891, -0.196654, 0.0
]

X_NOISE_GEN = 1619
Y_NOISE_GEN = 31337
Z_NOISE_GEN = 6971
SEED_NOISE_GEN = 1013
SHIFT_NOISE_GEN = 8

def cubic_interp(n0, n1, n2, n3, a):
    p = (n3 - n2) - (n0 - n1)
    q = (n0 - n1) - p
    r = n2 - n0
    s = n1

    return (p*a**3) + (q*a**2) + (r*a) + s

def linear_interp(n0, n1, a):
    return ((1 - a) * n0) + (a * n1)

def scurve3(a):
    return (a * a * (3-2*a))

def scurve5(a):
    return (6 * a**5) - (15 * a**4) + (10 * a**3)

def gradient_coherent_noise_3d(x, y, z, seed, quality):
    if x > 0:
        x0 = int(x)
    else:
        x0 = int(x) - 1

    if y > 0:
        y0 = int(y)
    else:
        y0 = int(y) - 1

    if z > 0:
        z0 = int(z)
    else:
        z0 = int(z) - 1

    x1 = x0 + 1
    y1 = y0 + 1
    z1 = z0 + 1

    xs = 0
    ys = 0
    zs = 0

    if quality == Quality.fast:
        xs = (x - x0)
        ys = (y - y0)
        zs = (z - z0)
    elif quality == Quality.std:
        xs = scurve3(x-x0)
        ys = scurve3(y-y0)
        zs = scurve3(z-z0)
    else:
        xs = scurve5(x-x0)
        ys = scurve5(y-y0)
        zs = scurve5(z-z0)

    n0 = gradient_noise_3d(x, y, z, x0, y0, z0, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y0, z0, seed)
    ix0 = linear_interp(n0, n1, xs)

    n0 = gradient_noise_3d(x, y, z, x0, y1, z0, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y1, z0, seed)
    ix1 = linear_interp(n0, n1, xs)
    iy0 = linear_interp(ix0, ix1, ys)

    n0 = gradient_noise_3d(x, y, z, x0, y0, z1, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y0, z1, seed)
    ix0 = linear_interp(n0, n1, xs)

    n0 = gradient_noise_3d(x, y, z, x0, y1, z1, seed)
    n1 = gradient_noise_3d(x, y, z, x1, y1, z1, seed)
    ix1 = linear_interp(n0, n1, xs)
    iy1 = linear_interp(ix0, ix1, ys)

    return linear_interp(iy0, iy1, zs)

def gradient_noise_3d(fx, fy, fz, ix, iy, iz, seed):
    vectorIndex = (
    X_NOISE_GEN * ix +
    Y_NOISE_GEN * iy +
    Z_NOISE_GEN * iz +
    SEED_NOISE_GEN * seed
    )

    vectorIndex &= 0xffffffff
    vectorIndex = vectorIndex ^ (vectorIndex >> SHIFT_NOISE_GEN)
    vectorIndex &= 0xff

    xv = vector[vectorIndex << 2]
    yv = vector[(vectorIndex << 2) + 1]
    zv = vector[(vectorIndex << 2) + 2]

    xvp = (fx - ix)
    yvp = (fy - iy)
    zvp = (fz - iz)

    return ((xv * xvp) + (yv * yvp) + (zv * zvp)*2.12)

def int_value_noise_3d(x, y, z, seed):
    n = (
        X_NOISE_GEN * x +
        Y_NOISE_GEN * y +
        Z_NOISE_GEN * z +
        SEED_NOISE_GEN * seed
    ) & 0x7fffffff

    n = (n >> 13) ^ n

    return (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff

def value_noise_3d(x, y, z, seed):
    return 1 - (int_value_noise_3d(x, y, z, seed) / 1073741824)


class Quality(Enum):
    fast = 1
    std = 2
    best = 3


## Different Noise Generators
class Perlin():
    """ The classic noise. https://en.wikipedia.org/wiki/Perlin_noise """
    def __init__(self, frequency=1, lacunarity=2, octaves=6, persistence=0.5, seed=0, quality=Quality.std):
        self.frequency = frequency
        self.lacunarity = lacunarity
        self.octaves = octaves
        self.seed = seed
        self.persistence = persistence
        self.quality = quality

    @lru_cache(maxsize=32)
    def __getitem__(self, pos):
        x,y,z = pos
        value = 0.0
        signal = 0.0
        curPersistence = 1.0

        x *= self.frequency
        y *= self.frequency
        z *= self.frequency

        for i in range(self.octaves):
            seed = (self.seed + i) & 0xffffffff
            signal = gradient_coherent_noise_3d(x, y, z, seed, self.quality)
            value += signal * curPersistence

            x *= self.lacunarity
            y *= self.lacunarity
            z *= self.lacunarity
            curPersistence *= self.persistence

        return value


class RidgedMulti():
    """ This is much like perlin noise, however each octave is modified by
    abs(x*-exponent) where x is x *= frequency repeated over each octave. """
    def __init__(self, frequency=1, lacunarity=2, quality=Quality.std,
        octaves=6, seed=0, exponent=1, offset=1, gain=2):
        self.frequency = frequency
        self.lacunarity = lacunarity
        self.quality = quality
        self.octaves = octaves
        self.seed = seed
        self.exponent = exponent
        self.max_octaves = 30
        self.weights = [0] * self.max_octaves
        self.offset = offset
        self.gain = gain

        freq = 1
        for i in range(0, self.max_octaves):
            self.weights[i] = freq**-exponent
            freq *= self.lacunarity

    @lru_cache(maxsize=32)
    def __getitem__(self, pos):
        x,y,z = pos
        x *= self.frequency
        y *= self.frequency
        z *= self.frequency

        signal = 0.0
        value = 0.0
        weight = 1.0

        for i in range(self.octaves):
            seed = (self.seed + i) & 0x7fffffff
            signal = gradient_coherent_noise_3d(x, y, z, seed, self.quality)

            signal = abs(signal)
            signal = self.offset - signal

            signal *= signal

            signal *= weight

            weight = signal * self.gain

            if weight > 1:
                weight = 1
            if weight < 0:
                weight = 0

            value += (signal * self.weights[i])

            x *= self.lacunarity
            y *= self.lacunarity
            z *= self.lacunarity

        return (value * 1.25) - 1


# class OpenSimplex():
#     """ Generates OpenSimplex noise. """
#     def __init__(self, seed=0, frequency=1, persistence=0.5, lacunarity=2, octaves=6):
#         self.stretch_constant = -1/6
#         self.squish_constant = 1/3
#         self.prng = np.random.RandomState(seed)
#         self.perm = self.prng.permutation(256)
#         self.perm = np.tile(self.perm, 2)
#         self.frequency = frequency
#         self.persistence = persistence
#         self.lacunarity = lacunarity
#         self.octaves = octaves

#     def next_perm(self):
#         self.perm = self.prng.permutation(256)
#         self.perm = np.tile(self.perm, 2)

#     def grad(self, hash, x, y, z):
#         h = hash & 15

#         if h < 8:
#             u = x
#         else:
#             u = y

#         if h < 4:
#             v = y
#         else:
#             if h == 12 or h == 14:
#                 v = x
#             else:
#                 v = z

#         if h & 1 == 0:
#             r1 = -u
#         else:
#             r1 = u

#         if h & 2 == 0:
#             r2 = -v
#         else:
#             r2 = v

#         return r1 + r2

#     def __getitem__(self, pos):
#         x,y,z = pos
#         F3 = 1/3
#         G3 = 1/6

#         x *= self.frequency
#         y *= self.frequency
#         z *= self.frequency
#         value = 0
#         cur_persistence = 1

#         for i in range(self.octaves):
#             #self.next_perm()
#             s = (x+y+z)*F3

#             xs = x + s
#             ys = y + s
#             zs = z + s

#             if xs == 0:
#                 xs = -1
#             if ys == 0:
#                 ys = -1
#             if zs == 0:
#                 zs = -1

#             i = math.floor(xs)
#             j = math.floor(ys)
#             k = math.floor(zs)

#             t = (i+j+k)*G3
#             X0 = i - t
#             Y0 = j - t
#             Z0 = k - t
#             x0 = x - X0
#             y0 = y - Y0
#             z0 = z - Z0

#             if x0 >= y0:
#                 if y0 >= z0:
#                     i1 = 1; j1 = 0; k1 = 0; i2 = 1; j2 = 1; k2 = 0;
#                 elif x0 >= z0:
#                     i1 = 1; j1 = 0; k1 = 0; i2 = 1; j2 = 0; k2 = 1;
#                 else:
#                     i1 = 0; j1 = 0; k1 = 1; i2 = 1; j2 = 0; k2 = 1;
#             else:
#                 if y0 < z0:
#                     i1 = 0; j1 = 0; k1 = 1; i2 = 0; j2 = 1; k2 = 1;
#                 elif x0 < z0:
#                     i1 = 0; j1 = 1; k1 = 0; i2 = 0; j2 = 1; k2 = 1;
#                 else:
#                     i1 = 0; j1 = 1; k1 = 0; i2 = 1; j2 = 1; k2 = 0;

#             x1 = x0 - i1 + G3
#             y1 = y0 - j1 + G3
#             z1 = z0 - k1 + G3

#             x2 = x0 - i2 + 2*G3
#             y2 = y0 - j2 + 2*G3
#             z2 = z0 - k2 + 2*G3

#             x3 = x0 - 1 + 3*G3
#             y3 = y0 - 1 + 3*G3
#             z3 = z0 - 1 + 3*G3

#             ii = i & 0xff
#             jj = j & 0xff
#             kk = k & 0xff

#             t0 = 0.6 - x0 * x0 - y0 * y0 - z0 * z0

#             if t0 < 0:
#                 n0 = 0
#             else:
#                 t0 *= t0
#                 n0 = t0 * t0 * self.grad(self.perm[ii + self.perm[jj + self.perm[kk]]], x0, y0, z0);

#             t1 = 0.6 - x1 * x1 - y1 * y1 - z1 * z1
#             if t1 < 0:
#                 n1 = 0
#             else:
#                 t1 *= t1
#                 n1 = t1 * t1 * self.grad(self.perm[ii + i1 + self.perm[jj + j1 +  self.perm[kk + k1]]], x1, y1, z1);

#             t2 = 0.6 - x2 * x2 - y2 * y2 - z2 * z2
#             if t2 < 0:
#                 n2 = 0
#             else:
#                 t2 *= t2
#                 n2 = t2 * t2 * self.grad(self.perm[ii + i2 + self.perm[jj + j2 + self.perm[kk + k2]]], x2, y2, z2);

#             t3 = 0.6 - x3 * x3 - y3 * y3 - z3 * z3
#             if t3 < 0:
#                 n3 = 0
#             else:
#                 t3 *= t3
#                 n3 = t3 * t3 * self.grad(self.perm[ii + 1 + self.perm[jj + 1 + self.perm[kk+1]]], x3, y3, z3);

#             signal = 32 * (n0 + n1 + n2 + n3)
#             value += signal * cur_persistence
#             x *= self.lacunarity
#             y *= self.lacunarity
#             z *= self.lacunarity
#             cur_persistence *= self.persistence

#         return value


class Turbulence():
    """
    Noise module that randomly displaces the input value before
    returning the output value from a source module.

    The __getitem__() method randomly displaces the (x, y, z)
    coordinates of the input value before retrieving the output value from
    the source0.  To control the turbulence, an application can
    modify its frequency, its power, and its roughness.

    The frequency of the turbulence determines how rapidly the
    displacement amount changes.  To specify the frequency, set the frequency
    parameter.

    The power of the turbulence determines the scaling factor that is
    applied to the displacement amount.  To specify the power, set the power
    parameter.

    The roughness of the turbulence determines the roughness of the
    changes to the displacement amount.  Low values smoothly change the
    displacement amount.  High values roughly change the displacement
    amount, which produces more "kinky" changes.  To specify the
    roughness, set the roughness parameter.

    Use of this noise module may require some trial and error.  Assuming
    that you are using a generator module as the source module, you
    should first:
     - Set the frequency to the same frequency as the source module.
     - Set the power to the reciprocal of the frequency.

    From these initial frequency and power values, modify these values
    until this noise module produce the desired changes in your terrain or
    texture.  For example:
    - Low frequency (1/8 initial frequency) and low power (1/8 initial
      power) produces very minor, almost unnoticeable changes.
    - Low frequency (1/8 initial frequency) and high power (8 times
      initial power) produces "ropey" lava-like terrain or marble-like
      textures.
    - High frequency (8 times initial frequency) and low power (1/8
      initial power) produces a noisy version of the initial terrain or
      texture.
    - High frequency (8 times initial frequency) and high power (8 times
      initial power) produces nearly pure noise, which isn't entirely
      useful.

    Displacing the input values result in more realistic terrain and
    textures.  If you are generating elevations for terrain height maps,
    you can use this noise module to produce more realistic mountain
    ranges or terrain features that look like flowing lava rock.  If you
    are generating values for textures, you can use this noise module to
    produce realistic marble-like or "oily" textures.

    Internally, there are three Perlin noise modules
    that displace the input value; one for the x, one for the y,
    and one for the z coordinate.

    This noise module requires one source module.
    """
    def __init__(self, source0, frequency=1, power=1, roughness=3, seed=0):
        self.frequency = frequency
        self.power = power
        self.roughness = roughness
        self.seed = seed
        self.xdm = Perlin(frequency=frequency, octaves=roughness, seed=seed)
        self.ydm = Perlin(frequency=frequency, octaves=roughness, seed=seed)
        self.zdm = Perlin(frequency=frequency, octaves=roughness, seed=seed)

        self.source0 = source0

    @lru_cache(maxsize=32)
    def __getitem__(self, pos):
        x,y,z = pos
        x0 = x + (12414.0 / 65536.0)
        y0 = y + (65124.0 / 65536.0)
        z0 = z + (31337.0 / 65536.0)
        x1 = x + (26519.0 / 65536.0)
        y1 = y + (18128.0 / 65536.0)
        z1 = z + (60493.0 / 65536.0)
        x2 = x + (53820.0 / 65536.0)
        y2 = y + (11213.0 / 65536.0)
        z2 = z + (44845.0 / 65536.0)

        xDistort = x + (self.xdm[x0, y0, z0] * self.power)
        yDistort = y + (self.ydm[x1, y1, z1] * self.power)
        zDistort = z + (self.zdm[x2, y2, z2] * self.power)

        return self.source0[xDistort, yDistort, zDistort]


class Voronoi():
    """
    Noise module that outputs Voronoi cells.

    In mathematics, a **Voronoi cell** is a region containing all the
    points that are closer to a specific **seed point** than to any
    other seed point.  These cells mesh with one another, producing
    polygon-like formations.

    By default, this noise module randomly places a seed point within
    each unit cube.  By modifying the **frequency** of the seed points,
    an application can change the distance between seed points.  The
    higher the frequency, the closer together this noise module places
    the seed points, which reduces the size of the cells.  To specify the
    frequency of the cells, set the frequency parameter.

    This noise module assigns each Voronoi cell with a random constant
    value from a coherent-noise function.  The **displacement value**
    controls the range of random values to assign to each cell.  The
    range of random values is +/- the displacement value.  To specify the
    displacement value, set the displacement parameter.

    To modify the random positions of the seed points, set the seed parameter
    to something different.

    This noise module can optionally add the distance from the nearest
    seed to the output value.  To enable this feature, set enable_distance
    to True. This causes the points in the Voronoi cells
    to increase in value the further away that point is from the nearest
    seed point.

    Voronoi cells are often used to generate cracked-mud terrain
    formations or crystal-like textures

    This noise module requires no source modules.
    """
    def __init__(self, displacement=1, enable_distance=False, frequency=1, seed=0):
        self.displacement = displacement
        self.enable_distance = enable_distance
        self.frequency = frequency
        self.seed = seed

    @lru_cache(maxsize=32)
    def __getitem__(self, pos):
        x,y,z = pos
        x *= self.frequency
        y *= self.frequency
        z *= self.frequency

        xInt = int(x) if (x > 0) else int(x) -1
        yInt = int(y) if (y > 0) else int(y) -1
        zInt = int(z) if (z > 0) else int(z) -1

        minDist = 2147483647.0
        xCan = 0
        yCan = 0
        zCan = 0

        for zCur in range(zInt-2, zInt+2):
            for yCur in range(yInt-2, yInt+2):
                for xCur in range(xInt-2, xInt+2):
                    xPos = xCur + value_noise_3d(xCur, yCur, zCur, self.seed)
                    yPos = yCur + value_noise_3d(xCur, yCur, zCur, self.seed+1)
                    zPos = zCur + value_noise_3d(xCur, yCur, zCur, self.seed+2)

                    xDist = xPos - x
                    yDist = yPos - y
                    zDist = zPos - z
                    dist = xDist * xDist + yDist * yDist + zDist * zDist

                    if dist < minDist:
                        minDist = dist
                        xCan = xPos
                        yCan = yPos
                        zCan = zPos
        value = 0

        if self.enable_distance:
            xDist = xCan - x
            yDist = yCan - y
            zDist = zCan - z

            value = (math.sqrt(xDist * xDist + yDist * yDist + zDist * zDist)) *\
                math.sqrt(3) - 1

        return value + (self.displacement * value_noise_3d(math.floor(xCan),
                                                math.floor(yCan),
                                                math.floor(zCan), 0))


## Test
# perl = Perlin()
# p = perl[1.4,30.5,3.3]
# print(p)
# simp = OpenSimplex()
# s = simp[1,3,30]
# print(s)
# multi = RidgedMulti()
# m = multi[15,45,754]
# print(m)
# vor = Voronoi()
# v = vor[1,30,5]
# print(v)