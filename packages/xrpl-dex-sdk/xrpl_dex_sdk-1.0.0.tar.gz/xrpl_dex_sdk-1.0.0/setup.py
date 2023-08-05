# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xrpl_dex_sdk',
 'xrpl_dex_sdk.data',
 'xrpl_dex_sdk.methods',
 'xrpl_dex_sdk.models',
 'xrpl_dex_sdk.models.ccxt',
 'xrpl_dex_sdk.models.methods',
 'xrpl_dex_sdk.models.xrpl',
 'xrpl_dex_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'pytest>=7.1.3,<8.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'websockets>=10.3,<11.0',
 'xrpl-py>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'xrpl-dex-sdk',
    'version': '1.0.0',
    'description': 'Python SDK for interacting with the XRPL decentralized exchange',
    'long_description': '# XRPL Decentralized Exchange SDK\n\nThis Python SDK provides a [CCXT-compatible API](https://docs.ccxt.com/en/latest/manual.html?#unified-api) for interacting with the [XRPL decentralized exchange](https://xrpl.org/decentralized-exchange.html).\n\nA TypeScript version of this SDK is available [here](https://github.com/AktaryTech/xrpl-dex-sdk).\n\n## Installation\n\nThis package requires [Python v3.8](https://www.python.org/downloads/release/python-3810) (or newer) and the [Pip](https://pypi.org/project/pip/) package installer.\n\n### From PyPI\n\n1. Add the SDK as a dependency to your project:\n\n```\n$ pip install xrpl_dex_sdk\n```\n\n2. Import the SDK into your script:\n\n```python\nimport xrpl_dex_sdk\n```\n\n### From Source\n\n1. Make sure you have [Poetry](https://python-poetry.org/docs/) installed on your system.\n\n> NOTE: If you use VSCode, it should automatically show a prompt to select the virtual environment created by Poetry (`./.venv`). You will now have auto-formatting with `black`, linting with `flake8`, type-checking with `mypy`, and vscode testing configs.\n\n2. Clone the repo and install dependencies:\n\n```\n$ git clone https://github.com/AktaryTech/xrpl-dex-sdk-python.git\n$ cd xrpl-dex-sdk-python\n$ poetry install\n```\n\n## Usage\n\nTo use the SDK, import it into your script and initialize it:\n\n```python\nfrom xrpl_dex_sdk import SDK, SDKParams, constants\n\nsdk = SDK(SDKParams.from_dict({\n  "network": constants.TESTNET,\n  "generate_wallet": True,\n}))\n```\n\n### Currencies, MarketSymbols, and ID Formatting\n\nCurrency codes, market symbols (aka pairs), and Order/Trade IDs are strings that follow the following formats:\n\n| Type             | Format                           | Example                                       |\n| ---------------- | -------------------------------- | --------------------------------------------- |\n| CurrencyCode     | `[Currency]+[IssuerAddress]`     | `USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq`      |\n| MarketSymbol     | `[BaseCurrency]/[QuoteCurrency]` | `XRP/USD+rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq`  |\n| OrderId, TradeId | `[AccountAddress]/[Sequence]`    | `rpkeJcxB2y5BeAFyycuWwdTTcR3og2a3SR:30419065` |\n\n### Examples\n\n#### Placing an Order\n\nThe following example places an Order to buy 20 TST tokens, issued by the account at `rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd`, at a price of 1.5 XRP each:\n\n```python\nfrom xrpl_dex_sdk import SDK, SDKParams, constants, models\n\nsdk = SDK(SDKParams(\n  network=constants.TESTNET,\n  generate_wallet=True,\n))\n\ncreate_order_result = await sdk.create_order(\n    symbol="TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",\n    side=models.OrderSide.Buy,\n    type=models.OrderType.Limit,\n    amount=20,\n    price=1.5,\n)\n\norder = await sdk.fetch_order(create_order_result.id)\n\nprint(order)\n```\n\nOutputs the newly created Order object:\n\n```\n{\n  ...,\n  "status": "open",\n  "symbol": "TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",\n  "type": "limit",\n  "timeInForce": "GTC",\n  "side": "buy",\n  "amount": "20",\n  "price": "1.5",\n  "average": "0",\n  "filled": "0",\n  "remaining": "20",\n  "cost": "0",\n  "trades": [],\n  "info": {\n    // ... raw response from XRPL server\n  }\n}\n```\n\n#### Fetching an Order Book\n\nThe following example retrieves the latest order book for the market pair `TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP`:\n\n```python\nfrom xrpl_dex_sdk import SDK, SDKParams, constants, models\n\nsdk = SDK(SDKParams(\n  network=constants.TESTNET,\n  generate_wallet=True,\n))\n\norder_book = await sdk.fetch_order_book(\n    symbol="TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",\n    limit=5\n)\n\nprint(order_book)\n```\n\nOutputs an object like the following:\n\n```json\n{\n  "symbol": "TST+rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd/XRP",\n  "bids": [\n    ["0.0030627837459923", "93.030522464522"],\n    ["0.00302447007930511", "1"]\n  ],\n  "asks": [["331.133829801611", "0.3"]],\n  "info": {\n    // ... raw response from XRPL server\n  }\n}\n```\n\n## Methods\n\nFor full SDK documentation, load [`docs/_build/html/index.html`](docs/_build/html/index.html) in your browser. Run `docs/build.sh` to re-generate documentation.\n\n## Further Reading\n\n### CCXT (CryptoCurrency eXchange Trading Library)\n\n- [General Documentation](https://docs.ccxt.com/en/latest/index.html)\n- [Unified API](https://docs.ccxt.com/en/latest/manual.html#unified-api)\n\n### XRPL Ledger\n\n- [General Documentation](https://xrpl.org/concepts.html)\n- [Decentralized Exchange](https://xrpl.org/decentralized-exchange.html)\n- [dEX Tutorial](https://xrpl.org/trade-in-the-decentralized-exchange.html)\n\n## Contributing\n\nPull requests, issues and comments are welcome! Make sure to add tests for new features and bug fixes.\n\n## Contact\n\nFor questions, suggestions, etc, you can reach the maintainer at [info@aktarytech.com](mailto:info@aktarytech.com).\n\n## License\n\nThe software is distributed under the MIT license. See [LICENSE](https://github.com/AktaryTech/xrpl-dex-sdk-python/blob/main/LICENSE) for details.\n\nUnless you explicitly state otherwise, any contribution intentionally submitted for inclusion in this library by you, as defined in the MIT license, shall be licensed as above, without any additional terms or conditions.\n\n## Disclaimer\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n## Copyright\n\nCopyright © 2022 Ripple Labs, Inc.\n',
    'author': 'AktaryTech',
    'author_email': 'info@aktarytech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
