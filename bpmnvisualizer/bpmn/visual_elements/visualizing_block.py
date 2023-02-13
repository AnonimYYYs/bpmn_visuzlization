import bpmnvisualizer.bpmn.bpmn_elements.entity as ent

import bpmnvisualizer.bpmn.visual_elements.vizualizing_entity as een

class VisualizingBlock:
    def __init__(
            self,
            name: str,
            label: str,
            args: dict
    ):
        self.name = name
        self.label = label

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
        pass

    def on_entity_proceed(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        pass

    def on_entity_leave(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        pass

    def on_entity_generate(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        pass

    def on_entity_delete(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        pass

    def on_entity_final_delete(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        pass

    def on_entity_copy(
            self,
            new_entity,
            old_entity,
            old_entity_names,
    ):
        new_entity.visualizer = een.VisualisingEntity(name=old_entity.visualizer.name)

    def delete(
            self
    ):
        pass

    def show_delay_statistic(
            self,
            meanTimeInside,
            filledAmountDistribution,
            queueDistribution,
            totalPassed
    ):
        pass

    def show_start_statistic(
            self,
            totalGenerated
    ):
        pass

    def show_end_statistic(
            self,
            totalDeleted,
            meanEntityTime
    ):
        pass
