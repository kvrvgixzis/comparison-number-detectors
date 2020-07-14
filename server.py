from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
import xml.etree.ElementTree as ET
import os
from base64 import b64encode

mc = MongoClient(host='192.168.0.101', port=27017)['faces2']['numbers_test']
app = Flask(__name__)


@app.route('/')
def index():

    start = request.args.get('start', default=0, type=int)
    end = request.args.get('end', default=start+10, type=int)
    context = {'count': mc.count()}
    if start >= context['count']:
        start = context['count'] - 10
        end = context['count']
    numbers = mc.find().skip(start).limit(end-start)
    context['last'] = end
    nn = []
    for n in numbers:
        if n['detections']:
            nn.append({'image_name': n['stream_name'], 'image': n['image'], "numbers_AI": n['detections'][0]['number'],
                       "detections_AI": {'number': n['detections'][0]['number'], 'crop': b64encode(n['detections'][0]['image']).decode("utf-8")},
                       'xml_number': ET.parse(f'./static/numbers/{n["stream_name"].split(".")[0]}.xml').getroot().find('License').text.replace("|", ""),
                       'state': n.get('state', None)})
        else:
            nn.append({'image_name': n['stream_name'], 'image': n['image'], "numbers_AI": None, "detections_AI": None,
                       'xml_number': ET.parse(f'./static/numbers/{n["stream_name"].split(".")[0]}.xml').getroot().find('License').text.replace("|", "") if ET.parse(f'./static/numbers/{n["stream_name"].split(".")[0]}.xml').getroot().find('License') else None,
                       'state': n.get('state', None)})

        # for number in n['detections']:
        #     nn[-1]['numbers_AI'].append(number['number'])
        #     nn[-1]['detections_AI'].append({'number': number['number'], 'crop': number['image']})
    context['numbers'] = nn
    return render_template('index.html', **context)


@app.route('/mark')
def mark():
    source = request.args.get('source', type=str)
    state = request.args.get('state', default=None, type=bool)
    finded = 0
    updated = 0
    if source:
        result = mc.update_one({'stream_name': source}, {'$set': {'state': state}})
        finded = result.matched_count
        updated = result.modified_count
    return jsonify({'finded': finded, 'updated': updated})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
