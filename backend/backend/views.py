from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rpma_server import PMemDNNCheckpoint, CheckpointSystem
from glob import glob
import json

current_device = "/dev/dax1.0"

def get_model_info(request):
    size = 16*1024*1024*1024
    chksys = CheckpointSystem(current_device, size, False, False)
    assert(chksys is not None)
    model_dict = {'models': 0, 'model_list': []}
    chkpts = chksys.existing_chkpts()
    model_dict['models'] = len(chkpts)
    for chkpt_name in chkpts:
        chkpt = chksys.get_chkpt(chkpt_name)
        nlayers = len(chkpt.get_layers_info())
        model_dict['model_list'].append({'name': chkpt_name, 'layers': nlayers})
    return JsonResponse(model_dict)

def get_pmem_usage(request):
    size = 16*1024*1024*1024
    chksys = CheckpointSystem(current_device, size, False, False)
    assert(chksys is not None)
    usage_dict = {'num_parts': 0, 'percentages': []}
    part_names = ['Valid Checkpoints', 'Invalid Checkpoints', 'Free Space']
    nparts = len(part_names)
    usage_dict['num_parts'] = nparts
    chkpts = chksys.existing_chkpts()
    usage_size = [0, 0, 0] # valid, invalid, free
    for chkpt_name in chkpts:
        chkpt = chksys.get_chkpt(chkpt_name)
        layers = chkpt.get_layers_info()
        usage_size[0] += sum([i[1] for i in layers])
    usage_size[-1] = size - sum(usage_size[:-1])
    for i, name in enumerate(part_names):
        usage_dict['percentages'].append({'value':usage_size[i], 'name':name})
    return JsonResponse(usage_dict)

def get_devs(request):
    device_dict = {'devices': []}
    global current_device
    for daxdev in sorted(glob('/dev/dax*')):
        device_dict['devices'].append(daxdev)
    current_device = device_dict['devices'][0]
    return JsonResponse(device_dict)

@csrf_exempt
def switch_device(request):
    req_data = json.loads(request.read())['content']
    desired_dev = req_data[1]
    if desired_dev not in glob('/dev/dax*'):
        return HttpResponseServerError("Fuck no such device!")
    global current_device
    current_device = desired_dev
    return HttpResponse("ack!")
