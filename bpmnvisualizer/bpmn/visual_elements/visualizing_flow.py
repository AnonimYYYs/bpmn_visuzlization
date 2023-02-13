class VisualizingFlow:
    def __init__(
            self,
            name: str,
            from_block_name: str,
            to_block_name: str,
            args: dict
    ):
        self.name: str = name
        self.from_block_name: str = from_block_name
        self.to_block_name: str = to_block_name

    def proceed_entity(
            self,
            entity
    ):
        pass
