import bpmnvisualizer.bpmn.elements_functions.start_functions as stfun
import bpmnvisualizer.bpmn.elements_functions.delay_functions as defun


def get_delay_function(fun_name):
    return getattr(defun, fun_name)

def get_start_function(fun_name):
    return getattr(stfun, fun_name)
