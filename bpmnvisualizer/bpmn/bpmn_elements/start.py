import bpmnvisualizer.bpmn.bpmn_elements.block as blk
import bpmnvisualizer.bpmn.bpmn_elements.entity as ent
import bpmnvisualizer.bpmn.elements_functions as funcs

class Start(blk.Block):
    def __init__(
            self,
            name: str,
            label: str,
            function,
            params,
    ):
        super().__init__(
            name=name,
            label=label,
            func=function,
            params=params
        )

        self.generator = None
        self.build_function(self.params)
        self.gen_amount: int = 0
        self.stats['totalGenerated'] = 0

    def build_function(
            self,
            params
    ):
        function = funcs.get_start_function(self.function_name)
        self.params = params
        self.generator = function(*self.params)

    def generate_entity(
            self,
            name: str
    ):
        entity = ent.Entity(
            name=name
        )
        entity.args['genTime'] = self.core.now
        self.visualizer.on_entity_generate(entity)
        self.on_entity_enter(entity)
        self.stats['totalGenerated'] += 1

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
        self.ent_in_work.append(entity)

    def on_entity_leave(
            self,
            entity
    ):
        super().on_entity_leave(entity)
        self.ent_in_work.remove(entity)
        self.flows_output[0].proceed_entity(entity)

    def step(
            self
    ):
        self.gen_amount = self.generator(self.core.now)
        self.gen_amount = 0 if (self.gen_amount < 0) else self.gen_amount
        for i in range(self.gen_amount):
            self.generate_entity(f'ent_{self.core.now}_{i}_{self.label}')
        while len(self.ent_queue) != 0:
            self.on_entity_proceed(self.ent_queue[0])
        while len(self.ent_in_work) != 0:
            self.on_entity_leave(self.ent_in_work[0])
        self.gen_amount = 0
        self.core.not_done_blocks.remove(self)

    def is_have_entities(
            self
    ):
        return True

    def statistic(
            self
    ):
        self.visualizer.show_start_statistic(
            totalGenerated=self.stats['totalGenerated']
        )

