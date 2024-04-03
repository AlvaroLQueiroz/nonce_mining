# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Alvaro L. S. Q. Mariano
# Copyright © 2023 # Alvaro L. S. Q. Mariano

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
import typing
import bittensor as bt

# Bittensor Miner Template:
import nonce_mining

# import base miner class which takes care of most of the boilerplate
from nonce_mining.base.miner import BaseMinerNeuron
from nonce_mining.utils.hashing import gen_hash, gen_nonce


class Miner(BaseMinerNeuron):
    """
    This class inherits from the BaseMinerNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class takes care of routine tasks such as setting up wallet, subtensor, metagraph, logging directory, parsing config, etc.
    This class provides reasonable default behavior for a miner such as blacklisting unrecognized hotkeys, prioritizing requests based on stake, and forwarding requests to the forward function.
    """

    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)
        self.nonces: set[str] = set()
        self.last_block_id: int|None = None
        self.extra_attempts = 10
        self.still_trying = True

    async def forward(
        self, synapse: nonce_mining.protocol.Dummy
    ) -> nonce_mining.protocol.Dummy:
        """
        Processes the incoming 'Dummy' synapse by performing a predefined operation on the input data.

        Args:
            synapse (template.protocol.Dummy): The synapse object containing the 'block_id' data.

        Returns:
            template.protocol.Dummy: The synapse object with the 'hash' field set with a random nonce value hashed.
        """

        # Reset the state for new block's
        if synapse.block_id != self.last_block_id:
            self.last_block_id = synapse.block_id
            self.still_trying = True
            self.nonces.clear()

        # Stop execution if max attempts has reached
        if not self.still_trying:
            return synapse

        # Generates a nonce until this is new and not used.
        nonce = gen_nonce()
        attempts = 0
        while nonce in self.nonces:
            nonce = gen_nonce()
            attempts += 1
            if attempts > len(self.nonces) + self.extra_attempts:
                self.still_trying = False
                bt.logging.warning(f"Max number of attempts ({self.extra_attempts}) reached for the block: {synapse.block_id}")
                return synapse

        self.nonces.add(nonce)
        nonce = int(gen_hash(nonce), 16)
        synapse.hash = nonce
        bt.logging.info(f"Synapse block: {synapse.block_id}, Step {self.step}, Generated nonce: {nonce}")
        return synapse

    async def blacklist(
        self, synapse: nonce_mining.protocol.Dummy
    ) -> typing.Tuple[bool, str]:
        """
        Determines whether an incoming request should be blacklisted and thus ignored. Y

        Blacklist runs before the synapse data has been deserialized (i.e. before synapse.data is available).
        The synapse is instead contructed via the headers of the request. It is important to blacklist
        requests before they are deserialized to avoid wasting resources on requests that will be ignored.

        Args:
            synapse (template.protocol.Dummy): A synapse object constructed from the headers of the incoming request.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating whether the synapse's hotkey is blacklisted,
                            and a string providing the reason for the decision.

        This function is a security measure to prevent resource wastage on undesired requests. It should be enhanced
        to include checks against the metagraph for entity registration, validator status, and sufficient stake
        before deserialization of synapse data to minimize processing overhead.
        """

        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            # Ignore requests from un-registered entities.
            bt.logging.trace(
                f"Blacklisting un-registered hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        if self.config.blacklist.force_validator_permit:
            # If the config is set to force validator permit, then we should only allow requests from validators.
            if not self.metagraph.validator_permit[uid]:
                bt.logging.warning(
                    f"Blacklisting a request from non-validator hotkey {synapse.dendrite.hotkey}"
                )
                return True, "Non-validator hotkey"

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"

    async def priority(self, synapse: nonce_mining.protocol.Dummy) -> float:
        """
        The priority function determines the order in which requests are handled. More valuable or higher-priority
        requests are processed before others.

        This implementation assigns priority to incoming requests based on the calling entity's stake in the metagraph.

        Args:
            synapse (template.protocol.Dummy): The synapse object that contains metadata about the incoming request.

        Returns:
            float: A priority score derived from the stake of the calling entity.
        """

        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )  # Get the caller index.
        prirority = float(
            self.metagraph.S[caller_uid]
        )  # Return the stake as the priority.
        bt.logging.trace(
            f"Prioritizing {synapse.dendrite.hotkey} with value: ", prirority
        )
        return prirority

    def save_state(self):
        pass

    def load_state(self):
        pass

# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)