import bpmnvisualizer.bpmn.bpmn_elements.block as blk

class End(blk.Block):
    def __init__(
            self,
            name: str,
            label: str
    ):
        super().__init__(
            name=name,
            label=label
        )
        self.stats['totalEndTime'] = 0.0
        self.stats['countDeleted'] = 0.0

    def delete_entity(
            self,
            entity
    ):
        timeInside = self.core.now - entity.args['genTime']
        self.visualizer.on_entity_final_delete(entity, params=timeInside)
        self.stats['totalEndTime'] += timeInside
        self.stats['countDeleted'] += 1
        entity.delete()

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
        self.delete_entity(entity)

    def step(
            self
    ):
        while len(self.ent_queue) != 0:
            self.on_entity_proceed(self.ent_queue[0])
        while len(self.ent_in_work) != 0:
            self.on_entity_leave(self.ent_in_work[0])
        self.core.not_done_blocks.remove(self)

    def show_statistic(
            self
    ):
        meanTime = 0 if self.stats['countDeleted'] == 0 else self.stats['totalEndTime'] / self.stats['countDeleted']
        self.visualizer.show_end_statistic(
            totalDeleted=int(self.stats['countDeleted']),
            meanEntityTime=meanTime
        )

    def get_stats(
            self
    ):
        meanTime = 0 if self.stats['countDeleted'] == 0 else self.stats['totalEndTime'] / self.stats['countDeleted']
        toRet = super().get_stats()
        toRet['meanEntityTime'] = meanTime
        return toRet
