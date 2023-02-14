import bpmnvisualizer.bpmn.bpmn_elements.start as st

class LogicCore:
    def __init__(
            self
    ):
        self.now: int = 0
        self.blocks: dict = {}
        self.filled_blocks: set = set()
        self.not_done_blocks: set = set()

    def _add_block(
            self,
            block_to_add
    ):
        if isinstance(block_to_add, st.Start):
            self.filled_blocks.add(block_to_add)
            self.not_done_blocks.add(block_to_add)
        self.blocks[block_to_add.name] = block_to_add
        block_to_add.core = self

    def _add_flow(
            self,
            flow_to_add
    ):
        block = self.blocks.get(flow_to_add.from_block_name, None)
        if block is None:
            raise Exception
        block.add_out_flow(flow_to_add)

        block = self.blocks.get(flow_to_add.to_block_name, None)
        if block is None:
            raise Exception
        block.add_in_flow(flow_to_add)

    def _step(
            self
    ):
        print(f'\n-----------------------------\n       step {self.now}->{self.now + 1}\n-----------------------------')
        while len(self.not_done_blocks) != 0:
            block = next(iter(self.not_done_blocks))
            block.step()
            if not(block.is_have_entities()):
                self.filled_blocks.remove(block)
        self.not_done_blocks = set(i for i in self.filled_blocks)
        self.now += 1

    def add_blocks(
            self,
            blocks: list
    ):
        for block in blocks:
            self._add_block(block)

    def add_flows(
            self,
            flows: list
    ):
        for flow in flows:
            self._add_flow(flow)

    def run(
            self,
            time
    ):
        for _ in range(time):
            self._step()

    def show_statistics(
            self
    ):

        for i in self.blocks:
            self.blocks[i].show_statistic()

    def stats(
            self
    ):
        return {self.blocks[name].label: self.blocks[name].get_stats() for name in self.blocks}

    def get_params(
            self
    ):
        return {self.blocks[name].name: self.blocks[name].get_params() for name in self.blocks}

    def set_params(
            self,
            block_name,
            params
    ):
        self.blocks[block_name].build_function(params)
