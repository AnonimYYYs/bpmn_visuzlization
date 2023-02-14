from bpmnvisualizer import BPMNVisualModel

initialData = {
    'bpmn_folder': './models/models',
    'image_folder': './models/model_images',
    'ip': '127.0.0.1',
    'port': 3000,
    "main_root": "/",
    "step_root": "/step",
    "reset_root": "/reset",
    "set_model_root": "/set_model",
    "write_stats": "/write_stats",
    "dropout_list_root": "/dropout_list",
    "init_bpmn_name": 'кольцо строповочное',
}

if __name__ == '__main__':
    model = BPMNVisualModel(
        bpmn_folder_path=initialData['bpmn_folder'],
        image_folder_path=initialData['image_folder'],
        ip=initialData['ip'],
        port=initialData['port'],
        main_root=initialData['main_root'],
        step_root=initialData['step_root'],
        reset_root=initialData['reset_root'],
        set_model_root=initialData['set_model_root'],
        write_stats=initialData['write_stats'],
        init_bpmn_name=initialData['init_bpmn_name'],
        dropout_list_root=initialData['dropout_list_root']
    )
    app = model.get_flask_app()

    # app is flask.Flask() instance

    app.run(port=initialData['port'], host=initialData['ip'])