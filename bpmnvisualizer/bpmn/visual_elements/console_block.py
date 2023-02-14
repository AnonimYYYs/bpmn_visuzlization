import bpmnvisualizer.bpmn.visual_elements.visualizing_block as vb
import bpmnvisualizer.bpmn.bpmn_elements.entity as ent
import bpmnvisualizer.bpmn.visual_elements.vizualizing_entity as een

class ConsoleBlock(vb.VisualizingBlock):
    def __init__(
            self,
            name: str,
            label: str,
            args: dict
    ):
        super().__init__(name, label, args)

    def on_entity_work(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        print(f"{entity.name} working at {self.label} (id:{self.name}); {params}")

    def on_entity_enter(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        print(f"{entity.name} has entered {self.label} (id:{self.name});")

    def on_entity_proceed(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        print(f"{entity.name} proceeding at {self.label} (id:{self.name});")

    def on_entity_leave(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        print(f"{entity.name} has left {self.label} (id:{self.name});")

    def on_entity_generate(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        entity.visualizer = een.VisualisingEntity('')
        print(f"{entity.name} was generated at {self.label} (id:{self.name});")

    def on_entity_delete(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        print(f"{entity.name} was deleted at {self.label} (id:{self.name});")

    def on_entity_final_delete(
            self,
            entity: ent.Entity,
            params: str = ''
    ):
        print(f"{entity.name} was deleted at {self.label} (id:{self.name}); time inside: {params}")

    def show_delay_statistic(
            self,
            meanTimeInside,
            filledAmountDistribution,
            queueDistribution,
            totalPassed
    ):
        print(f"statistic about delay '{self.label}'")
        print(f'>> total entities passed: {totalPassed}')
        print(f'>> mean time inside: {meanTimeInside}')
        print(f'>> working amount distribution: {filledAmountDistribution}')
        print(f'>> waiting queue distribution: {queueDistribution}')

    def show_start_statistic(
            self,
            totalGenerated
    ):
        print(f"statistic about generator '{self.label}'")
        print(f'>> total generated at this block: {totalGenerated}')

    def show_end_statistic(
            self,
            totalDeleted,
            meanEntityTime
    ):
        print(f"statistic about end block '{self.label}'")
        print(f'>> total deleted at this block: {totalDeleted}')
        print(f'>> mean time of entity inside model: {meanEntityTime}')

