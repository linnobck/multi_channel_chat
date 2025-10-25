Multi-user chat server
In this homework assignment you will implement a multi-user chat server using ZeroMQ.
You will also implement basic tests using Python’s pytest framework (https://docs.pytest.org/en/ stable/).
You will find an example test for Part 1 with the starter code for this assignment. You should implement
similar tests for each of the remaining parts.
The purpose of this assignment is to reinforce your understanding of different communication patterns. The
assignment includes four parts: first you will create a client/server pair for publishing messages to a chat
channel; you will then create a pub/sub mechanism for displaying the contents of the channel; next you will
integrate these two models to create an interactive, multi-user chat client/server; finally, you will create a
multi-channel client/server using topics to filter message.
