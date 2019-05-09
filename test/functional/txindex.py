#!/usr/bin/env python3
# Copyright (c) 2014-2015 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test txindex generation and fetching
#

import time
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import *
from test_framework.script import *
from test_framework.mininode import *
import binascii
from test_framework.blocktools import *
from test_framework.key import CECKey

class TxIndexTest(BitcoinTestFramework):

    def set_test_params(self):
        self.num_nodes = 4
        self.setup_clean_chain = True
        self.extra_args = [["-debug","-deprecatedrpc=signrawtransaction"],["-debug", "-txindex","-deprecatedrpc=signrawtransaction"],
                           ["-debug", "-txindex","-deprecatedrpc=signrawtransaction"], ["-debug", "-txindex","-deprecatedrpc=signrawtransaction"]]

    def setup_network(self):
        self.setup_nodes()

        # Nodes 0/1 are "wallet" nodes
        # Nodes 2/3 are used for testing
        connect_nodes(self.nodes[0], self.nodes[1])
        connect_nodes(self.nodes[0], self.nodes[2])
        connect_nodes(self.nodes[0], self.nodes[3])

        self.is_network_split = False
        self.sync_all()

    def run_test(self):
        print("Mining blocks...")
        self.nodes[0].generate(105)
        self.sync_all()

        chain_height = self.nodes[1].getblockcount()
        assert_equal(chain_height, 105)

        print("Testing transaction index...")

        privkey = "cSdkPxkAjA4HDr5VHgsebAPDEh9Gyub4HK8UJr2DFGGqKKy4K5sG"
        address = "mgY65WSfEmsyYaYPQaXhmXMeBhwp4EcsQW"
        addressHash = bytes([11,47,10,12,49,191,224,64,107,12,204,19,129,253,190,49,25,70,218,220])
        scriptPubKey = CScript([OP_DUP, OP_HASH160, addressHash, OP_EQUALVERIFY, OP_CHECKSIG])
        unspent = self.nodes[0].listunspent()
        tx = CTransaction()
        amount = int(unspent[0]["amount"] * 10000000)
        tx.vin = [CTxIn(COutPoint(int(unspent[0]["txid"], 16), unspent[0]["vout"]))]
        tx.vout = [CTxOut(amount, scriptPubKey)]
        tx.rehash()

        signed_tx = self.nodes[0].signrawtransaction(binascii.hexlify(tx.serialize()).decode("utf-8"))
        txid = self.nodes[0].sendrawtransaction(signed_tx["hex"], True)
        self.nodes[0].generate(1)
        self.sync_all()

        # Check verbose raw transaction results
        verbose = self.nodes[3].getrawtransaction(unspent[0]["txid"], 1)
        assert_equal(verbose["vout"][0]["valueSat"], 5000000000);
        assert_equal(verbose["vout"][0]["value"], 50);

        print("Passed\n")


if __name__ == '__main__':
    TxIndexTest().main()