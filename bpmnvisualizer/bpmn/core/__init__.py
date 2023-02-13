import bpmnvisualizer.bpmn.core.logic_core as lc
import bpmnvisualizer.bpmn.core.message_core as mc
import bpmnvisualizer.bpmn.parser.bpmn_parser as bpmn_parser
import bpmnvisualizer.bpmn.parser.dict_parser as dict_parser

import json


def constructFullBpmnPath(folder, name):
    return f'{folder}/{name}.bpmn'


def constructFullPngPath(folder, name):
    return f'{folder}/{name}.png'


def prepareVisualCore(bpmn_path):
    class VC:
        def __init__(self):
            self.logic_core = None
            self.message_core = None
            self.newModel(bpmn_path)

        def step(self, steps=1):
            self.logic_core.run(steps)

        def getJsonMessages(self):
            return json.dumps(self.message_core.get_messages())

        def newModel(self, path):
            bpmn_dict = bpmn_parser.bpmn_to_dict(path)

            delta_x, delta_y = bpmn_parser.get_coords_deltas(path)

            self.logic_core = lc.LogicCore()
            self.message_core = mc.MessageCore()

            blocks = dict_parser.blocks_from_dict(
                delta_x=delta_x,
                delta_y=delta_y,
                bpmn_dict=bpmn_dict,
                visual_type='messages',
                visual_core=self.message_core
            )
            flows = dict_parser.flows_from_dict(
                delta_x=delta_x,
                delta_y=delta_y,
                bpmn_dict=bpmn_dict,
                visual_type='messages'
            )

            self.logic_core.add_blocks(blocks)
            self.logic_core.add_flows(flows)
    return VC()
