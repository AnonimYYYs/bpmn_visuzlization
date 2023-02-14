import bpmnvisualizer.bpmn.bpmn_elements.block as blk
import bpmnvisualizer.bpmn.elements_functions as funcs

class Delay(blk.Block):
    def __init__(
            self,
            name: str,
            label: str,
            function,
            params,
            capacity
    ):
        super().__init__(
            name=name,
            label=label,
            params=params,
            func=function
        )
        self.delay_generator = None
        self.stats['totalPassed'] = 0.0
        self.stats['totalTime'] = 0.0

        self.queueDistribution = dict()
        self.workDistribution = dict()
        self.capacity = capacity
        self.build_function(self.params)

    def build_function(
            self,
            params
    ):
        function = funcs.get_delay_function(self.function_name)
        self.params = params
        self.delay_generator = function(*self.params)

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
        delayTime = self.delay_generator()
        entity.args[f'delay_{self.name}'] = {'endTime': self.core.now + delayTime, 'delay': delayTime}
        self.ent_in_work.append(entity)

    def on_entity_leave(
            self,
            entity
    ):
        super().on_entity_leave(entity)
        self.ent_in_work.remove(entity)
        del entity.args[f'delay_{self.name}']
        self.flows_output[0].proceed_entity(entity)

    def step(
            self
    ):
        """
        First check if any entities are in work. If so, check if any can proceed further.
        Then check if working list have any free space and have entities in queue.
        If so - take one entity from queue to work.
        In the end - remove self from 'not done' in core
        """
        is_changed = True
        while is_changed:
            is_changed = False
            # make entities work
            i = 0
            while i < len(self.ent_in_work):
                entity = self.ent_in_work[i]
                if entity.args[f'delay_{self.name}']['endTime'] == self.core.now:
                    self.stats['totalTime'] += entity.args[f'delay_{self.name}']['delay']
                    self.stats['totalPassed'] += 1
                    self.on_entity_leave(entity)
                    is_changed = True
                    continue
                i += 1

            # take entity from queue and make it work
            while (len(self.ent_in_work) < self.capacity) & (len(self.ent_queue) != 0):
                entity = self.ent_queue[0]
                self.on_entity_proceed(entity)
                is_changed = True
                self.visualizer.on_entity_work(entity, params=f"delay={entity.args[f'delay_{self.name}']}")
        length = len(self.ent_in_work)
        if length != 0:
            self.workDistribution[length] = self.workDistribution.get(length, 0) + 1
        length = len(self.ent_queue)
        if length != 0:
            self.queueDistribution[length] = self.queueDistribution.get(length, 0) + 1
        self.core.not_done_blocks.remove(self)

    def get_stats(
            self
    ):
        meanTime = 0 if self.stats['totalTime'] == 0 else self.stats['totalTime'] / self.stats['totalPassed']
        toRet = super().get_stats()
        toRet['meanTimeInside'] = meanTime
        toRet['queueDistribution'] = self.queueDistribution
        toRet['filledAmountDistribution'] = self.workDistribution
        return toRet

    def show_statistic(
            self
    ):
        meanTime = 0 if self.stats['totalTime'] == 0 else self.stats['totalTime'] / self.stats['totalPassed']
        self.visualizer.show_delay_statistic(
            totalPassed=int(self.stats['totalPassed']),
            meanTimeInside=meanTime,
            filledAmountDistribution=self.workDistribution,
            queueDistribution=self.queueDistribution
        )
