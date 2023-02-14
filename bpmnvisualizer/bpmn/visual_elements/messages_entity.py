import bpmnvisualizer.bpmn.visual_elements.vizualizing_entity as ven

class MessagesEntity(ven.VisualisingEntity):
    def __init__(
            self,
            name,
            message_core,
            x,
            y,
            old_names
    ):
        super().__init__(name)
        self.message_core = message_core
        self.x = x
        self.y = y
        self.message_core.add_message({
            'type': 'generate',
            'name': self.name,
            'coords': {
                'x': self.x,
                'y': self.y
            },
            'old_names': old_names
        })

    def move_to(
            self,
            x,
            y
    ):
        self.message_core.add_message({
            'type': 'move',
            'name': self.name,
            'from': {
                'x': int(self.x),
                'y': int(self.y)
            },
            'to': {
                'x': int(x),
                'y': int(y)
            }
        })
        self.x = int(x)
        self.y = int(y)

    def delete(
            self
    ):
        self.message_core.add_message({
            'type': 'delete',
            'name': self.name
        })
