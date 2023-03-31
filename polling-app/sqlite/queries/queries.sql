-- add user

INSERT INTO User(UserID, Username, HashedPass, AccessDate)
VALUES((SELECT MAX(UserID) + 1 FROM User user), aaa, bbb, ccc)

-- add option

INSERT INTO Option(PollID, OptionID, Content, Votes)
VALUES(aaa, bbb, ccc, 0);

-- add poll

INSERT INTO Poll(PollID, UserID, Content, DatePosted)
VALUES((SELECT MAX(PollID) + 1 FROM Poll poll), aaa, bbb, ccc);

-- add vote

INSERT INTO Vote(UserID, PollID, OptionID)
VALUES(aaa, bbb, ccc);
UPDATE Option
SET Votes = Votes + 1
WHERE PollID = bbb
AND OptionID = ccc;

-- delete poll

DELETE FROM Poll
WHERE PollID = aaa;
DELETE FROM Vote
WHERE PollID = aaa;
DELETE FROM Option
WHERE PollID = aaa;

-- delete vote

DELETE FROM Vote
WHERE PollID = aaa
AND OptionID = bbb
AND UserID = ccc;
UPDATE Option
SET Votes = Votes - 1
WHERE PollID = aaa
AND OptionID = bbb;

-- get user

SELECT * 
FROM User
WHERE Username = aaa;

-- get user polls

SELECT *
FROM Poll
WHERE UserID = aaa;

-- get option vote

SELECT Votes FROM Option
WHERE OptionID = aaa
AND PollID = bbb;

-- get total votes

SELECT COUNT(*) FROM Vote 
WHERE PollID = aaa;

-- get poll

SELECT * 
FROM Poll
WHERE PollID = aaa;

-- get lastrowid of Poll

SELECT MAX(PollID)
FROM Poll;

-- get poll options

SELECT *
FROM Option
WHERE PollID = aaa;

-- find user vote

SELECT *
FROM Vote
WHERE UserID = aaa
AND PollID = bbb;

-- reset votes

DELETE FROM Vote
WHERE UserID = aaa;

-- get all user votes

SELECT *
FROM Vote
WHERE UserID = aaa;

-- get max user id

SELECT MAX(UserID)
FROM User;

-- get user vote for poll

SELECT *
FROM Vote
WHERE UserID = aaa
AND PollID = bbb;

-- delete user

DELETE FROM User
WHERE UserID = aaa;

-- don't mind the weird order. i'm hoping to reorganize this at some point in the future.