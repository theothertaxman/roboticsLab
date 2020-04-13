#!/usr/bin/env python  
import rospy
from geometry_msgs.msg import Twist # for cmd_vel topic
from sensor_msgs.msg import Range # for /proximity topic

# list used to store sensor values
sensor_values = {0: 0,
        1: 0,
        2: 0,
        5: 0,
        6: 0,
        7: 0}

# TODO weight dictionary here
weight_left = {0: 10,
	1: 8,
	2: 4,	
	5: -4,
	6: -8,
	7:-10}
weight_right = {0: -10,
	1: -8,
	2: -4,
	5: 4,
	6: 8,
	7:10}

def getTwist(leftMotorSpeed, rightMotorSpeed):
    """Get a new twist message from differential-drive left-right motor speeds.

    :leftMotorSpeed: number
    :rightMotorSpeed: number
    :returns: geometry_msgs.Twist object"""

    wheelSeparation = 5.3

    newValue = Twist()

    newValue.linear.x = (leftMotorSpeed + rightMotorSpeed) / 2
    newValue.angular.z = (rightMotorSpeed - leftMotorSpeed) / wheelSeparation

    return newValue
# end getTwist()

def calculateSensorsWeightSum(weights):
	sum = 0
	for key in sensor_values.keys():
		if(key in weights):
			sum += weights[key] * sensor_values[key]
		else:
			print("No element defined for weights at index ", key)
	return sum

def handleDistanceSensors(data, sensor_id):
    """Receives new sensor data from the ROS topic
    :data: Range object
    :sensor_id: number"""

    distance = data.range * 15
    # TODO store `distance` variable in the `sensor_values` dictionary using `sensor_id` as key
    rospy.loginfo("Received sensor[%d] = %.2f" %(sensor_id, distance))
    sensor_values[sensor_id] = distance
	
# end handleDistanceSensors()

if __name__ == '__main__':
    rospy.init_node('avoid')

    prox = {0: "/ePuck0/proximity0",
            1: "/ePuck0/proximity1",
            2: "/ePuck0/proximity2",
            5: "/ePuck0/proximity5",
            6: "/ePuck0/proximity6",
            7: "/ePuck0/proximity7"}

    for (sensorNr, topic) in prox.items():
        rospy.Subscriber(topic, Range, handleDistanceSensors, sensorNr)

    epuckVel = rospy.Publisher('ePuck0/cmd_vel', Twist,queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():

        # TODO replace the `getTwist(10, 10)` with `getTwist(left, right)`,
        #       where `left` and `right` are values computed dinamically based on sensor values
	#Compute sum = weight + sensor values
	sumLeft = calculateSensorsWeightSum(weight_left)
	left = 5 + sumLeft
	
	
	sumRight = calculateSensorsWeightSum(weight_right)
	right = 5 + sumRight
	cmd = getTwist(left, right)
        epuckVel.publish(cmd)

        rate.sleep()
