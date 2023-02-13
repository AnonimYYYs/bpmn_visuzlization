import bpmnvisualizer.bpmn.visual_elements.visualizing_block as evb
import bpmnvisualizer.bpmn.visual_elements.console_block as cvb
import bpmnvisualizer.bpmn.visual_elements.messages_block as mvb

import bpmnvisualizer.bpmn.visual_elements.visualizing_flow as efl
import bpmnvisualizer.bpmn.visual_elements.console_flow as cfl
import bpmnvisualizer.bpmn.visual_elements.messages_flow as mfl

import bpmnvisualizer.bpmn.bpmn_elements.start as st
import bpmnvisualizer.bpmn.bpmn_elements.end as end
import bpmnvisualizer.bpmn.bpmn_elements.delay as dl
import bpmnvisualizer.bpmn.bpmn_elements.selection as sel
import bpmnvisualizer.bpmn.bpmn_elements.parallel as prl
import bpmnvisualizer.bpmn.bpmn_elements.flow as flw

import bpmnvisualizer.bpmn.core.message_core as mcr


def get_item(collection, key, target):
    return next((item for item in collection if item.get(key, None) == target), None)


def blocks_from_dict(
        bpmn_dict,
        visual_type=None,
        visual_core=None,
        delta_x=0,
        delta_y=0
):
    BlockVisualizer = evb.VisualizingBlock
    if visual_type == 'console':
        BlockVisualizer = cvb.ConsoleBlock
    if visual_type == 'messages':
        BlockVisualizer = mvb.MessagingBlock
        if not(isinstance(visual_core, mcr.MessageCore)):
            raise BaseException

    blocks: list = []
    process = bpmn_dict['bpmn:definitions']['bpmn:process']
    diagram = bpmn_dict['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']

    if type(process.get('bpmn:startEvent', [])) is dict:
        process['bpmn:startEvent'] = [process['bpmn:startEvent']]
    for block in process.get('bpmn:startEvent', []):
        coords = get_item(diagram.get('bpmndi:BPMNShape', []), '@bpmnElement', block['@id']).get('dc:Bounds', {})
        coords['@x'] = int(coords['@x']) - delta_x
        coords['@y'] = int(coords['@y']) - delta_y
        label = block.get('@name', '')
        function = 'sequence'
        params = [1]
        if label != '':
            for row in label.split('\n')[1:]:
                if row.startswith('fun'):
                    function = row.split('=')[1]
                if row.startswith('params'):
                    params = [int(i) for i in row.split('=')[1].split(',')]
            label = label.split('\n')[0]
        to_add_block = st.Start(
            name=block['@id'],
            label=label,
            function=function,
            params=params
        )
        to_add_block.visualizer = BlockVisualizer(
            name=block['@id'],
            label=label,
            args={
                'coords': coords,
                'message_core': visual_core
            }
        )
        blocks.append(to_add_block)

    if type(process.get('bpmn:endEvent', [])) is dict:
        process['bpmn:endEvent'] = [process['bpmn:endEvent']]
    for block in process.get('bpmn:endEvent', []):
        coords = get_item(diagram.get('bpmndi:BPMNShape', []), '@bpmnElement', block['@id']).get('dc:Bounds', {})
        coords['@x'] = int(coords['@x']) - delta_x
        coords['@y'] = int(coords['@y']) - delta_y
        label = block.get('@name', block['@id'])
        to_add_block = end.End(
            name=block['@id'],
            label=label
        )
        to_add_block.visualizer = BlockVisualizer(
            name=block['@id'],
            label=label,
            args={
                'coords': coords,
                'message_core': visual_core}
        )
        blocks.append(to_add_block)

    if type(process.get('bpmn:task', [])) is dict:
        process['bpmn:task'] = [process['bpmn:task']]
    for block in process.get('bpmn:task', []):
        coords = get_item(diagram.get('bpmndi:BPMNShape', []), '@bpmnElement', block['@id']).get('dc:Bounds', {})
        coords['@x'] = int(coords['@x']) - delta_x
        coords['@y'] = int(coords['@y']) - delta_y
        label = block.get('@name', '')
        function = 'constant'
        params = [1]
        capacity = 1
        if label != '':
            for row in label.split('\n')[1:]:
                if row.startswith('fun'):
                    function = row.split('=')[1]
                if row.startswith('capacity'):
                    capacity = int(row.split('=')[1])
                if row.startswith('params'):
                    params = [i for i in row.split('=')[1].split(',')]
            label = label.split('\n')[0]
        to_add_block = dl.Delay(
            name=block['@id'],
            label=label,
            function=function,
            params=params,
            capacity=capacity
        )
        to_add_block.visualizer = BlockVisualizer(
            name=block['@id'],
            label=label,
            args={
                'coords': coords,
                'message_core': visual_core}
        )
        blocks.append(to_add_block)

    if type(process.get('bpmn:exclusiveGateway', [])) is dict:
        process['bpmn:exclusiveGateway'] = [process['bpmn:exclusiveGateway']]
    for block in process.get('bpmn:exclusiveGateway', []):
        coords = get_item(diagram.get('bpmndi:BPMNShape', []), '@bpmnElement', block['@id']).get('dc:Bounds', {})
        coords['@x'] = int(coords['@x']) - delta_x
        coords['@y'] = int(coords['@y']) - delta_y
        to_add_block = sel.Selection(
            name=block['@id'],
            label=block.get('@name', block['@id'])
        )
        to_add_block.visualizer = BlockVisualizer(
            name=block['@id'],
            label=block.get('@name', block['@id']),
            args={
                'coords': coords,
                'message_core': visual_core
            }
        )
        blocks.append(to_add_block)

    if type(process.get('bpmn:parallelGateway', [])) is dict:
        process['bpmn:parallelGateway'] = [process['bpmn:parallelGateway']]
    for block in process.get('bpmn:parallelGateway', []):
        coords = get_item(diagram.get('bpmndi:BPMNShape', []), '@bpmnElement', block['@id']).get('dc:Bounds', {})
        coords['@x'] = int(coords['@x']) - delta_x
        coords['@y'] = int(coords['@y']) - delta_y
        name, label = block['@id'], block.get('@name', block['@id'])
        if type(block['bpmn:incoming']) is str:
            to_add_block = prl.ParallelOpen(
                name=name,
                label=label
            )
        else:
            to_add_block = prl.ParallelClose(
                name=name,
                label=label
            )
        to_add_block.visualizer = BlockVisualizer(
                name=name,
                label=label,
                args={
                    'coords': coords,
                    'message_core': visual_core
                }
        )
        blocks.append(to_add_block)
    return blocks


