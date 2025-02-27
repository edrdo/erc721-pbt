import pytest
from erc721_pbt import StateMachine, Options
from brownie import TokenReceiver

@pytest.fixture()
def contract2test(NFToken):
    yield NFToken


class NFToken(StateMachine):
    def __init__(self, accounts, contract2test):
        wallets = list()
        for i in range(0, Options.ACCOUNTS):
            tr = TokenReceiver.deploy({"from": accounts[i] })
            wallets.append(tr.address)
        contract = contract2test.deploy({"from": wallets[0]})
        super().__init__(self, wallets, contract)

    def onSetup(self):
        for tokenId in range(1, Options.TOKENS + 1):
            account = tokenId % Options.ACCOUNTS
            address = self.wallets[account]
            self.contract.mintToken(tokenId, address, { "from": self.wallets[0] } )
            self.owner[tokenId] = account
            self.balance[account] = self.balance.get(account, 0) + 1

def test_stateful(contract2test, accounts, state_machine):
    state_machine(NFToken, accounts, contract2test)
