import asyncio
from random import random

from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template


class ClassifierAgent(agent.Agent):
    def setup(self):
        print('Agent {} running'.format(self.name))
        classify_template = Template()
        classify_template.set_metadata('performative', 'classify')
        self.add_behaviour(self.Classify(), classify_template)

    class Classify(OneShotBehaviour):
        async def run(self):
            rev_msg = await self.receive(10)
            if rev_msg:
                print('here the classifier runs {}'.format(self.agent.jid))

                # TODO: sleep() here simulates the classifier
                await asyncio.sleep(random() * 3)

                rating_msg = Message(to='rating@localhost')
                rating_msg.set_metadata('performative', 'mark')
                rating_msg.body = str(random() * 4)
                await self.send(rating_msg)

            else:
                print('no rev received')
