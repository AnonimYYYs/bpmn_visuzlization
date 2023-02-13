class Block:
    def __init__(
            self,
            name: str,
            params=None,
            label: str = '',
            func: str = ''
    ):
        if params is None:
            params = []
        self.params = params
        self.name: str = name
        self.function_name: str = func
        self.type = self.__class__.__name__
        self.label: str = label if label != '' else name
        self.ent_queue: list = []
        self.ent_in_work: list = []
        self.ent_leaving_queue: list = []
        self.flows_input: list = []
        self.flows_output: list = []
        self.visualizer = None
        self.visual_args: dict = {}
        self.core = None
        self.stats = {}

    def build_function(
            self,
            params
    ):
        pass

    def on_entity_enter(
            self,
            entity
    ):
        """
        Puts entity that just came to queue
        tells core that this block is not empty any more
        Call this method as super when overwrite it
        """
        self.visualizer.on_entity_enter(entity)
        self.ent_queue.append(entity)
        self.core.filled_blocks.add(self)
        self.core.not_done_blocks.add(self)

    def on_entity_leave(
            self,
            entity
    ):
        """
        Puts entity into output flows corresponding to some logic
        Must be overwritten by concrete block type corresponding to its logic
        """
        self.visualizer.on_entity_leave(entity)

    def on_entity_proceed(
            self,
            entity
    ):
        """
        Gets entity from queue and do the things with it
        Must be overwritten by concrete block type corresponding to its logic
        """
        self.visualizer.on_entity_proceed(entity)

    def step(
            self
    ):
        """
        check if self can proceed any entities and make if can
        Must be overwritten by concrete block type corresponding to its logic
        """
        pass

    def is_have_entities(
            self
    ):
        return not((len(self.ent_queue) + len(self.ent_in_work) + len(self.ent_leaving_queue)) == 0)

    def add_out_flow(
            self,
            flow_to_add
    ):
        if flow_to_add.from_block_name != self.name:
            raise Exception
        self.flows_output.append(flow_to_add)
        flow_to_add.from_block = self

    def add_in_flow(
            self,
            flow_to_add
    ):
        if flow_to_add.to_block_name != self.name:
            raise Exception
        self.flows_input.append(flow_to_add)
        flow_to_add.to_block = self

    def get_stats(
            self
    ):
        toRet = self.stats.copy()
        toRet['type'] = self.type
        return toRet

    def show_statistic(
            self
    ):
        pass

    def get_params(
            self
    ):
        return {'params': self.params, 'type': self.type}