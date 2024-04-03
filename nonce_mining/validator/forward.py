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

from typing import List
import bittensor as bt
import torch

from nonce_mining.protocol import Dummy
from nonce_mining.validator.reward import get_rewards
from nonce_mining.utils.uids import get_random_uids


async def forward(self):
    """
    The forward function is called by the validator every time step.

    It is responsible for querying the network and scoring the responses.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the necessary state for the validator.

    """
    # Define how the validator selects a miner to query, how often, etc.
    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

    # The dendrite client queries the network.
    responses: List[int] = await self.dendrite(
        axons=[self.metagraph.axons[uid] for uid in miner_uids],
        synapse=Dummy(block_id=self.block),
        deserialize=True,
    )

    # Log the results for monitoring purposes.
    bt.logging.info(f"Received responses: {responses}")

    # Adjust the scores based on responses from miners.
    rewards = get_rewards(self, responses=responses)

    bt.logging.info(f"Scored responses: {rewards}")

    # Update the scores based on the rewards.
    self.update_scores(rewards, miner_uids)
