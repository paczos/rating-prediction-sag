import numpy
from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from random import randint

class ClassifierAgent(agent.Agent):
    def __init__(self, jid, password, classifier):
        super().__init__(jid, password)
        self.classifier = classifier

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

                if randint(0, 3) > 1:
                    print('unlucky agent, stop him')
                    self.agent.stop()
                    self.kill()
                else:
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
