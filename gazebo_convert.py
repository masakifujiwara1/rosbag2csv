import rosbag
import csv
import os

# ルートディレクトリのパスを設定
root_dir = '/path/to/root/directory'

# ルートディレクトリ内の全ての.bagファイルを取得
bag_files = [f for f in os.listdir(root_dir) if f.endswith('.bag')]

for bag_file in bag_files:
    bag_path = os.path.join(root_dir, bag_file)
    base_name = os.path.splitext(bag_file)[0]
    csv_file = os.path.join(root_dir, base_name + '.csv')
    
    with rosbag.Bag(bag_path, 'r') as bag, open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['time', 'id', 'x', 'y'])
        
        last_write_time = None
        interval = 0.4  # 0.4秒間隔
    
        for topic, msg, t in bag.read_messages(topics=['/gazebo/model_states']):
            current_time = t.to_sec()
            if last_write_time is None or current_time - last_write_time >= interval:
                try:
                    model_names = msg.name
                    robot_idx = model_names.index('orne_box')
                    actor2_idx = model_names.index('actor2')
                    if 'actor1' in model_names:
                        actor1_idx = model_names.index('actor1')
                        csv_writer.writerow([f"{current_time:.6f}", 3, msg.pose[actor1_idx].position.x, msg.pose[actor1_idx].position.y])
    
                    csv_writer.writerow([f"{current_time:.6f}", 2, msg.pose[robot_idx].position.x, msg.pose[robot_idx].position.y])
                    csv_writer.writerow([f"{current_time:.6f}", 1, msg.pose[actor2_idx].position.x, msg.pose[actor2_idx].position.y])
                    last_write_time = current_time
                except AttributeError:
                    print(f"メッセージに 'x' または 'y' 属性が存在しません: {msg}")

    print(f"データが {csv_file} に正常に書き込まれました。")
