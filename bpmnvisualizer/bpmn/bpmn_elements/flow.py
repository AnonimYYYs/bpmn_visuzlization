class Flow:
    def __init__(
            self,
            name: str,
            from_block_name: str,
            to_block_name: str,
            visualizer
    ):
        self.name: str = name
        self.from_block = None
        self.to_block = None
        self.from_block_name: str = from_block_name
        self.to_block_name: str = to_block_name
        self.visualizer = visualizer
        # vfl.VisualizingFlow(
        #     from_block_name=from_block_name,
        #     to_block_name=to_block_name,
        #     start_coords=start_coords,
        #     coords=coords
        # )

    def proceed_entity(
            self,
            entity
    ):
        self.visualizer.proceed_entity(entity)
        self.to_block.on_entity_enter(entity)

