from spade import agent


class ClassifierAgent(agent.Agent):
    def setup(self):
        print('Imma classifier agent {}'.format(str(self.jid)))
