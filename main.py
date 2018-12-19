from DummyAgent import DummyAgent


def main():
    # run command prosodyctl create freshagent@localhost and then type password 123456 twice
    dummy = DummyAgent("freshagent@localhost", "123456")
    dummy.start()


if __name__ == "__main__":
    main()
