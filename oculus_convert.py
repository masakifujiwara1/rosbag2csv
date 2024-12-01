import rosbag
import csv
import os

def extract_tf_data(msg):
    """tf2_msgs/TFMessage からデータ行を抽出するヘルパー関数"""
    for transform in msg.transforms:
        yield [
            transform.header.seq,
            transform.header.stamp.secs,
            transform.header.stamp.nsecs,
            transform.header.frame_id,
            transform.child_frame_id,
            transform.transform.translation.x,
            transform.transform.translation.y,
            transform.transform.translation.z,
            transform.transform.rotation.x,
            transform.transform.rotation.y,
            transform.transform.rotation.z,
            transform.transform.rotation.w,
        ]

def rosbag_to_csv(rosbag_path, topic_name="/tf", header=None):
    """rosbagファイルをCSVファイルに変換する関数"""
    csv_filename = os.path.splitext(rosbag_path)[0] + ".csv"

    if header is None:
        header = ["header.seq", "header.stamp.secs", "header.stamp.nsecs", "header.frame_id", "child_frame_id", "transform.translation.x", "transform.translation.y", "transform.translation.z", "transform.rotation.x", "transform.rotation.y", "transform.rotation.z", "transform.rotation.w"]
    
    try:
        with rosbag.Bag(rosbag_path, 'r') as bag:
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)

                for _, msg, _ in bag.read_messages(topics=[topic_name]): # topic, t は未使用なので _ で受け取る
                     if topic_name == '/tf': # topic_nameによる条件分岐
                        for row in extract_tf_data(msg):
                            writer.writerow(row)


    except rosbag.bag.ROSBagUnindexedException:
        print(f"Error: '{rosbag_path}' はインデックスされていません。`rosbag reindex {rosbag_path}` を実行してください。")

def convert_all_rosbags(root_dir, topic_name="/tf", header=None):
    """指定されたディレクトリ以下の全てのrosbagファイルをCSVに変換する関数"""
    for dirpath, _, filenames in os.walk(root_dir): # dirnames は未使用なので _ で受け取る
        for filename in filenames:
            if filename.endswith(".bag"):
                rosbag_path = os.path.join(dirpath, filename)
                print(f"Converting: {rosbag_path}")
                rosbag_to_csv(rosbag_path, topic_name, header)

if __name__ == "__main__":
    root_dir = "/home/ubuntu/host_files/oculus_rosbag-20241201T114313Z-001/oculus_rosbag"
    topic_name = "/tf"

    convert_all_rosbags(root_dir, topic_name)
    print("Conversion complete.")