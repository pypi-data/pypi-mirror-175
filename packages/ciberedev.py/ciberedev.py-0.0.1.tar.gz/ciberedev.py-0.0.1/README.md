<h1>ciberedev.py</h1>
<p>Python Wrapper for <a href="https://www.cibere.dev">cibere.dev</a></p>

<h2>Installing</h2>
<span style="font-weight: bold;">Python 3.8 or higher is required</span>
Install from pip

```
python -m pip install -U ciberedev.py
```

Install from github

```bash
python -m pip install -U https://github.com/cibere/ciberedev.py # requires git to be installed
```

<h2>Examples</h2>
Create Paste Example

```py
import asyncio
import ciberedev

client = ciberedev.Client()

async def main():
  async with client:
    paste = await client.create_paste("my_paste_text")
    print(paste.url)

if __name__ == "__main__":
  asyncio.run(main())
```

See <a href="https://github.com/cibere/ciberedev.py/tree/main/examples">the examples folder</a> for a full list of examples
