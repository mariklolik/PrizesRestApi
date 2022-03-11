#!flask/bin/python
import json
from random import choice
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

promos = []
promo_n = 0
prizes = []
prizes_n = 0
participants = []
participants_n = 0
res = []


@app.route('/promo', methods=['POST'])
def create_promo():
    global promo_n, promos
    promos.append({})
    promos[promo_n]['id'] = promo_n
    promos[promo_n]['name'] = request.json['name']
    if 'description' in request.json:
        promos[promo_n]['description'] = request.json['description']
    else:
        promos[promo_n]['description'] = ''
    promo_n += 1
    return promo_n - 1


@app.route('/promo', methods=['GET'])
def send_promos():
    global promo_n, promos
    return json.dumps(promos)


@app.route('/promo/<int:id>', methods=['GET'])
def send_promo(id):
    global promo_n, promos
    return json.dumps(promos[id])


@app.route('/promo/<int:id>', methods=['PUT'])
def change_promo(id):
    global promo_n, promos
    promos[id]['name'] = request.json['name']
    promos[id]['description'] = request.json['description']
    return id


@app.route('/promo/<int:id>', methods=['DELETE'])
def delete_promo(id):
    global promo_n, promos
    promos.remove(id)
    promo_n -= 1
    return id


@app.route('/promo/<int:id>/participant', methods=['POST'])
def add_participant(id):
    global promo_n, promos, participants, participants_n
    participants.append({})
    participants[participants_n]['id'] = participants_n
    participants[participants_n]['name'] = request.json['name']
    if 'promo_id' not in participants[participants_n]:
        participants[participants_n]['promo_id'] = []
    participants[participants_n]['promo_id'].append(id)

    participants_n += 1
    return participants_n - 1


@app.route('/promo/<int:id>/participant/<int:participantid>', methods=['DELETE'])
def delete_participant(id, participantid):
    global promo_n, promos, participants, participants_n
    a = participants[participantid]['promo_id'].index(id)
    participants[participantid]['promo_id'].remove(a)
    return participantid


@app.route('/promo/<int:id>/prize', methods=['POST'])
def add_prize(id):
    global promo_n, promos, participants, participants_n, prizes, prizes_n
    prizes.append({})
    prizes[prizes_n]['promo_id'] = id
    prizes[prizes_n]['description'] = request.json['description']


@app.route('/promo/<int:id>/prize/<int:prizeid>', methods=['DELETE'])
def delete_prize(id, prizeid):
    global promo_n, promos, participants, participants_n, prizes
    a = prizes[prizeid]['promo_id'].index(id)
    prizes[prizeid]['promo_id'].remove(a)
    return prizeid


@app.route('/promo/<int:id>/raffle', methods=['POST'])
def raffle(id):
    global promo_n, promos, participants, participants_n, prizes, prizes_n
    partis = []
    prizez = []
    for i in participants:
        if id in i['promo_id']:
            partis.append(i)

    for i in prizes:
        if id == i['promo_id']:
            prizez.append(i)
    w = choice(partis)
    k = choice(prizez)
    return json.dumps({'winner':choice(partis),
                       'prize':k})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
