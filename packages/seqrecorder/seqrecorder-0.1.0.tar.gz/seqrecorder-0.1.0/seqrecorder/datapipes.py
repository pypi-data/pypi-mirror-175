"""Iterative datapipes built from seqrecord"""


from typing import Callable, Dict, List, Optional

import numpy as np
import torch
import torch.utils.data.datapipes as dp
from tqdm import tqdm

from .seqrecord import SeqRecord


class VideoDatapipeFromSeqRecord(dp.datapipe.IterDataPipe):
    """A torch datapiple class that iteratively read video(episode) segment from record files."""

    def __init__(
        self,
        record: SeqRecord,
        segment_len: int,
        features_rename: Dict[str, str],
        shuffle_recordfile: bool = False,
    ) -> None:
        super().__init__()
        self.segmentproto = record.get_proto4segment(segment_len, features_rename.keys())
        self.record = record
        self.features_rename = features_rename
        self.shuffle_recordfiles = shuffle_recordfile

    def __iter__(self):
        for segment in self.record.read_segments(self.segmentproto, shuffle_recordfile=self.shuffle_recordfiles):
            res = {}
            for feature in self.features_rename:
                res[self.features_rename[feature]]= segment[feature]
            yield res

class ItemDatapipeFromSeqRecord(dp.datapipe.IterDataPipe):
    """A torch datapiple class that iteratively read item (frame) from record files."""

    def __init__(
        self,
        record: SeqRecord,
        features_rename: Dict[str, str],
        shuffle_recordfiles: bool = False,
    ) -> None:
        super().__init__()
        self.record = record
        self.features_rename = features_rename
        self.shuffle_recordfiles = shuffle_recordfiles

    def __iter__(self):
        res = {}
        for item in self.record.read_items(
            features=self.features_rename.keys(), shuffle_recordfiles=self.shuffle_recordfiles
        ):
            res = {}
            for feature in self.features_rename:
                res[self.features_rename[feature]]= item[feature]
            yield res


def collate_fn(batch: List[Dict[str, np.ndarray]]) -> Dict[str, torch.Tensor]:
    collated_batch: Dict[str, torch.Tensor] = {}
    for feature in batch[0]:
        collated_batch[feature] = torch.from_numpy(
            np.stack([batch[i][feature] for i in range(len(batch))], axis=0)
        )
    return collated_batch


def list2array(data_list: Dict[str, List[np.ndarray]]) -> Dict[str, np.ndarray]:
    """transform data from list of np.array to a single numpy array. Only needed for video datapipes.
    Args:
        data_np (Dict[str, List[np.ndarray]]): _description_
    Returns:
        Dict[str, np.ndarray]: _description_
    """
    data_array: Dict[str, np.ndarray] = {}
    for feature in data_list:
        data_array[feature] = np.stack(data_list[feature], axis=0)
    return data_array


def build_datapipes(
    datapipe: dp.datapipe.IterDataPipe,
    shuffle_buffer_size: Optional[int],
    batch_size: int,
    mappings: List[Callable],
) -> dp.datapipe.IterDataPipe:
    """Iteratively apply operations to datapipe: shuffle, sharding, map, batch, collator

    Args:
        datapipe (dp.datapipe.IterDataPipe): entry datapipe
        shuffle_buffer_size (Optional[int]): buffer size for pseudo-shuffle
        batch_size (int):
        mappings (List[Callable]): a list of transforms applied to datapipe, between sharding and batch

    Returns:
        dp.datapipe.IterDataPipe: transformed datapipe ready to be sent to dataloader
    """
    # Shuffle will happen as long as you do NOT set `shuffle=False` later in the DataLoader
    # https://pytorch.org/data/main/tutorial.html#working-with-dataloader
    if shuffle_buffer_size is not None:
        datapipe = dp.iter.Shuffler(datapipe, buffer_size=shuffle_buffer_size)
    # sharding: Place ShardingFilter (datapipe.sharding_filter) as early as possible in the pipeline,
    # especially before expensive operations such as decoding, in order to avoid repeating these expensive operations across worker/distributed processes.
    datapipe = dp.iter.ShardingFilter(datapipe)
    for i, mapping in enumerate(mappings):
        datapipe = dp.iter.Mapper(datapipe, fn=mapping)
    # Note that if you choose to use Batcher while setting batch_size > 1 for DataLoader,
    # your samples will be batched more than once. You should choose one or the other.
    # https://pytorch.org/data/main/tutorial.html#working-with-dataloader
    datapipe = dp.iter.Batcher(datapipe, batch_size=batch_size, drop_last=True)
    datapipe = dp.iter.Collator(datapipe, collate_fn=collate_fn)
    return datapipe
