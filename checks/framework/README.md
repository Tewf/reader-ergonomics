# Framework

What every check is built on: the interface a check implements, the prose units the reading checks count, and the
judgment backends. Nothing here checks anything; every tier imports it, and it imports none of them.

<!-- checks:start -->
| File | Role |
|---|---|
| [check_api.py](check_api.py) | The interface every check shares: the files in scope, and the finding a check returns |
| [judgment.py](judgment.py) | Judgment: the questions a program cannot answer exactly, sent to the backend chosen in config |
| [prose.py](prose.py) | The units the reading checks count: the blocks of a markdown file, and the sentences of a paragraph |
<!-- checks:end -->
