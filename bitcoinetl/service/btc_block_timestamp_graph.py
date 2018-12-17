# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from bitcoinetl.domain.block import BtcBlock
from bitcoinetl.service.btc_service import BtcService
from blockchainetl.service.graph_operations import Point


class BlockTimestampGraph(object):
    def __init__(self, bitcoin_rpc):
        self._bitcoin_rpc = bitcoin_rpc
        self._btc_service = BtcService(bitcoin_rpc)

    def get_first_point(self):
        block_hash = self._bitcoin_rpc.getblockhash(0)
        block = self._bitcoin_rpc.getblock(block_hash)
        return block_to_point(block)

    def get_last_point(self):
        block_height = self._bitcoin_rpc.getblockcount()
        block_hash = self._bitcoin_rpc.getblockhash(block_height)
        block = self._bitcoin_rpc.getblock(block_hash)

        return block_to_point(block)

    def get_point(self, block_height):
        block_hash = self._bitcoin_rpc.getblockhash(block_height)
        block = self._bitcoin_rpc.getblock(block_hash)
        return block_to_point(block)

    def get_points(self, block_heights):
        blocks = self._btc_service.get_blocks(block_heights, with_transactions=False)
        return [block_to_point(block) for block in blocks]


def block_to_point(block):
    if isinstance(block, BtcBlock):
        return Point(block.height, block.time)
    else:
        return Point(block['height'], block["time"])
