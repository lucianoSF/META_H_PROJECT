class Users:
    id_ = None
    x = None
    y = None
    height = None
    orientation = None
    ang_azim = None
    
    def __init__(self, id_, x, y, height, orientation, ang_azim):
        self.id_ = id_
        self.x = x
        self.y = y
        self.height = height
        self.orientation = orientation
        self.ang_azim = ang_azim
