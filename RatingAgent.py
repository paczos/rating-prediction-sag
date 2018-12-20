from statistics import mean

from spade import agent
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template

from consts import SCALE_RESOLUTION


class RatingAgent(agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.classification_results = []

    def setup(self):
        print('I am a rating agent')
        review_template = Template()
        review_template.set_metadata('performative', 'review')
        self.add_behaviour(self.ReceiveReview(), review_template)

        classification_template = Template()
        classification_template.set_metadata('performative', 'mark')
        self.add_behaviour(self.ReceiveClassification(period=1), classification_template)

        final_result_template = Template()
        final_result_template.set_metadata('performative', 'finish')
        self.add_behaviour(self.NotifyFinalResult(), final_result_template)

    class ReceiveReview(OneShotBehaviour):
        async def run(self):
            review_msg = await self.receive(60)
            if review_msg:
                print('received a review: {}'.format(review_msg.body))
                for i in range(SCALE_RESOLUTION):
                    msg = Message(to='class{}@localhost'.format(i))
                    msg.set_metadata('performative', 'classify')
                    msg.body = review_msg.body
                    await self.send(msg)
                    print('review passed to the classifier')

            else:
                print('ratingagent: no review')

    class ReceiveClassification(PeriodicBehaviour):
        async def run(self):
            if len(self.agent.classification_results) == SCALE_RESOLUTION:
                finish_msg = Message('rating@localhost')
                finish_msg.set_metadata('performative', 'finish')
                await self.send(finish_msg)
                print('no more classifiers')
                self.kill()
            rating_msg = await self.receive(20)
            if rating_msg:
                print('wow, mark received from {} and the result is {}'.format(rating_msg.sender, rating_msg.body))
                self.agent.classification_results.append(float(rating_msg.body))
            else:
                print('so loooong, MARIANNEEE! Classification timeout')

    class NotifyFinalResult(OneShotBehaviour):
        async def run(self):
            print('notify final result')
            res = await self.receive(30)
            if res:
                msg = Message(to='user@localhost')
                msg.set_metadata('performative', 'finish')
                print(self.agent.classification_results)
                m = mean(self.agent.classification_results)
                print(m)
                msg.body = str(m)
                await self.send(msg)
            else:
                print('no accumulated results')
