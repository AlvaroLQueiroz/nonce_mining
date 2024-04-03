# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Alvaro L. S. Q. Mariano
# Copyright © 2023 Alvaro L. S. Q. Mariano

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


import time

# Bittensor
import bittensor as bt

# Bittensor Validator Template:
import nonce_mining
from nonce_mining.utils.hashing import gen_hash, gen_nonce
from nonce_mining.validator import forward

# import base validator class which takes care of most of the boilerplate
from nonce_mining.base.validator import BaseValidatorNeuron

class Validator(BaseValidatorNeuron):
    """
    This class inherits from the BaseValidatorNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class takes care of routine tasks such as setting up wallet, subtensor, metagraph, logging directory, parsing config, etc.
    This class provides reasonable default behavior for a validator such as keeping a moving average of the scores of the miners and using them to set weights at the end of each epoch. Additionally, the scores are reset for new hotkeys at the end of each epoch.
    """

    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()
        self.nonce_not_found: bool = True
        self.nonce: int = 0
        self.last_block: int|None = None

    async def forward(self):
        """
        Validator forward pass. Consists of:
        - Generating the nonce
        - Querying the miners
        - Getting the responses
        - Rewarding the miners
        - Updating the scores
        """

        # Generate a new nonce for a new block
        if self.last_block != self.block:
            nonce = gen_nonce()
            self.nonce_not_found = True
            self.nonce = int(gen_hash(nonce), 16)
            self.last_block = self.block
            bt.logging.info(f"Expected nonce: {self.nonce}")

        # If the nonce was found, don't make requests to the miners and wait a new block.
        if self.nonce_not_found:
            bt.logging.info(f"step({self.step}) block({self.block})")
            self.step += 1
            await forward(self)

        return

# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(5)
