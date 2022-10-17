#!/usr/bin/env python3
import rospy
import tf
import math
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn

if __name__ == "__main__":
    rospy.init_node("tf_listener", anonymous= True)

    rospy.wait_for_service("spawn")
    turtle2 = rospy.ServiceProxy("spawn", Spawn)
    turtle2(4, 2, 0, "turtle2")

    tf_listener = tf.TransformListener()
    turtle2_cmd_vel = Twist()
    turtle2_velocity_publisher = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size= 1)
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (translation, rotation) = tf_listener.lookupTransform("/turtle2_frame", "/turtle1_frame", rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        
        x_in_turtle1_frame = translation[0]
        y_in_turtle1_frame = translation[1]

        angular_velocity = 4 * math.atan2(y_in_turtle1_frame, x_in_turtle1_frame)
        linear_velocity = 0.5 * math.sqrt(x_in_turtle1_frame ** 2 + y_in_turtle1_frame ** 2)

        turtle2_cmd_vel.linear.x = linear_velocity
        turtle2_cmd_vel.angular.z = angular_velocity
        turtle2_velocity_publisher.publish(turtle2_cmd_vel)
        rate.sleep()