from classes.Config import Config

class BaseStation:
    id_ = None
    x = None
    y = None
    height = None
    #connected_bs = None
    #c_ijUL = None
    #a_ijUL = None
    #c_ijDL = None
    #a_ijDL = None  
    #l_it = None
    #m_it = None
    #w_it = None
    #Pi = None
    
    def __init__(self, id_, x, y, height):
        self.id_ = id_
        self.x = x
        self.y = y
        self.height = height
        
    