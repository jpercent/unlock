
from model import UnlockModel

class GridStateChange(object):
    XChange = 0
    YChange = 1
    def __init__(self, change, step_value=None):
        super(GridStateChange, self).__init__()
        self.change = change
        self.step_value = step_value
        
        
class GridState(UnlockModel):
    IncrementYCursor=1
    DecrementYCursor=2
    DecrementXCursor=3
    IncrementXCursor=4
    def __init__(self, controllers):
        super(GridState, self).__init__()
        assert len(controllers) > 0
        
        self.ordering = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,-1), (-1,1)]
        self.state = (0,0)
        self.state_change = None
        self.controllers = {}
        
        for slot in self.ordering:
            self.controllers[slot] = 'deadbeef'
        
        index = 0
        for controller in controllers:
            x_offset, y_offset = self.ordering[index]
            self.controllers[(x_offset, y_offset)] = controller
            index += 1
          
    def process_command(self, command):
        if command.decision is not None:
            self.process_decision(command.decision)
            
        if command.selection:
            if self.state in self.controllers:
                controller = self.controllers[self.state]
                controller.activate()
                
    def process_decision(self, decision):
        current_x, current_y = self.state

        if decision == GridState.IncrementYCursor:
            new_state = (current_x, current_y+1)
            change = GridStateChange.YChange, 1
            
        elif decision == GridState.DecrementYCursor:
            new_state = (current_x, current_y-1)
            change = GridStateChange.YChange, -1
            
        elif decision == GridState.DecrementXCursor:
            new_state = (current_x-1, current_y)            
            change = GridStateChange.XChange, -1
            
        elif decision == GridState.IncrementXCursor:
            new_state = (current_x+1, current_y)
            change = GridStateChange.XChange, 1

        #print "decision = ", decision, ' new state = ', new_state, ' controllers ', self.controllers
        #print "state = ", self.state
        if new_state in self.controllers:
            self.state = new_state
            self.state_change = GridStateChange(*change)
                    
    def get_state(self):
        ret = self.state_change
        self.state_change = None
        return ret
        
      