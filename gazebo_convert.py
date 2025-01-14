import rosbag
import csv
import os
from gazebo_msgs.msg import ModelStates

def extract_model_states_data(msg):
    """gazebo_msgs/ModelStates からデータ行を抽出するヘルパー関数"""
    for i, name in enumerate(msg.name):
        yield [
            msg.header.seq,
            msg.header.stamp.secs,
            msg.header.stamp.nsecs,
            name,
            msg.pose[i].position.x,
            msg.pose[i].position.y,
            msg.pose[i].position.z,
            msg.pose[i].orientation.x,
            msg.pose[i].orientation.y,
            msg.pose[i].orientation.z,
            msg.pose[i].orientation.w,
            msg.twist[i].linear.x,
            msg.twist[i].linear.y,
            msg.twist[i].linear.z,
            msg.twist[i].angular.x,
            msg.twist[i].angular.y,
            msg.twist[i].angular.z,
        ]

def rosbag_to_csv(rosbag_path, topic_name="/gazebo/model_states", header=None):
    """rosbagファイルをCSVファイルに変換する関数"""
    csv_filename = os.path.splitext(rosbag_path)[0] + ".csv"

    if header is None:
        header = [
            "header.seq", "header.stamp.secs", "header.stamp.nsecs", "name",
            "pose.position.x", "pose.position.y", "pose.position.z",
            "pose.orientation.x", "pose.orientation.y", "pose.orientation.z", "pose.orientation.w",
            "twist.linear.x", "twist.linear.y", "twist.linear.z",
            "twist.angular.x", "twist.angular.y", "twist.angular.z"
        ]
    
    try:
        with rosbag.Bag(rosbag_path, 'r') as bag:
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)

                for _, msg, _ in bag.read_messages(topics=[topic_name]):
                    for row in extract_model_states_data(msg):
                        writer.writerow(row)

    except rosbag.bag.ROSBagUnindexedException:
        print(f"Error: '{rosbag_path}' はインデックスされていません。`rosbag reindex {rosbag_path}` を実行してください。")

def convert_all_rosbags(root_dir, topic_name="/gazebo/model_states", header=None):
    """指定されたディレクトリ以下の全てのrosbagファイルをCSVに変換する関数"""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".bag"):
                rosbag_path = os.path.join(dirpath, filename)
                print(f"Converting: {rosbag_path}")
                rosbag_to_csv(rosbag_path, topic_name, header)

if __name__ == "__main__":
    root_dir = "/home/ubuntu/host_files/oculus_rosbag-20241201T114313Z-001/oculus_rosbag"
    topic_name = "/gazebo/model_states"

    convert_all_rosbags(root_dir, topic_name)
    print("Conversion complete.")