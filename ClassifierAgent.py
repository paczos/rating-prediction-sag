from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template


class ClassifierAgent(agent.Agent):
    def setup(self):
        print('Agent {} running'.format(self.name))
        classify_behav_template = Template()
        classify_behav_template.set_metadata('performative', 'classify')
        self.add_behaviour(self.Classify(), classify_behav_template)

    class Classify(OneShotBehaviour):
        async def run(self):
            rev_msg = await self.receive(10)
            if rev_msg:
                print('here the classifier runs {}'.format(self.agent.jid))
            else:
                print('no rev received')
