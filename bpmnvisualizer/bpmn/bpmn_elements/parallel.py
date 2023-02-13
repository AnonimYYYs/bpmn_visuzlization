import bpmnvisualizer.bpmn.bpmn_elements.block as blk
import bpmnvisualizer.bpmn.bpmn_elements.entity as ent

class ParallelOpen(blk.Block):
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
        for i in range(len(self.flows_output)):
            new_entity = entity.copy()
            new_entity.name = f'{new_entity.name}:{i}_copy'
            new_entity.args['parallel'] = new_entity.args.get('parallel', dict()).copy()
            new_entity.args['parallel'][entity.name] = [i, len(self.flows_output)]
            self.visualizer.on_entity_copy(
                new_entity=new_entity,
                old_entity=entity,
                old_entity_names=[entity.name]
            )
            self.ent_in_work.append(new_entity)
        self.visualizer.on_entity_delete(entity)
        entity.delete()

    def on_entity_leave(
            self,
            entity
    ):
        super().on_entity_leave(entity)
        self.ent_in_work.remove(entity)
        a = entity.name.split(':')
        b = a[0]
        c = entity.args['parallel']
        d = c[b][0]
        self.flows_output[d].proceed_entity(entity)

    def step(
            self
    ):
        while len(self.ent_queue) != 0:
            self.on_entity_proceed(self.ent_queue[0])
        while len(self.ent_in_work) != 0:
            self.on_entity_leave(self.ent_in_work[0])
        self.core.not_done_blocks.remove(self)


class ParallelClose(blk.Block):
    def __init__(
            self,
            name: str,
            label: str
    ):
        super().__init__(
            name=name,
            label=label
        )
        self.counter = 0
        self.combine_queue: dict = dict()

    def on_entity_enter(
            self,
            entity
    ):
        """
        Receive entity from one of input flows and put it in waiting queue
        """
        super().on_entity_enter(entity)

    def on_entity_proceed(
            self,
            entity
    ):
        """
        Takes unsorted entity from waiting queue and put sort it by "parallel" args
        Put in few queues to wait while one of them would be filled to combine some entities into one
        """
        super().on_entity_proceed(entity)
        self.ent_queue.remove(entity)
        for name in entity.args['parallel']:
            self.combine_queue[name] = self.combine_queue.get(name, {
                'len': entity.args['parallel'][name][1],
                'entities': []
            })
            self.combine_queue[name]['entities'].append(entity)

    def on_entity_queue_combine(
            self,
            to_combine_name: str
    ):
        entities = self.combine_queue[to_combine_name]['entities']
        del self.combine_queue[to_combine_name]
        old_names = [entity.name for entity in entities]
        names = [entity.name.split(':') for entity in entities]

        name = []
        for i in range(len(names[0])):
            if names[0][i] == names[1][i]:
                name.append(names[0][i])
        name = ':'.join(name)
        entity = ent.Entity(f'{self.counter}_{name}')
        self.visualizer.on_entity_copy(
            new_entity=entity,
            old_entity=entities[0],
            old_entity_names=old_names
        )
        self.counter += 1
        entity.args = entities[0].args
        del entity.args['parallel'][to_combine_name]
        self.ent_in_work.append(entity)
        while len(entities) != 0:
            entity = entities[0]
            entities.remove(entity)
            entity.delete()

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
        """
        First sort all entities from waiting queue by its 'parallel' queues
        Then check if any queue can be combined. Combine if so.
        Pass all combined entities to output flow
        """

        while len(self.ent_queue) != 0:
            self.on_entity_proceed(self.ent_queue[0])

        for name in [name for name in self.combine_queue if self.combine_queue[name]['len'] == len(self.combine_queue[name]['entities'])]:
            self.on_entity_queue_combine(name)

        while len(self.ent_in_work) != 0:
            self.on_entity_leave(self.ent_in_work[0])

        self.core.not_done_blocks.remove(self)
