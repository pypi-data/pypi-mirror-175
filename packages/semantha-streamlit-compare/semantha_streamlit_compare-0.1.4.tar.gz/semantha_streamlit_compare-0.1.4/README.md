This project gives you an idea of how to use and build applications for streamlit. And all of this using semantha's native capabilities to process semantics in text.

tl;dr: using Streamlit, you can employ semantha's semantic comparison with just three lines of code (see below).

### Which Components Are Involved?
Streamlit.io offers easy GUI implementations. semantha.ai is a semantic processing platform which provides a REST/API for many use cases, end systems, etc.

![alt text](img/streamlit-compare-component.jpg "Streamlit Example")


## Setup, Secret, and API Key
To use semantha, you need to request a secrets.toml file. You can request that at support@thingsthinking.atlassian.net<br />
The file is structured as follows:
```
[semantha]
server_url="URL_TO_SERVER"
api_key="YOUR_API_KEY_ISSUED"
domain="USAGE_DOMAIN_PROVIDED_TO_YOU"
```


## Usage
Using the component is simple:

```python
from semantha_streamlit_compare.components.compare import SemanticCompare

compare = SemanticCompare()
compare.build_input(sentences=("First sentence", "Second sentence"))
```
