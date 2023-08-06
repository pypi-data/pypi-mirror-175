This is the project to build a demo application for semantha's capabilities with streamlit.

## Usage:

Using the component is simple:

```python
from semantha_streamlit_compare.components.compare import SemanticCompare

compare = SemanticCompare()
compare.build_input(sentences=("First sentence", "Second sentence"))
```