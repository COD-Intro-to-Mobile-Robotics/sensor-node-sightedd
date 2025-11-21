import rclpy                    # import the ROS Client Library for Python (RCLPY)
from rclpy.node import Node     # from RCLPY, import the Node Class used to create ROS 2 nodes
from std_msgs.msg import Int32 # from standard messages, import the String message
from std_msgs.msg import String
from sensorlab import hat_library as hatLib
import RPi.GPIO as GPIO

class MinimalPublisher(Node):   # Create a new class called MinimalPublisher that inherits variables & functions from Node

    def __init__(self):
        super().__init__('minimal_publisher')                               # Initialize the Node with the name 'minimal_publisher'

        self.declare_parameter('publish_period', 0.5)  # seconds
        self.declare_parameter('sensor_id', 1)

        timer_period = float(self.get_parameter('publish_period').value)
        sensor_id = self.get_parameter('sensor_id').value
        self.get_logger().warn("self.sensor_id")
        if sensor_id == 1:
            self.pin = hatLib.IR1_INPUT_PIN
            self.get_logger().warn("Got Sensor 1")
        elif sensor_id == 2:
            self.pin = hatLib.IR2_INPUT_PIN
            self.get_logger().warn("Got Sensor 2")
        

        self.publisher_ = self.create_publisher(Int32, 'sensorA', 10)     # Create a publisher for String type messages on the topic 'my_topic'                                              # Define the timer period in seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)   # Create a timer that calls 'timer_callback' every 0.5 seconds
        self.get_logger().info(
            f"Sensor publisher started: period={timer_period}s, pin={self.pin}"
        )
        self.i = 0                                                          # Initialize a counter for message numbering

    def timer_callback(self):
        ir1Value = hatLib.get_ir_state(self.pin)
        if ir1Value == hatLib.INVALID:
            self.get_logger().warn("Got INVALID reading, not publishing")
            return

        if ir1Value == hatLib.DARK:
            state = "Dark"
        elif ir1Value == hatLib.LIGHT:
            state = "Light"
        else:
            state = "UNKNOWN"
        msg = Int32()                                          # Create a new String message
        msg.data = int(ir1Value)   
                    # Assign text to msg.data, including the current value of i
        self.publisher_.publish(msg)                            # Publish the message to the topic
        self.get_logger().info('Publishing: "%s"' % msg.data)   # Log the published message for debugging
        self.get_logger().info('Publishing: "%s"' % state)
        self.i += 1                                             # Increment the counter for the next message


def main(args=None):
    print ("Beginning to talk...")          # Print a starting message
    rclpy.init(args=args)                   # Initialize the ROS 2 Python client library

    minimal_publisher = MinimalPublisher()  # Create an instance of the MinimalPublisher class

    try:
        rclpy.spin(minimal_publisher)       # Keep the node active and processing callbacks until interrupted

    except KeyboardInterrupt:   # Handle a keyboard interrupt (Ctrl+C)
        print("\n")             # Print a newline for better format
        print("Stopping...")    # Print a stopping message
 
    finally:
        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        minimal_publisher.destroy_node()
        if rclpy.ok():                      # Check if the rclpy library is still running
            rclpy.shutdown()                # Shut down the ROS 2 client library, cleanly terminating the node



if __name__ == '__main__':
    main()                  # Call the main function to execute the code when the script is run