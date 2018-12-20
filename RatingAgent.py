from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from consts import SCALE_RESOLUTION


class RatingAgent(agent.Agent):
    def setup(self):
        print('Imma rating agent')
        template = Template()
        template.set_metadata('performative', 'review')
        print(template)

        self.add_behaviour(self.ReceiveReview(), template)

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
                print('no review')
