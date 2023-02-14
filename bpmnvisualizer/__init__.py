import json
import os

import flask
from flask import request, render_template, send_from_directory

import bpmnvisualizer.bpmn.core as c
import bpmnvisualizer.bpmn.core.logic_core as lc
import bpmnvisualizer.bpmn.parser.bpmn_parser as bpmn_parser
import bpmnvisualizer.bpmn.parser.dict_parser as dict_parser

class BPMNVisualModel:
    def __init__(
        self,
        bpmn_folder_path,
        image_folder_path,
        ip,
        port,
        main_root,
        step_root,
        reset_root,
        set_model_root,
        write_stats,
        dropout_list_root,
        init_bpmn_name,
    ):
        self.ip = ip
        self.port = port
        self.bpmn_folder_path = bpmn_folder_path
        self.image_folder_path = image_folder_path
        self.main_root = main_root
        self.step_root = step_root
        self.reset_root = reset_root
        self.set_model_root = set_model_root
        self.write_stats_root = write_stats
        self.dropout_list_root = dropout_list_root

        self.bpmn_name = init_bpmn_name

        self.core = c.prepareVisualCore(c.constructFullBpmnPath(self.bpmn_folder_path, self.bpmn_name))


    def get_flask_app(self):

        app =  flask.Flask(
            'bpmn_api',
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static')
        )

        @app.route(f'{self.main_root}')
        def main():
            return self.main()

        @app.route(f'{self.step_root}')
        def step():
            return self.step()

        @app.route(f'{self.reset_root}')
        def reset():
            return self.reset()

        @app.route(f'{self.set_model_root}')
        def set_model():
            return self.set_model()

        @app.route(f'{self.write_stats_root}')
        def write_stats_from_model():
            return self.write_stats()

        @app.route(f'{self.dropout_list_root}')
        def get_dropout_list():
            return self.get_dropout_list()

        return app

    def main(self):
        model_name = request.args.get('model_name', default=None)
        if model_name:
            imgs = os.listdir(self.image_folder_path)
            imgs = [i[:-4] for i in imgs if i.endswith(".png")]
            bpmns = os.listdir(self.bpmn_folder_path)
            bpmns = [b[:-5] for b in bpmns if b.endswith(".bpmn")]
            if not(model_name in imgs) or not(model_name in bpmns):
                model_name = self.bpmn_name
        else:
            model_name = self.bpmn_name


        self.core.newModel(c.constructFullBpmnPath(self.bpmn_folder_path, model_name))
        return render_template(
            "index.html",
            ip = self.ip,
            port = self.port,
            step_root = self.step_root,
            reset_root = self.reset_root,
            set_model_root = self.set_model_root,
            write_stats = self.write_stats_root,
            dropout_list_root = self.dropout_list_root,
            bpmn_name = model_name,
        )



    def step(self):
        steps = request.args.get('steps', default=1, type=int)
        response = flask.Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, GET, OPTIONS'
        response.headers['Access-Control-Request-Method'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        self.core.step(steps)
        response.data = self.core.getJsonMessages()
        return response



    def reset(self):
        print('-----------------------------\n       model reseted\n-----------------------------')
        self.core.newModel(c.constructFullBpmnPath(self.bpmn_folder_path, self.bpmn_name))
        response = flask.Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, GET, OPTIONS'
        response.headers['Access-Control-Request-Method'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        response.data = json.dumps({'response': 'model reseted'})
        return response



    def set_model(self):
        model_name = request.args.get('model', default=1, type=str)
        response = flask.Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, GET, OPTIONS'
        response.headers['Access-Control-Request-Method'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        if model_name == 'default':
            model_name = self.bpmn_name
        pathModel = c.constructFullBpmnPath(self.bpmn_folder_path, model_name)
        pathImg = c.constructFullPngPath(self.image_folder_path, model_name)
        if os.path.isfile(pathImg) and os.path.isfile(pathModel):
            self.bpmn_name = model_name
            self.core.newModel(pathModel)
            print('-----------------------------\n       new model was set\n-----------------------------')
            img = open(pathImg, 'rb').read()
            response.mimetype = 'image/png'
            response.data = img
        else:
            response.mimetype = 'application/json'
            response.data = json.dumps({'response': 'error in model'})
        return response


    def write_stats(self):
        data = self.core.logic_core.stats()
        return json.dumps(data, ensure_ascii=False, indent=4)
        # data = self.core.logic_core.stats()
        # return data
        # path = os.path.join(os.path.dirname(__file__), 'results')
        # with open(path, "w+", encoding='utf-8') as jsonFile:
        #     jsonFile.write(json.dumps(data, ensure_ascii=False, indent=4))
        # print('-----------------------------\n       file written\n-----------------------------')
        # return send_from_directory(directory='results', path='data.json', as_attachment=True)


    def get_dropout_list(self):
        imgs = os.listdir(self.image_folder_path)
        imgs = [i[:-4] for i in imgs if i.endswith(".png")]
        bpmns = os.listdir(self.bpmn_folder_path)
        bpmns = [b[:-5] for b in bpmns if b.endswith(".bpmn")]
        common = list(set(bpmns).intersection(imgs))
        response = flask.Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, GET, OPTIONS'
        response.headers['Access-Control-Request-Method'] = '*'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        response.mimetype = 'application/json'
        response.data = json.dumps({'response': common})
        return response



class BPMNConsoleModel:
    def __init__(
            self
    ):
        self.ready = False
        self.core = None
        self.currModel = ''

    def set_model(
            self,
            new_model_path
    ):
        self.currModel = new_model_path
        bpmn_path = self.currModel
        bpmn_dict = bpmn_parser.bpmn_to_dict(bpmn_path)
        self.core = lc.LogicCore()

        blocks = dict_parser.blocks_from_dict(bpmn_dict=bpmn_dict, visual_type='console')
        flows = dict_parser.flows_from_dict(bpmn_dict=bpmn_dict, visual_type='console')

        self.core.add_blocks(blocks)
        self.core.add_flows(flows)

        self.ready = True

    def reset(self):
        self.set_model(self.currModel)

    def run(
            self,
            n=1
    ):
        if self.ready:
            self.core.run(n)
        else:
            print('set model first')

    def show_statistics(
            self
    ):
        self.core.show_statistics()

    def stats(
            self
    ):
        return self.core.stats()

    def get_params(
            self
    ):
        return self.core.get_params()

    def set_params(
            self,
            block_name,
            params
    ):
        self.core.set_params(block_name, params)

