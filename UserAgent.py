from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class UserAgent(agent.Agent):
    def setup(self):
        self.add_behaviour(self.DispatchToReview())

    class DispatchToReview(OneShotBehaviour):
        async def run(self):
            msg = Message(to='rating@localhost')
            msg.set_metadata('performative', 'review')
            # TODO: message body should be loaded from stdin or a file:
            msg.body = 'some review'
            await self.send(msg)
