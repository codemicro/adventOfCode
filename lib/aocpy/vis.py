import os.path

class SaveManager():
    def __init__(self, d):
        self.dir = d
        self.current_n = 0

    def save(self, im):
        im.save(os.path.join(self.dir, f"frame_{str(self.current_n).zfill(4)}.png"))
        self.current_n += 1
    
    