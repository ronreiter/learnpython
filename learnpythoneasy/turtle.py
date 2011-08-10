# creates a turtle_data json block to display, using the go and turn commands.
import math
import simplejson

def init_track():
	global moves, angle
	moves = []
	angle = float(math.radians(-90))

def go(distance):
	global moves
	diff_x = int(math.cos(angle) * distance * 4)
	diff_y = int(math.sin(angle) * distance * 4)
	moves.append([diff_x, diff_y])

def turn(degrees):
	global angle
	angle = angle + math.radians(degrees)

def is_drawing():
	return len(moves) > 0

def get_data():
	return {
		"output": "turtle", 
		"moves" : moves, 
		"angle" : int(math.degrees(angle))+90,
	}
