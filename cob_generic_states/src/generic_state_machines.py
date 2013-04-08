#!/usr/bin/python

import roslib; roslib.load_manifest('cob_generic_states')
import rospy

import smach
import smach_ros

# generic states
from generic_manipulation_states import *
from generic_perception_states import *

class sm_open_door(smach.StateMachine):
	def __init__(self):	
		smach.StateMachine.__init__(self, 
			outcomes=['succeeded', 'door_not_opened', 'failed'])
		
		with self:
			smach.StateMachine.add('DETECT_DOOR', detect_object("door", max_retries = 10),
				transitions={'succeeded':'OPEN_DOOR', 
							'retry':'DETECT_DOOR', 
							'no_more_retries':'door_not_opened', 
							'failed':'failed'})

			smach.StateMachine.add('OPEN_DOOR', open_door(),
				transitions={'succeeded':'succeeded', 
							'retry':'DETECT_DOOR',
							'no_more_retries':'door_not_opened',
							'failed':'failed'})

class sm_pick_object(smach.StateMachine):
	def __init__(self):	
		smach.StateMachine.__init__(self, 
			outcomes=['object_picked_top', 'object_picked_side', 'object_not_picked', 'failed'],
			input_keys=['object_name'])
		
		with self:
			smach.StateMachine.add('DETECT_OBJECT', detect_object(max_retries = 10),
				transitions={'succeeded':'SELECT_GRASP', 
							'retry':'DETECT_OBJECT', 
							'no_more_retries':'object_not_picked', 
							'failed':'failed'})

			smach.StateMachine.add('SELECT_GRASP', select_grasp(),
				transitions={'top':'GRASP_TOP', 
							'side':'GRASP_SIDE', 
							'failed':'failed'})
			
			smach.StateMachine.add('GRASP_SIDE', grasp_side(max_retries = 10),
				transitions={'succeeded':'object_picked_side', 
							'retry':'DETECT_OBJECT', 
							'no_more_retries':'object_not_picked', 
							'failed':'failed'})
				
			smach.StateMachine.add('GRASP_TOP', grasp_top(max_retries = 10),
				transitions={'succeeded':'object_picked_top', 
							'retry':'DETECT_OBJECT', 
							'no_more_retries':'object_not_picked', 
							'failed':'failed'})
