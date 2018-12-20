from aioxmpp import PresenceShow

from ClassifierAgent import ClassifierAgent
from RatingAgent import RatingAgent
from UserAgent import UserAgent

"""
In this code it is assumed that you have the following users in prosody
if you don't have these users, run:
sudo prosodyctl adduser <login> and then type <pass>

login: rating@localhost pass: rating

login: class0@localhost    pass: class
login: class1@localhost    pass: class
login: class2@localhost    pass: class
login: class3@localhost    pass: class
login: class4@localhost    pass: class

login: user@localhost      pass: user


 
"""


def main():
    user = UserAgent('user@localhost', 'user')
    user.start()
    user.web.start(hostname='localhost', port='10000')

    rating_agent = RatingAgent('rating@localhost', 'rating')
    rating_agent.start()
    rating_agent.web.start(hostname='localhost', port='10001')
    user.presence.subscribe('rating@localhost')

    classifier_agents = [ClassifierAgent('class{}'.format(i), 'class') for i in range(5)]
    for a in classifier_agents:
        rating_agent.presence.subscribe(str(a.jid))


if __name__ == "__main__":
    main()
