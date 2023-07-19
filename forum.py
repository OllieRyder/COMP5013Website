import sqlite3
con = sqlite3.connect("forum.db")
c = con.cursor()


c.execute("DROP TABLE IF EXISTS user");
c.execute("CREATE TABLE user (userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, userName TEXT NOT NULL, passwordHash BLOB NOT NULL, isAdmin BOOLEAN NOT NULL, creationTime INTEGER NOT NULL, lastVisit INTEGER NOT NULL)");

c.execute("DROP TABLE IF EXISTS topic");
c.execute("CREATE TABLE topic (topicID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, topicName TEXT NOT NULL, postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, creationTime INTEGER NOT NULL, updateTime INTEGER NOT NULL )");

c.execute("DROP TABLE IF EXISTS claim");
c.execute("CREATE TABLE claim (claimID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, topic INTEGER NOT NULL REFERENCES topic(topicID) ON DELETE CASCADE ON UPDATE CASCADE, postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, creationTime INTEGER NOT NULL, updateTime INTEGER NOT NULL, text TEXT NOT NULL )");

c.execute("DROP TABLE IF EXISTS claimToClaimType");
c.execute("CREATE TABLE claimToClaimType (claimRelTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, claimRelType TEXT NOT NULL)");
c.execute('INSERT INTO claimToClaimType VALUES (1,"Opposed")');
c.execute('INSERT INTO claimToClaimType VALUES (2,"Equivalent")');

c.execute("DROP TABLE IF EXISTS claimToClaim");
c.execute("CREATE TABLE claimToClaim (claimRelID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, first INTEGER NOT NULL REFERENCES claim(claimID) ON DELETE CASCADE ON UPDATE CASCADE, second INTEGER NOT NULL REFERENCES claim(claimID) ON DELETE CASCADE ON UPDATE CASCADE, claimRelType INTEGER NOT NULL REFERENCES claimToClaimType(claimRelTypeID) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT claimToClaimUnique UNIQUE (first, second))");

c.execute("DROP TABLE IF EXISTS replyText");
c.execute("CREATE TABLE replyText (replyTextID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, creationTime INTEGER NOT NULL, text TEXT NOT NULL)");

c.execute("DROP TABLE IF EXISTS replyToClaimType");
c.execute("CREATE TABLE replyToClaimType (claimReplyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, claimReplyType TEXT NOT NULL)");
c.execute('INSERT INTO replyToClaimType VALUES (1, "Clarification")');
c.execute('INSERT INTO replyToClaimType VALUES (2, "Supporting Argument")');
c.execute('INSERT INTO replyToClaimType VALUES (3, "Counterargument")');

c.execute("DROP TABLE IF EXISTS replyToClaim");
c.execute("CREATE TABLE replyToClaim (replyToClaimID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, reply INTEGER NOT NULL REFERENCES replyText (replyTextID) ON DELETE CASCADE ON UPDATE CASCADE, claim INTEGER NOT NULL REFERENCES claim (claimID) ON DELETE CASCADE ON UPDATE CASCADE, replyToClaimRelType INTEGER NOT NULL REFERENCES replyToClaimType(claimReplyTypeID) ON DELETE CASCADE ON UPDATE CASCADE)");

c.execute("DROP TABLE IF EXISTS replyToReplyType");
c.execute("CREATE TABLE replyToReplyType (replyReplyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, replyReplyType TEXT NOT NULL)");
c.execute('INSERT INTO replyToReplyType VALUES (1, "Evidence")');
c.execute('INSERT INTO replyToReplyType VALUES (2, "Support")');
c.execute('INSERT INTO replyToReplyType VALUES (3, "Rebuttal")');

c.execute("DROP TABLE IF EXISTS replyToReply");
c.execute("CREATE TABLE replyToReply (replyToReplyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, reply INTEGER NOT NULL REFERENCES replyText(replyTextID) ON DELETE CASCADE ON UPDATE CASCADE, parent INTEGER NOT NULL REFERENCES replyText(replyTextID) ON DELETE CASCADE ON UPDATE CASCADE, replyToReplyRelType INTEGER NOT NULL REFERENCES replyToReplyType(replyReplyTypeID) ON DELETE CASCADE ON UPDATE CASCADE)")
con.commit()