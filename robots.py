from sys import argv
import json
from collections import deque, OrderedDict

robot = OrderedDict()
script, filename = argv

# keeps track of the current robot's bearing
compass = deque(['north','east','south','west'])

direction = {
	'north':[0,1],
	'east':[1,0],
	'south':[0,-1],
	'west':[-1,0],
}

# update the compass and robot position
def move(data):
	length = len(robot)-1
	movement = data['movement']
	bearing = robot[length]['bearing']

	if movement == 'turn-right':
		compass.rotate(-1)
	elif movement == 'turn-left':
		compass.rotate(1)
	new_bearing = compass[0]

	robot[length]['position']['x'] += direction[new_bearing][0]
	robot[length]['position']['y'] += direction[new_bearing][1]

# create a new robot
def create_robot(data):
	length = len(robot)
	robot[length] = OrderedDict()
	robot[length]['type'] = 'robot'
	robot[length]['position'] = OrderedDict([( 'x' , data['position']['x'] ) , ( 'y' , data['position']['y'] )])
	robot[length]['bearing'] = data['bearing']
	
	# reset compass
	while compass[0] != data['bearing']:
		compass.rotate(1)

def detect_type(data):
	
	if data['type'] == 'new-robot':
		create_robot(data)
		
	elif data['type'] == 'move':
		move(data)

def finish():
	for key, val in robot.items():
		print json.dumps(val)

with open(filename) as f:
    for line in f:
        detect_type(json.loads(line))
finish()