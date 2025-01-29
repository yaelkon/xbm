import os
import pandas as pd
import shutil

from tqdm import tqdm

# Function to organize CelebA dataset into train, validation, and test sets
def organize_celebA_data(data_dir, output_dir):
      # Read the partition file
      partition_file = os.path.join(data_dir, 'list_eval_partition.csv')
      partitions = pd.read_csv(partition_file)

      # Create directories for train, validation, and test sets
      train_dir = os.path.join(output_dir, 'train')
      val_dir = os.path.join(output_dir, 'val')
      test_dir = os.path.join(output_dir, 'test')
      os.makedirs(train_dir, exist_ok=True)
      os.makedirs(val_dir, exist_ok=True)
      os.makedirs(test_dir, exist_ok=True)

      # Move images to respective directories
      for _, row in partitions.iterrows():
            img_name = row['image_id']
            partition = row['partition']
            src_path = os.path.join(data_dir, 'img_align_celeba', img_name)
            
            if partition == 0:
                  dst_path = os.path.join(train_dir, img_name)
            elif partition == 1:
                  dst_path = os.path.join(val_dir, img_name)
            elif partition == 2:
                  dst_path = os.path.join(test_dir, img_name)
            else:
                  raise ValueError('Partition value must be 0, 1, or 2')
                  
            shutil.move(src_path, dst_path)

def organize_celebA_to_ImageFolder(data_dir, output_dir, output_attribute='Blond_Hair'):
      # Read the attributes file
      attributes_file = os.path.join(data_dir, 'list_attr_celeba.csv')
      attributes = pd.read_csv(attributes_file)

      # Read the partition file
      partition_file = os.path.join(data_dir, 'list_eval_partition.csv')
      partitions = pd.read_csv(partition_file)

      # Create directories for train, validation, and test sets
      train_dir = os.path.join(output_dir, 'train')
      val_dir = os.path.join(output_dir, 'val')
      test_dir = os.path.join(output_dir, 'test')
      
      os.makedirs(train_dir, exist_ok=True)
      os.makedirs(val_dir, exist_ok=True)
      os.makedirs(test_dir, exist_ok=True)

      # Create directories for positive and negative examples of the attribute
      os.makedirs(os.path.join(train_dir, output_attribute), exist_ok=True)
      os.makedirs(os.path.join(train_dir, 'no_' + output_attribute), exist_ok=True)
      os.makedirs(os.path.join(val_dir, output_attribute), exist_ok=True)
      os.makedirs(os.path.join(val_dir, 'no_' + output_attribute), exist_ok=True)
      os.makedirs(os.path.join(test_dir, output_attribute), exist_ok=True)
      os.makedirs(os.path.join(test_dir, 'no_' + output_attribute), exist_ok=True)

      # Copy images to respective directories
      for _, row in tqdm(attributes.iterrows(), total=len(attributes)):
            img_name = row['image_id']
            attribute = row[output_attribute]
            partition = int(partitions[partitions['image_id'] == img_name]['partition'])
            
            if partition == 0:
                  src_path = os.path.join(data_dir, "train", img_name)
                  if attribute == 1:
                        dst_path = os.path.join(train_dir, output_attribute, img_name)
                  else:
                        dst_path = os.path.join(train_dir, 'no_' + output_attribute, img_name)
            
            elif partition == 1:
                  src_path = os.path.join(data_dir, "val", img_name)
                  if attribute == 1:
                        dst_path = os.path.join(val_dir, output_attribute, img_name)
                  else:
                        dst_path = os.path.join(val_dir, 'no_' + output_attribute, img_name)
            
            elif partition == 2:
                  src_path = os.path.join(data_dir, "test", img_name)
                  if attribute == 1:
                        dst_path = os.path.join(test_dir, output_attribute, img_name)
                  else:
                        dst_path = os.path.join(test_dir, 'no_' + output_attribute, img_name)
            else:
                  raise ValueError('Partition value must be 0, 1, or 2')
                  
            shutil.copy(src_path, dst_path)


if __name__ == '__main__':
      executable_function = 'organize_celebA_to_ImageFolder'

      data_dir = '/home/yk449/datasets/CelebA'

      if executable_function == 'organize_celebA_data':
            output_dir = '/home/yk449/datasets/CelebA'
            organize_celebA_data(data_dir, output_dir)
      
      elif executable_function == 'organize_celebA_to_ImageFolder':
            output_dir = '/home/yk449/python_projects/xbm/data/CelebA'
            organize_celebA_to_ImageFolder(data_dir, output_dir)
