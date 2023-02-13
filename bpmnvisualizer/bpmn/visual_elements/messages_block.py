import bpmnvisualizer.bpmn.visual_elements.visualizing_block as vb
import bpmnvisualizer.bpmn.bpmn_elements.entity as ent
import bpmnvisualizer.bpmn.visual_elements.messages_entity as men

class MessagingBlock(vb.VisualizingBlock):
    def __init__(
            self,
            name: str,
            label: str,
            args: dict
    ):
        super().__init__(name, label, args)
        self.visualizer = args['message_core']
        self.x_left = int(args['coords']['@x'])
        self.x_right = int(args['coords']['@x']) + int(args['coords']['@width'])
        self.y_top = int(args['coords']['@y'])
        self.y_bottom = int(args['coords']['@y']) + int(args['coords']['@height'])

    def on_entity_work(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        pass

    def on_entity_enter(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        entity.visualizer.move_to(
            y=int((self.y_bottom+self.y_top)/2),
            x=self.x_left
        )

    def on_entity_proceed(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        entity.visualizer.move_to(
            y=int((self.y_bottom+self.y_top)/2),
            x=int((self.x_right+self.x_left)/2)
        )

    def on_entity_leave(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        entity.visualizer.move_to(
            y=int((self.y_bottom+self.y_top)/2),
            x=self.x_right
        )

    def on_entity_generate(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        vis = men.MessagesEntity(
            name=entity.name,
            message_core=self.visualizer,
            y=int((self.y_bottom+self.y_top)/2),
            x=self.x_left,
            old_names=[]
        )
        entity.visualizer = vis

    def on_entity_copy(
            self,
            new_entity,
            old_entity,
            old_entity_names
    ):
        vis = men.MessagesEntity(
            name=new_entity.name,
            message_core=self.visualizer,
            y=old_entity.visualizer.y,
            x=old_entity.visualizer.x,
            old_names=old_entity_names
        )
        new_entity.visualizer = vis


