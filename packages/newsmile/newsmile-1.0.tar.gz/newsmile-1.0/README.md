# NewSmile
## Another Smile Format Decoder/Encoder for Python 3

### Decoding example
```python
from newsmile import SmileDecoder
decoder = SmileDecoder()
with open('smile-data-file', 'rb') as smile_file:
    data = decoder.decode(smile_file.read())
```

### Encoding example
```python
import json
from newsmile import SmileEncoder
encoder = SmileEncoder(shared_values=True, encoding='iso-8859-1')
dico = {'a': 1, 'b': [2, 3, 4], 'c': {'subkey': 'a string'}}
smile_data = encoder.encode(json.dumps(dico))
```

### Running tests
```bash
cd tests
```
```python
python test.py
```
