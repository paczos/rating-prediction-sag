from spade import agent


class DummyAgent(agent.Agent):
    def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))



