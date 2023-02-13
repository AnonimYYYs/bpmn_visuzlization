import bpmnvisualizer.bpmn.visual_elements.visualizing_flow as vfl

class ConsoleFlow(vfl.VisualizingFlow):
    def __init__(
            self,
            name: str,
            from_block_name: str,
            to_block_name: str,
            args: dict
    ):
        super().__init__(name, from_block_name, to_block_name, args)

    def proceed_entity(
            self,
            entity
    ):
        print(f'flow {self.name} passed {entity.name} from {self.from_block_name} to {self.to_block_name}')
