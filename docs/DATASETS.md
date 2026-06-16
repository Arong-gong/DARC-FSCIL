# Datasets and public split files

This repository does not redistribute raw images. It only provides public split
and index files needed to reproduce the degraded-support FSCIL protocol.

## mCURE-171

mCURE-171 is a curated 171-class pill-recognition benchmark derived from CURE
pill imagery. Place the prepared image directory as:

```text
data/mcure171/
  images/class_000/...
  images/class_001/...
```

Public split files:

```text
splits/mcure171/csv/
  base_train_all.csv
  incremental_support_5shot_seed2021_actual.csv
  query_strict_excluding_incremental_support_seed2021.csv
  session_classes.csv
splits/mcure171/cec/
  base_train.txt
  query_strict.txt
  session_1.txt ... session_8.txt
```

The paper-facing strict query contains 3720 clean images and excludes every
actual incremental support image. The strict-query SHA-256 is:

```text
4276424a4b69d8a453ebcb6097a72b3b7989ce50043ddb2da254fb625b8428fd
```

## Flowers102-FSCIL

Download Oxford Flowers102 from the official source and place images as:

```text
data/flowers102/flowers-102/jpg/image_00001.jpg
```

Public split files:

```text
splits/flowers102/csv/
  base_train_all.csv
  incremental_support_1shot_seed2021.csv
  incremental_support_3shot_seed2021.csv
  incremental_support_5shot_seed2021.csv
  query_all_test.csv
  session_classes.csv
splits/flowers102/cec/
  base_train.txt
  test.txt
  session_1.txt ... session_8.txt
```

The 1-shot and 3-shot files are deterministic subsets of the 5-shot support
manifest using the first K canonical support images per incremental class.

