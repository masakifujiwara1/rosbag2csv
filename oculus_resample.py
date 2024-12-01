import csv
from collections import defaultdict
import os

def resample_and_format_tf_data(csv_filepath, interval=0.4):
    """CSVデータをリサンプリングし、指定のフォーマットに変換する"""

    data = []
    with open(csv_filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    resampled_data = []
    current_time = 10  # 初期時間
    time_increment = 10
    last_timestamp = 0.0



    left_hand_data = defaultdict(lambda: {})  # 左手データ格納用
    right_hand_data = defaultdict(lambda: {}) # 右手データ格納用


    for row in data:

        timestamp = int(row['header.stamp.secs']) + int(row['header.stamp.nsecs']) * 1e-9

        if row['child_frame_id'] == 'LeftlHand Controller':
             left_hand_data[timestamp] = {'x': float(row['transform.translation.x']), 'y': float(row['transform.translation.y'])}
        elif row['child_frame_id'] == 'RightHand Controller':
            right_hand_data[timestamp] = {'x': float(row['transform.translation.x']), 'y': float(row['transform.translation.y'])}

    # リサンプリング処理
    sorted_timestamps = sorted(set(left_hand_data.keys()) | set(right_hand_data.keys())) #両方のキーをまとめてソート

    for timestamp in sorted_timestamps:

        if timestamp - last_timestamp >= interval or last_timestamp == 0:
            if timestamp in left_hand_data:
                resampled_data.append([current_time, 1, left_hand_data[timestamp]['x'], left_hand_data[timestamp]['y']])
            if timestamp in right_hand_data:
                resampled_data.append([current_time, 2, right_hand_data[timestamp]['x'], right_hand_data[timestamp]['y']])
            
            current_time += time_increment
            last_timestamp = timestamp


    return resampled_data

def convert_all_csvs(root_dir):
    """指定されたディレクトリ以下の全てのrosbagファイルをCSVに変換する関数"""
    for dirpath, _, filenames in os.walk(root_dir): # dirnames は未使用なので _ で受け取る
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_path = os.path.join(dirpath, filename)
                print(f"Converting: {csv_path}")
                resampled_data = resample_and_format_tf_data(csv_path)

                csv_filename = os.path.splitext(csv_path)[0] + "_resampled.csv"

                # CSVファイルへの書き出し
                with open(csv_filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["time", "id", "x", "y"]) # header
                    writer.writerows(resampled_data)

if __name__ == "__main__":
    root_dir = "/home/ubuntu/host_files/oculus_rosbag-20241201T114313Z-001/oculus_rosbag"

    convert_all_csvs(root_dir)
    print("Conversion complete.")



    print("リサンプリングとフォーマット変換が完了しました。結果が resampled_tf_data.csv に保存されました。")