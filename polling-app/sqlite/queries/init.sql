-- Some sample accounts and polls!

-- Author : Marcus Antonelli
-- CODE FOO IGN CHALLENGE

CREATE TABLE Poll(
    PollID INT NOT NULL, 
    UserID INT NOT NULL,
    Content varchar(255) NOT NULL,
    DatePosted DATE NOT NULL,
    PRIMARY KEY (PollID)
);

INSERT INTO Poll (PollID, UserID, Content, DatePosted)
VALUES
    (1, 1, "Which city would you rather live in?", DATE('2022-10-17')),
    (2, 1, "What's your favorite color?", DATE('2022-12-12')),
    (3, 2, "What's your favorite programming language?", DATE('2023-01-17')),
    (4, 1, "Which social media platform is the best?", DATE('2023-02-24')), 
    (5, 3, "Which altcoin would you consider buying?", DATE('2023-02-27')), 
    (6, 2, "Have you ever played a game by Blizzard?", DATE('2023-03-08')), 
    (7, 4, "How many employees does your workplace have?", CURRENT_DATE), 
    (8, 5, "Are you impressed with this polling application?", CURRENT_DATE), 
    (9, 6, "Which front-end web development framework do you prefer?", CURRENT_DATE), 
    (10, 6, "What generation are you from?", CURRENT_DATE);

CREATE TABLE Option(
    PollID INT NOT NULL,
    OptionID INT NOT NULL,
    Content varchar(255) NOT NULL,
    Votes INT,
    PRIMARY KEY (PollID, OptionID)
);

INSERT INTO Option (PollID, OptionID, Content, Votes)
VALUES
    (1, 1, "New York", NULL),
    (1, 2, "Tokyo", NULL),
    (1, 3, "Hong Kong", NULL),
    (1, 4, "Sydney", NULL),
    (1, 5, "Johannesburg", NULL);

CREATE TABLE User(
    UserID INT NOT NULL,
    Username varchar(15) NOT NULL,
    HashedPass varchar(255) NOT NULL,
    AccessDate DATE NOT NULL,
    PRIMARY KEY (UserID)
);

INSERT INTO User (UserID, Username, HashedPass, AccessDate)
VALUES
    (1, "johnnyappleseed18", "$2a$12$GIjSB3OegWTctihUzI4cre3iN5YgNjCBS/WpX4xs5PiVn3dSRf.R.", CURRENT_DATE),
    (2, "johndoe33", "$2a$12$JwJKnxoPLhtPsgEVD8CgpO5Y5lj47btCHWiNrWeQS7x1uyrml4DeC", CURRENT_DATE),
    (3, "charlesxavier11", "$2a$12$F0W3AwUhc.sukVqB62lvKuZUW7gunuUjwc3pg41VeABTfFpMFOOIi", CURRENT_DATE),
    (4, "thomas9145", "$2a$12$V/rm5HePi.3N1GyVSB/yMeH0HVPK6vqMXoMIpuGh9frtsTakAxHfq", CURRENT_DATE),
    (5, "marcusantonelli", "$2a$12$Fqx3orZShP9n6ruZG0aQquTCBpGxiHTajMtSlP76ud5C0jl.AM6Qq", CURRENT_DATE),
    (6, "x_nick_x", "$2a$12$Qogy3A5co/8u9/8ZZIMS..klZPma5Jn.X1CfRWMAj.sgyJovZocWO", CURRENT_DATE);

CREATE TABLE Vote(
    UserID INT NOT NULL,
    PollID INT NOT NULL,
    OptionID INT NOT NULL,
    PRIMARY KEY (UserID, PollID, OptionID)
);

