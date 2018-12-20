from spade import agent


class UserAgent(agent.Agent):
    def setup(self):
        print('I\'m a user {}'.format(str(self.jid)))
