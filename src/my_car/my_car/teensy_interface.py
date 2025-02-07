import rclpy
from rclpy.node import Node
import serial
import time

from std_msgs.msg import String  # Replace with appropriate ROS 2 messages (e.g., Float32, Int32, etc.)
from geometry_msgs.msg import Twist  # Example for robot movement commands

class TeensyInterfaceNode(Node):
    def __init__(self):
        super().__init__('teensy_interface')

        # Serial configuration
        self.serial_port = "/dev/ttyUSB0"  # Change to the correct port
        self.baud_rate = 115200  # Match with Teensy
        self.ser = None

        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for serial to initialize
            self.get_logger().info(f"Connected to Teensy on {self.serial_port}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to connect to serial: {e}")
            return

        # ROS 2 Publisher: Send received data from Teensy
        self.sensor_publisher = self.create_publisher(String, 'teensy_data', 10)

        # ROS 2 Subscriber: Receive commands from ROS 2 and send to Teensy
        self.command_subscriber = self.create_subscription(Twist, 'cmd_vel', self.command_callback, 10)

        # Timer for reading serial data
        self.create_timer(0.1, self.read_serial_data)

    def read_serial_data(self):
        """ Reads data from the Teensy and publishes it to a ROS 2 topic """
        if self.ser and self.ser.in_waiting > 0:
            try:
                data = self.ser.readline().decode('utf-8').strip()
                msg = String()
                msg.data = data
                self.sensor_publisher.publish(msg)
                self.get_logger().info(f"Received from Teensy: {data}")
            except Exception as e:
                self.get_logger().error(f"Error reading from serial: {e}")

    def command_callback(self, msg):
        """ Sends movement commands to the Teensy """
        try:
            cmd = f"{msg.linear.x},{msg.angular.z}\n"  # Example command format
            self.ser.write(cmd.encode('utf-8'))
            self.get_logger().info(f"Sent to Teensy: {cmd.strip()}")
        except Exception as e:
            self.get_logger().error(f"Error sending to serial: {e}")

    def destroy_node(self):
        """ Clean up before shutdown """
        if self.ser:
            self.ser.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = TeensyInterfaceNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
