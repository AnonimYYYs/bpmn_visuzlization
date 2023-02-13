from random import choice

import bpmnvisualizer.bpmn.bpmn_elements.block as blk


class Selection(blk.Block):
    def __init__(
            self,
            name: str,
            label: str
    ):
        super().__init__(
            name=name,
            label=label
        )

    def on_entity_enter(
            self,
            entity
    ):
        super().on_entity_enter(entity)

    def on_entity_proceed(
            self,
            entity
    ):
        super().on_entity_proceed(entity)
        self.ent_queue.remove(entity)
        entity.args[f'selection_{self.name}'] = 0
        if len(self.flows_output) != 1:
            entity.args[f'selection_{self.name}'] = choice(range(len(self.flows_output)))
        self.ent_in_work.append(entity)

    def on_entity_leave(
            self,
            entity
    ):
        super().on_entity_leave(entity)
        self.ent_in_work.remove(entity)
        self.flows_output[entity.args[f'selection_{self.name}']].proceed_entity(entity)
        del entity.args[f'selection_{self.name}']

    def step(
            self
    ):
        while len(self.ent_queue) != 0:
            self.on_entity_proceed(self.ent_queue[0])
        while len(self.ent_in_work) != 0:
            self.on_entity_leave(self.ent_in_work[0])
        self.core.not_done_blocks.remove(self)
