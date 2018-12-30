import asyncio
from random import random

from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import learning_func
import numpy


class ClassifierAgent(agent.Agent):
    def __init__(self, jid, password, classifier):
        super().__init__(jid, password)
        self.classifier = classifier
        #self.vectorizer = vectorizer

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
                #await asyncio.sleep(random() * 3)
                #X = learning_func.prepare_review_text(rev_msg, self.agent.vectorizer)
                tmp = rev_msg.body.split(',')
                tmp = [int(i) for i in tmp]
                tmp = numpy.array([tmp])
                prediction = self.agent.classifier.predict(tmp)

                rating_msg = Message(to='rating@localhost')
                rating_msg.set_metadata('performative', 'mark')
                rating_msg.body = str(prediction[0])
                await self.send(rating_msg)

            else:
                print('no rev received')
