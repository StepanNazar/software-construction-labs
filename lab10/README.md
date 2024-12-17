# PNU 2024 KPZ lab10 Stepan Nazar

This is a laboratory work №10 for the subject Software Construction.

# Usage

You can run main module of package, which is an argparse application.
    
```bash
python -m pnu_2024_kpz_lab10_stepan_nazar.main -h
```

Output:

```plaintext
usage: main.py [-h] [strings ...]

Reverse words in strings. No arguments will read from stdin.

positional arguments:
  strings     Strings to reverse.

options:
  -h, --help  show this help message and exit
```

or you can use string_utils module inside your code.

```python
from pnu_2024_kpz_lab10_stepan_nazar import string_utils
print(string_utils.reverse_words_in_string("Hello, world!"))
```

Output:

```plaintext
olleH, dlrow!
```
