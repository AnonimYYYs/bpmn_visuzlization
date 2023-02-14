import bpmnvisualizer.bpmn.visual_elements.visualizing_flow as efl

class MessageFlow(efl.VisualizingFlow):
    def __init__(
            self,
            name: str,
            from_block_name: str,
            to_block_name: str,
            args: dict
    ):
        super().__init__(name, from_block_name, to_block_name, args)
        self.start_coords = args['start_coords']
        self.coords = args['coords']

    def proceed_entity(
            self,
            entity
    ):
        entity.visualizer.move_to(x=self.start_coords['x'], y=self.start_coords['y'])
        for coord in self.coords:
            entity.visualizer.move_to(x=int(coord['x']), y=int(coord['y']))
