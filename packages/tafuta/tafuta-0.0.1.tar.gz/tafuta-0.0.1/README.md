# tafuta
This is a simple program that computes hamming distance between two DNA sequences, generates reverse complement of a sequence, determines naive exact matching and naive with mismatch of a pattern in a sequence together with the pattern's reverse complements.

![PAKA](https://myoctocat.com/assets/images/base-octocat.svg) 

## installation
tafuta_pattern can be installed as follows:

```
pip install tafuta
```

## Usage
### For computation of hamming distances between the two sequences
```
from tafuta import paka
paka.hamming_dist(S1,S2)
```

### For determining reverse complement of a sequence
```
from tafuta import paka
paka.reverse_complement (S)
```
### For determining pattern matching positions in a sequence with naive exact matching
```
from tafuta import paka
paka.naive_exact_match (sequence,pattern)
```
### For determining pattern matching positions in a sequence with naive with mismatch together with reverse complement of a pattern
```
from tafuta import paka
paka.naive_with_mismatch (sequence,pattern)
```