def flows_from_dict(
        bpmn_dict,
        visual_type=None,
        delta_x=0,
        delta_y=0
):
    FlowVisualizer = efl.VisualizingFlow
    if visual_type == 'console':
        FlowVisualizer = cfl.ConsoleFlow
    if visual_type == 'messages':
        FlowVisualizer = mfl.MessageFlow

    flows: list = []
    process = bpmn_dict['bpmn:definitions']['bpmn:process']
    diagram = bpmn_dict['bpmn:definitions']['bpmndi:BPMNDiagram']['bpmndi:BPMNPlane']

    if type(process.get('bpmn:sequenceFlow', [])) is dict:
        process['bpmn:sequenceFlow'] = [process['bpmn:sequenceFlow']]
    if type(diagram.get('bpmndi:BPMNEdge', [])) is dict:
        diagram['bpmndi:BPMNEdge'] = [diagram['bpmndi:BPMNEdge']]
    for flow in process.get('bpmn:sequenceFlow', []):
        coords = get_item(diagram.get('bpmndi:BPMNEdge', []), '@bpmnElement', flow['@id']).get('di:waypoint', [])
        flows.append(flw.Flow(
            name=flow['@id'],
            from_block_name=flow['@sourceRef'],
            to_block_name=flow['@targetRef'],
            visualizer=FlowVisualizer(
                name=flow['@id'],
                from_block_name=flow['@sourceRef'],
                to_block_name=flow['@targetRef'],
                args={
                    'start_coords': {'x': int(coords[0]['@x']) - delta_x, 'y': int(coords[0]['@y']) - delta_y},
                    'coords': [{'x': int(coord['@x']) - delta_x, 'y': int(coord['@y']) - delta_y} for coord in coords[1:]]
                }
            )
        ))
    return flows
