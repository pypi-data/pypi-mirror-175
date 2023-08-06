## datasets for tfrecords

## The update statement 
[usage:](https://github.com/ssbuild/fastdatasets-examples)  https://github.com/ssbuild/fastdatasets-examples
<br>
<font color='red'>2022-11-02: splict record for record and memory module </font>
<font color='red'>2022-10-29: add kv dataset </font>
<font color='red'>2022-10-19: update and modify for __all__ module</font>

## Install
```commandline
pip install -U fastdatasets
```


### 1. Record Write

```python
import data_serialize
from fastdatasets.record import load_dataset, gfile,TFRecordOptions, TFRecordCompressionType, TFRecordWriter

# 写二进制特征
def test_write_featrue():
    options = TFRecordOptions(compression_type=TFRecordCompressionType.NONE)

    def test_write(filename, N=3, context='aaa'):
        with TFRecordWriter(filename, options=options) as file_writer:
            for _ in range(N):
                val1 = data_serialize.Int64List(value=[1, 2, 3] * 20)
                val2 = data_serialize.FloatList(value=[1, 2, 3] * 20)
                val3 = data_serialize.BytesList(value=[b'The china', b'boy'])
                featrue = data_serialize.Features(feature=
                {
                    "item_0": data_serialize.Feature(int64_list=val1),
                    "item_1": data_serialize.Feature(float_list=val2),
                    "item_2": data_serialize.Feature(bytes_list=val3)
                }
                )
                example = data_serialize.Example(features=featrue)
                file_writer.write(example.SerializeToString())

    test_write('d:/example.tfrecords0', 3, 'file0')
    test_write('d:/example.tfrecords1', 10, 'file1')
    test_write('d:/example.tfrecords2', 12, 'file2')


# 写任意字符串
def test_write_string():
    options = TFRecordOptions(compression_type=TFRecordCompressionType.NONE)

    def test_write(filename, N=3, context='aaa'):
        with TFRecordWriter(filename, options=options) as file_writer:
            for _ in range(N):
                # x, y = np.random.random(), np.random.random()
                file_writer.write(context + '____' + str(_))

    test_write('d:/example.tfrecords0', 3, 'file0')
    test_write('d:/example.tfrecords1', 10, 'file1')
    test_write('d:/example.tfrecords2', 12, 'file2')



```

### 2. record Simple Writer Demo

```python
import pickle
import data_serialize
from fastdatasets.record import load_dataset, gfile,FeatureWriter, StringWriter, PickleWriter, DataType


def test_string(filename=r'd:\\example_writer.record0'):
    print('test_string ...')
    with StringWriter(filename) as writer:
        for i in range(2):
            writer.write(b'123')

    datasets = load_dataset.IterableDataset(filename)
    for i, d in enumerate(datasets):
        print(i, d)


def test_pickle(filename=r'd:\\example_writer.record1'):
    print('test_pickle ...')
    with PickleWriter(filename) as writer:
        for i in range(2):
            writer.write(b'test_pickle' + b'123')
    datasets = load_dataset.RandomDataset(filename)
    datasets = datasets.map(lambda x: pickle.loads(x))
    for i in range(len(datasets)):
        print(i, datasets[i])


def test_feature(filename=r'd:\\example_writer.record2'):
    print('test_feature ...')
    with FeatureWriter(filename) as writer:
        for i in range(3):
            feature = {
                'input_ids': {
                    'dtype': DataType.int64_list,
                    'data': list(range(i + 1))
                },
                'seg_ids': {
                    'dtype': DataType.float_list,
                    'data': [i, 0, 1, 2]
                },
                'other': {
                    'dtype': DataType.bytes_list,
                    'data': [b'aaa', b'bbbc1']
                },
            }
            writer.write(feature)

    datasets = load_dataset.RandomDataset(filename)
    for i in range(len(datasets)):
        example = data_serialize.Example()
        example.ParseFromString(datasets[i])
        feature = example.features.feature
        print(feature)


test_string()
test_pickle()
test_feature()

```

### 3. IterableDataset demo

```python
import data_serialize
from fastdatasets.record import load_dataset, gfile, RECORD

data_path = gfile.glob('d:/example.tfrecords*')
options = RECORD.TFRecordOptions(compression_type=None)
base_dataset = load_dataset.IterableDataset(data_path, cycle_length=1,
                                            block_length=1,
                                            buffer_size=128,
                                            options=options,
                                            with_share_memory=True)


def test_batch():
    num = 0
    for _ in base_dataset:
        num += 1
    print('base_dataset num', num)

    base_dataset.reset()
    ds = base_dataset.repeat(2).repeat(2).repeat(3).map(lambda x: x + bytes('_aaaaaaaaaaaaaa', encoding='utf-8'))
    num = 0
    for _ in ds:
        num += 1

    print('repeat(2).repeat(2).repeat(3) num ', num)


def test_torch():
    def filter_fn(x):
        if x == b'file2____2':
            return True
        return False

    base_dataset.reset()
    dataset = base_dataset.filter(filter_fn).interval(2, 0)
    i = 0
    for d in dataset:
        i += 1
        print(i, d)

    base_dataset.reset()
    dataset = base_dataset.batch(3)
    i = 0
    for d in dataset:
        i += 1
        print(i, d)

    # torch.utils.data.IterableDataset
    from fastdatasets.torch_dataset import IterableDataset
    dataset.reset()
    ds = IterableDataset(dataset=dataset)
    for d in ds:
        print(d)


def test_mutiprocess():
    print('mutiprocess 0...')
    base_dataset.reset()
    dataset = base_dataset.shard(num_shards=3, index=0)
    i = 0
    for d in dataset:
        i += 1
        print(i, d)

    print('mutiprocess 1...')
    base_dataset.reset()
    dataset = base_dataset.shard(num_shards=3, index=1)
    i = 0
    for d in dataset:
        i += 1
        print(i, d)

    print('mutiprocess 2...')
    base_dataset.reset()
    dataset = base_dataset.shard(num_shards=3, index=2)
    i = 0
    for d in dataset:
        i += 1
        print(i, d)

```



### 4. RandomDataset demo

```python
from fastdatasets.record import load_dataset, gfile, RECORD

data_path = gfile.glob('d:/example.tfrecords*')
options = RECORD.TFRecordOptions(compression_type=None)
dataset = load_dataset.RandomDataset(data_path, options=options,
                                     with_share_memory=True)

dataset = dataset.map(lambda x: x + b"adasdasdasd")
print(len(dataset))

for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('batch...')
dataset = dataset.batch(7)
for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('unbatch...')
dataset = dataset.unbatch()
for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('shuffle...')
dataset = dataset.shuffle(10)
for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('map...')
dataset = dataset.map(transform_fn=lambda x: x + b'aa22222222222222222222222222222')
for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('torch Dataset...')
from fastdatasets.torch_dataset import Dataset

d = Dataset(dataset)
for i in range(len(d)):
    print(i + 1, d[i])


```



### 5. leveldb dataset

```python
# @Time    : 2022/10/27 20:37
# @Author  : tk

from tqdm import tqdm
from fastdatasets.leveldb import DB,load_dataset,WriterObject,DataType,StringWriter,JsonWriter,FeatureWriter

db_path = 'd:\\example_leveldb'


def test_write(db_path):
    options = DB.LeveldbOptions(create_if_missing=True,error_if_exists=False)
    f = WriterObject(db_path, options = options)

    keys,values = [],[]
    n = 30
    for i in range(n):
        keys.append('input{}'.format(i))
        keys.append('label{}'.format(i))
        values.append(str(i))
        values.append(str(i))
        if (i+1) % 10000 == 0:
            f.file_writer.put_batch(keys,values)
            keys.clear()
            values.clear()
    if len(keys):
        f.file_writer.put_batch(keys, values)
        
    f.put('total_num',str(n))
    f.close()


def test_iterable(db_path):
    options = DB.LeveldbOptions(create_if_missing=False, error_if_exists=False)
    dataset = load_dataset.IterableDataset(db_path, options = options)
    for d in dataset:
        print(d)

def test_random(db_path):
    options = DB.LeveldbOptions(create_if_missing=False, error_if_exists=False)
    dataset = load_dataset.RandomDataset(db_path,
                                        data_key_prefix_list=('input','label'),
                                        num_key='total_num',
                                        options = options)

    dataset = dataset.shuffle(10)
    print(len(dataset))
    for i in tqdm(range(len(dataset)),total=len(dataset)):
        d = dataset[i]
        print(i,d)

test_write(db_path)
test_iterable(db_path)
test_random(db_path)

```


### 6. lmdb dataset

```python
# @Time    : 2022/10/27 20:37
# @Author  : tk


from tqdm import tqdm
from fastdatasets.lmdb import DB,load_dataset,WriterObject,DataType,StringWriter,JsonWriter,FeatureWriter

db_path = 'd:\\example_lmdb'


def test_write(db_path):
    options = DB.LmdbOptions(env_open_flag = 0,
                env_open_mode = 0o664, # 8进制表示
                txn_flag = 0,
                dbi_flag = 0,
                put_flag = 0)

    f = WriterObject(db_path, options = options,map_size=1024 * 1024 * 1024)

    keys, values = [], []
    n = 30
    for i in range(n):
        keys.append('input{}'.format(i))
        keys.append('label{}'.format(i))
        values.append(str(i))
        values.append(str(i))
        if (i + 1) % 10000 == 0:
            f.file_writer.put_batch(keys, values)
            keys.clear()
            values.clear()
    if len(keys):
        f.file_writer.put_batch(keys, values)

    f.put('total_num', str(n))
    f.close()


def test_iterable(db_path):
    options = DB.LmdbOptions(env_open_flag=DB.LmdbFlag.MDB_RDONLY,
                     env_open_mode=0o664,  # 8进制表示
                     txn_flag=0,
                     dbi_flag=0,
                     put_flag=0)
    dataset = load_dataset.IterableDataset(db_path,options = options)
    for d in dataset:
        print(d)

def test_random(db_path):
    options = DB.LmdbOptions(env_open_flag=DB.LmdbFlag.MDB_RDONLY,
                               env_open_mode=0o664,  # 8进制表示
                               txn_flag=0,
                               dbi_flag=0,
                               put_flag=0)
    dataset = load_dataset.RandomDataset(db_path,
                                        data_key_prefix_list=('input','label'),
                                        num_key='total_num',
                                        options = options)

    dataset = dataset.shuffle(10)
    print(len(dataset))
    for i in tqdm(range(len(dataset)),total=len(dataset)):
        d = dataset[i]
        print(i,d)

test_write(db_path)
test_iterable(db_path)
test_random(db_path)
```