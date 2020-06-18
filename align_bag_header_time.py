#!/usr/bin/python
"""
Example:
    python align_bag_header_time.py -i 2020-06-12-14-24-36_lane_inhouse.bag
"""

import rospy
import rosbag
import os
import sys
import argparse

def align_offset(inbags):
  for inbag_name in inbags:
    outbag_name = "aligned-" + inbag_name
    rospy.loginfo('      Processing input bagfile: %s', inbag_name)
    rospy.loginfo('     Writing to output bagfile: %s', outbag_name)
    outbag = rosbag.Bag(outbag_name,'w')
    inbag = rosbag.Bag(inbag_name, 'r')
    bag_start_time = inbag.get_start_time()
    msg_start_time = None
    time_offset = None
    for topic, msg, t in inbag.read_messages():
      new_timestamp = t
      if msg._has_header:
        if not (msg_start_time and time_offset):
          msg_start_time = msg.header.stamp
          time_offset = rospy.rostime.Time.from_sec(bag_start_time) - msg_start_time
        new_timestamp = msg.header.stamp + time_offset
        msg.header.stamp = new_timestamp
      outbag.write(topic, msg, new_timestamp)
    outbag.close()


if __name__ == "__main__":
  rospy.init_node('aligh_bag_header_time')
  parser = argparse.ArgumentParser(description="Align header timestamps with bag start time")
  parser.add_argument('-i', metavar='BAGFILE', required=True, help='input bagfile(s)', nargs='+')
  args = parser.parse_args()
  try:
    align_offset(args.i)
  except Exception, e:
    import traceback
    traceback.print_exc()
