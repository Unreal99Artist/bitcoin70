Bitcoin69 Core integration/staging tree
=====================================

To see how to run BTC69, please read the respective files in [the doc folder](doc)

What is Bitcoin69?
----------------

Bitcoin69 is a Meme coin created without a specific purpose, driven directly by the community, miners, investors.

# BTC69 Coin Information

- **Official Site:** [https://btc69.org](https://btc69.org)

## BTC69 Coin Specifications

- **P2P Port:** 6969
- **RPC Port:** 6970
- **Block Time:** 1 minute
- **Max Supply:** 69000000 BTC69 
- **Micro-Halving:** every 10 days (14400 blocks)


License
-------

Bitcoin69 Core is released under the terms of the MIT license. See [COPYING](COPYING) for more information or see https://opensource.org/licenses/MIT.

Development Process
-------------------

The `master` branch is regularly built and tested, but is not guaranteed to be
completely stable. [Tags](TODO) are created
regularly to indicate new official, stable release versions of BTC69 Core.

Active development is done in the `develop` branch.  *TODO

The contribution workflow is described in [CONTRIBUTING.md](CONTRIBUTING.md).

Please join us on discord in #development. https://discord.gg/XM296xQyXk

Testing
-------

Testing and code review is the bottleneck for development; we get more pull
requests than we can review and test on short notice. Please be patient and help out by testing
other people's pull requests, and remember this is a security-critical project where any mistake might cost people
lots of money.

Testnet is up and running and available to use during development.

### Automated Testing

Developers are strongly encouraged to write [unit tests](src/test/README.md) for new code, and to
submit new unit tests for old code. Unit tests can be compiled and run
(assuming they weren't disabled in configure) with: `make check`. Further details on running
and extending unit tests can be found in [/src/test/README.md](/src/test/README.md).

There are also [regression and integration tests](/test), written
in Python, that are run automatically on the build server.
These tests can be run (if the [test dependencies](/test) are installed) with: `test/functional/test_runner.py`


### Manual Quality Assurance (QA) Testing

Changes should be tested by somebody other than the developer who wrote the
code. This is especially important for large or high-risk changes. It is useful
to add a test plan to the pull request description if testing the changes is
not straightforward.



