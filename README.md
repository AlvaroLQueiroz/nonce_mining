
## Simple nonce mining


This project create nonce mining from bitcoing in a realllyyyyy simplified way using the BitTensor network.


---
- [Introduction](#introduction)
  - [Example](#example)
- [Installation](#installation)
  - [Before you proceed](#before-you-proceed)
  - [Install](#install)
- [License](#license)

---
## Introduction

**IMPORTANT**: If you are new to Bittensor subnets, read this section before proceeding to [Installation](#installation) section.

The Bittensor blockchain hosts multiple self-contained incentive mechanisms called **subnets**. Subnets are playing fields in which:
- Subnet miners who produce value, and
- Subnet validators who produce consensus

determine together the proper distribution of TAO for the purpose of incentivizing the creation of value, i.e., generating digital commodities, such as intelligence or data.

Each subnet consists of:
- Subnet miners and subnet validators.
- A protocol using which the subnet miners and subnet validators interact with one another. This protocol is part of the incentive mechanism.
- The Bittensor API using which the subnet miners and subnet validators interact with Bittensor's onchain consensus engine [Yuma Consensus](https://bittensor.com/documentation/validating/yuma-consensus). The Yuma Consensus is designed to drive these actors: subnet validators and subnet miners, into agreement on who is creating value and what that value is worth.

### Example

The Bittensor Subnet 1 for Text Prompting is built using this template. See [Bittensor Text-Prompting](https://github.com/opentensor/text-prompting) for how to configure the files and how to add monitoring and telemetry and support multiple miner types. Also see this Subnet 1 in action on [Taostats](https://taostats.io/subnets/netuid-1/) explorer.

---

## Installation

### Before you proceed
**IMPORTANT: It's not possible to run this subnet on bittensor mainnet/testnet.**

- You can run your subnet either as a subnet owner, or as a subnet validator or as a subnet miner.
- Make sure you are aware of the minimum compute requirements for your subnet. See the [Minimum compute YAML configuration](./min_compute.yml).

### Install

- **Running locally**: Follow the step-by-step instructions described in this section: [Running Subnet Locally](./docs/running_on_staging.md).


## License
This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
