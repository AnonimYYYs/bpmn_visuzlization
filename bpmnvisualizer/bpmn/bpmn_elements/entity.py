
class Entity:
    def __init__(
            self,
            name: str
    ):
        self.name: str = name
        self.visualizer = None
        self.args: dict = dict()

    def copy(
            self
    ):
        entity = Entity(self.name)
        entity.args = self.args.copy()
        return entity

    def delete(
            self
    ):
        self.visualizer.delete()
        del self
