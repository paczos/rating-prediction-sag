import datetime
from statistics import mean

from spade import agent
from spade.behaviour import OneShotBehaviour, PeriodicBehaviour, TimeoutBehaviour
from spade.message import Message
from spade.template import Template

from nltk.tokenize import RegexpTokenizer

from consts import SCALE_RESOLUTION
import learning_func


class RatingAgent(agent.Agent):
    def __init__(self, jid, password, vectorizer):
        super().__init__(jid, password)
        self.classification_results = []
        self.vectorizer = vectorizer

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
        self.add_behaviour(
            self.SumUpClassification(start_at=datetime.datetime.now() + datetime.timedelta(seconds=18)))

    class SumUpClassification(TimeoutBehaviour):
        async def run(self):
            print('time to sum up classification')
            finish_msg = Message('rating@localhost')
            finish_msg.set_metadata('performative', 'finish')
            await self.send(finish_msg)
            print('no more classifiers')

    class ReceiveReview(OneShotBehaviour):
        async def run(self):
            review_msg = await self.receive(60)
            if review_msg:
                print('received a review: {}'.format(review_msg.body))
                for i in range(SCALE_RESOLUTION):
                    msg = Message(to='class{}@localhost'.format(i))
                    msg.set_metadata('performative', 'classify')
                    list1 = learning_func.prepare_review_text(review_msg.body, self.agent.vectorizer)
                    str1 = [','.join(item) for item in list1.astype(str)]
                    msg.body = str1[0]
                    await self.send(msg)
                    print('review passed to the classifier')

            else:
                print('RatingAgent: no review')

    class ReceiveClassification(PeriodicBehaviour):
        async def run(self):
            rating_msg = await self.receive(8)
            if rating_msg:
                print('wow, mark received from {} and the result is {}'.format(rating_msg.sender, rating_msg.body))
                tokenizer = RegexpTokenizer(r'\d')
                rate = tokenizer.tokenize(str(rating_msg.sender))
                rate = int(rate[0]) + 1
                self.agent.classification_results.append(float(rating_msg.body) * float(rate))
            else:
                print('Waited for classification agents, '
                      'but apparently some of them do not respond')

    class NotifyFinalResult(OneShotBehaviour):
        async def run(self):
            print('notify final result')
            res = await self.receive(30)
            if res:
                msg = Message(to='user@localhost')
                msg.set_metadata('performative', 'finish')
                print('{} agents returned their classifications. All classifications: {}'.format(
                    len(self.agent.classification_results),
                    str(self.agent.classification_results)))
                if len(list(filter(lambda x: x != 0, self.agent.classification_results))) == 0:
                    print('no ClassifierAgents returned results')
                else:
                    m = mean(filter(lambda x: x != 0, self.agent.classification_results)) - 1

                    print(m)
                    msg.body = str(m)
                    await self.send(msg)
            else:
                print('no accumulated results')

        async def on_end(self):
            self.agent.stop()
