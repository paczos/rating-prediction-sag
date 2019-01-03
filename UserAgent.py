from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import pandas as pd


class UserAgent(agent.Agent):
    def setup(self):
        self.add_behaviour(self.DispatchToReview())

        finish_template = Template()
        finish_template.set_metadata('performative', 'finish')
        self.add_behaviour(self.FinalResults(), finish_template)

    class DispatchToReview(OneShotBehaviour):
        async def run(self):
            msg = Message(to='rating@localhost')
            msg.set_metadata('performative', 'review')
            df = pd.read_csv('reviews.csv')
            msg.body = df.iloc[0, 1]
            await self.send(msg)

    class FinalResults(OneShotBehaviour):
        async def run(self):
            msg = await self.receive(20)
            if msg:
                print(
                    'final classification results are in thanks to this wonderful agent system I am using. The movie '
                    'got {} mark'.format(
                        msg.body))
