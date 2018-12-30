import time

from spade.message import Message

from ClassifierAgent import ClassifierAgent
from RatingAgent import RatingAgent
from UserAgent import UserAgent
from consts import SCALE_RESOLUTION
import learning_func

"""
In this code it is assumed that you have the following users in prosody
if you don't have these users, run:
sudo prosodyctl adduser <login> and then type <pass>

login: rating@localhost pass: rating

login: class0@localhost    pass: class
login: class1@localhost    pass: class
login: class2@localhost    pass: class
login: class3@localhost    pass: class

login: user@localhost      pass: user
"""


def main():
    classifier, vectorizer = learning_func.train_classifiers( 'bayes', 'data.csv' )
    user = UserAgent('user@localhost', 'user')
    rating_agent = RatingAgent('rating@localhost', 'rating', vectorizer)
    rating_agent.start()
    rating_agent.web.start(hostname='localhost', port='10001')

    classifier_agents = [ClassifierAgent('class{}@localhost'.format(i), 'class', classifier[i]) for i in range(SCALE_RESOLUTION)]
    for agent in classifier_agents:
        rating_agent.presence.subscribe(str(agent.jid))
        agent.start()

    msg = Message(to='rating@localhost')
    msg.set_metadata('performative', 'inform')
    msg.body = 'a review'

    time.sleep(1)
    user.start()
    user.web.start(hostname='localhost', port='10000')


if __name__ == '__main__':
    main()
