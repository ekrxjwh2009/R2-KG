pr_1 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of answers]: If you can answer the question, give all possible answers.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Question : 'Freie Universität Berlin employed Wolf-Dieter Heilmeyer in the course of which years'
Given Entity : ['Wolf-Dieter Heilmeyer', 'Freie Universität Berlin']

[Your Task]
Statement : Let's look the relations linked with given entity.
Helper function : getRelation['Wolf-Dieter Heilmeyer'] ## getRelation['Freie Universität Berlin']
[User]
Execution result : 
Relation_list['Wolf-Dieter Heilmeyer']=['award received', 'employer']
Relation_list['Freie Universität Berlin'=['rector']
[Your Task]
Statement : The relation 'employer' of looks 'Wolf-Dieter Heilmeyer' mostly related to the question.
Helper function : exploreKG['Wolf-Dieter Heilmeyer']=['employer']
[User]
Execution result : ['Wolf-Dieter Heilmeyer', 'employer', 'Freie Universität Berlin', '1977', '2002'], ['Wolf-Dieter Heilmeyer', 'employer', 'University of Tübingen', '1971', '1977'], ['Wolf-Dieter Heilmeyer', 'employer', 'German Archaeological Institute at Athens', '1967', '1970'], ['Wolf-Dieter Heilmeyer', 'employer', 'Antikensammlung Berlin', '1978', '2002'], ['Wolf-Dieter Heilmeyer', 'employer', 'German Archaeological Institute at Rome', '1965', '1965']
[Your Task]
Statement : Now, we have all evidence to answer the year that Freie Universität Berlin employed in Wolf-Dieter Heilmeyer.
Helper function : Verification['1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002']


Example 2)
Question : 'Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom'
Given Entity : ['Member of the 31st Parliament of the United Kingdom','district attorney','J. D. Rees']

[Your Task]
Statement : Let's look the relations linked with given entity.
Helper function : getRelation['Member of the 31st Parliament of the United Kingdom'] ## getRelation['district attorney'] ## getRelation['district attorney'] ## getRelation['J. D. Rees']
[User]
Execution result : 
Relation_list['Member of the 31st Parliament of the United Kingdom']=['~position held']
Relation_list['district attorney']=['~position held', '~occupation']
Relation_list['J. D. Rees']=['position held']
[Your Task]
Statement : The relation 'position held' looks mostly related to the question.
Helper function : exploreKG['J. D. Rees']=['position held']
[User]
Execution result : ['J. D. Rees', 'position held', 'Member of the 28th Parliament of the United Kingdom', '1906', '1910'], ['J. D. Rees', 'position held', 'Member of the 29th Parliament of the United Kingdom', '1910', '1910'], ['J. D. Rees', 'position held', 'Member of the 30th Parliament of the United Kingdom', '1912', '1918'], ['J. D. Rees', 'position held', 'Member of the 31st Parliament of the United Kingdom', '1918', '1922']
[Your Task]
Statement : The relation '~position held' looks mostly related to the question.
Helper function : exploreKG['district attorney']=['~position held']
[User]
Execution result : ['district attorney', '~position held', 'Jim Chapman', '1976', '1985'], ['district attorney', '~position held', 'Kamala Harris', '1990', '1998'], ['district attorney', '~position held', 'Merlin Hull', '1907', '1909'], ['district attorney', '~position held', 'Thomas Jefferson Murray', '1922', '1933'], ['district attorney', '~position held', 'James E. Rogan', '1985', '1990'], ['district attorney', '~position held', 'Leverett Saltonstall', '1921', '1922'], ['district attorney', '~position held', 'Milton Horace West', '1922', '1925'], ['district attorney', '~position held', 'John Albert Carroll', '1937', '1941'], ['district attorney', '~position held', 'Steven Schiff', '1980', '1988'], ['district attorney', '~position held', 'Charles Russell Clason', '1922', '1926']
[Your Task]
Statement : Now, we have all evidence to answer the person that district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom.
Execution result : Verification['Leverett Saltonstall', 'Milton Horace West', 'Thomas Jefferson Murray']


Example 3)
Question : 'Before 2004 Summer Olympics, who held member of the Riksdag's position'
Given Entity : ['member of the Riksdag', '2004 Summer Olympics']

[Your Task]
Statement : Let's look the relations linked with given entity.
Helper function : getRelation['member of the Riksdag'] ## getRelation['2004 Summer Olympics']
[User]
Execution result : 
Relation_list['member of the Riksdag']=['~position held']
Relation_list['2004 Summer Olympics']=['~participant of', 'significant event']
[Your Task]
Statement : The relation '~position held' of 'member of the Riksdag', the relation '~participant of' and 'significant event' of '2004 Summer Olympics' looks mostly related to the question.
Helper function : exploreKG['member of the Riksdag']=['~participant of'] ## exploreKG['2004 Summer Olympics']=['significant event']
[User]
Execution result : ['member of the Riksdag', '~position held', 'Per Ahlmark', '1967', '1969'], ['member of the Riksdag', '~position held', 'Per Gahrton', '1976', '1979'], ['member of the Riksdag', '~position held', 'Karin Söder', '1976', '1991'], ['member of the Riksdag', '~position held', 'Olle Wästberg', '1976', '1982'], ['member of the Riksdag', '~position held', 'Claes Adelsköld', '1885', '1893'], ['member of the Riksdag', '~position held', 'Ewa Björling', '2014', '2014'], ['member of the Riksdag', '~position held', 'Veronica Palm', '2014', '2015'], ['member of the Riksdag', '~position held', 'Claes Adelsköld', '1862', '1863'], ['member of the Riksdag', '~position held', 'Per Gahrton', '1994', '1995'], ['member of the Riksdag', '~position held', 'Cecilia Wikström', '2002', '2009'], ['member of the Riksdag', '~position held', 'Alf Svensson', '1985', '1988'], ['member of the Riksdag', '~position held', 'Mauricio Rojas', '2006', '2008'], ['member of the Riksdag', '~position held', 'Gunilla Carlsson', '2002', '2013'], ['member of the Riksdag', '~position held', 'Per Gahrton', '1988', '1991'], ['member of the Riksdag', '~position held', 'Max Andersson', '2006', '2010'], ['member of the Riksdag', '~position held', 'Axel Gustav Adlercreutz', '1847', '1866'], ['member of the Riksdag', '~position held', 'Claes Adelsköld', '1876', '1884'], ['member of the Riksdag', '~position held', 'Fredrik Reinfeldt', '1991', '2014'], ['member of the Riksdag', '~position held', 'Maria Wetterstrand', '2001', '2011'], ['member of the Riksdag', '~position held', 'Alf Svensson', '1991', '2009'], ['member of the Riksdag', '~position held', 'Einar Dahl', '1954', '1970'], ['member of the Riksdag', '~position held', 'Mauricio Rojas', '2002', '2006'], ['member of the Riksdag', '~position held', 'Per Ahlmark', '1969', '1970'], ['member of the Riksdag', '~position held', 'Edvard Fränckel', '1889', '1911'], ['member of the Riksdag', '~position held', 'Hjalmar Branting', '1896', '1925'], ['member of the Riksdag', '~position held', 'Lena Ek', '2014', '2015'], ['member of the Riksdag', '~position held', 'Axel Gustav Adlercreutz', '1877', '1880'], ['member of the Riksdag', '~position held', 'Fredrick Federley', '2006', '2014'], ['2004 Summer Olympics', 'significant event', 'occurrence', '2004', '2004']
[Your Task]
Statement :  Now, we have all evidence to answer the person who held the member of Riksdag's position before 2004 Summer Olympics
Helper function : Verification['Per Ahlmark', 'Per Gahrton', 'Karin Söder', 'Olle Wästberg', 'Claes Adelsköld', 'Per Gahrton', 'Cecilia Wikström', 'Alf Svensson', 'Gunilla Carlsson', 'Axel Gustav Adlercreutz', 'Fredrik Reinfeldt', 'Maria Wetterstrand', 'Einar Dahl', 'Mauricio Rojas', 'Edvard Fränckel', 'Hjalmar Branting']


Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.
"""

pr_2 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of answers]: If you can answer the question, give all possible answers.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

Example 1)
Question : 'What person had been Governor of Connecticut before World War II'
Given entity : ['Governor of Connecticut', 'World War II']

[Your Task]
Statement : First, we need to information about governor of connecticut and world war II. Let's get relations linked with them.
Helper function : getRelation['Governor of Connecticut'] ## getRelation['World War II']
[User]
Execution result : 
Relation_list['Governor of Connecticut']=['~position held']
Relation_list['World War II']=['~conflict', '~participant of', 'significant event']
[Your Task]
Statement : Let's see triple around Governor of Connecticut linked with '~position held' and to know the occurrent year of world war II, let's see triples around world war II linked with 'significant event'.
Helper function : exploreKG['Governor of Connecticut']=['~position held'] ## exploreKG['World War II]=['significant event']
[User]
Execution result :
['World War II', 'significant event', 'occurrence', '1939', '1945'],['Governor of Connecticut', '~position held', 'Marcus H. Holcomb', '1915', '1921'], ['Governor of Connecticut', '~position held', 'Abraham A. Ribicoff', '1955', '1961'], ['Governor of Connecticut', '~position held', 'Clark Bissell', '1847', '1849'], ['Governor of Connecticut', '~position held', 'Chester Bowles', '1949', '1951'], ['Governor of Connecticut', '~position held', 'John G. Rowland', '1995', '2004'], ['Governor of Connecticut', '~position held', 'Wilbur Lucius Cross', '1931', '1939'], ['Governor of Connecticut', '~position held', 'John Davis Lodge', '1951', '1955'], ['Governor of Connecticut', '~position held', 'James L. McConaughy', '1947', '1948'], ['Governor of Connecticut', '~position held', 'Henry W. Edwards', '1833', '1834'], ['Governor of Connecticut', '~position held', 'Hiram Bingham III', '1925', '1925'], ['Governor of Connecticut', '~position held', 'Raymond E. Baldwin', '1939', '1941'], ['Governor of Connecticut', '~position held', 'Samuel Huntington', '1786', '1796'], ['Governor of Connecticut', '~position held', 'William W. Ellsworth', '1838', '1842'], ['Governor of Connecticut', '~position held', 'Ella T. Grasso', '1975', '1980'], ['Governor of Connecticut', '~position held', 'Everett J. Lake', '1921', '1923'], ['Governor of Connecticut', '~position held', 'Isaac Toucey', '1846', '1847'], ['Governor of Connecticut', '~position held', 'Oliver Wolcott', '1817', '1827'], ['Governor of Connecticut', '~position held', 'Simeon Eben Baldwin', '1911', '1915'], ['Governor of Connecticut', '~position held', 'Thomas Joseph Meskill', '1971', '1975'], ['Governor of Connecticut', '~position held', 'Jonathan Trumbull', '1797', '1809'], ['Governor of Connecticut', '~position held', 'Lowell P. Weicker', '1991', '1995'], ['Governor of Connecticut', '~position held', 'Oliver Wolcott', '1796', '1797'], ['Governor of Connecticut', '~position held', 'Roger Sherman Baldwin', '1844', '1846']
[Your Task]
Statement : According to the triples, the world war II occured in 1939, so the person held as governor of connecticut is 'Wilbur Lucius Cross'
Helper function : Verification['Wilbur Lucius Cross']


Example 2)
Question : Who were Governor of Idaho after Nazi Germany
Given entity : ['Governor of Idaho', 'Nazi Germany']

[Your Task]
Statement : Let's see what relations linked to Governor of Idaho and Nazi Germany.
Helper function : getRelation['Governor of Idaho'] ## getRelation['Nazi Germany']
[User]
Execution result : 
Relation_list['Governor of Idaho']=['~position held']
Relation_list['Nazi Germany']=['~allegiance', '~country', 'replaces', 'head of state', '~located in the administrative territorial entity', '~country of citizenship', 'shares border with', '~occupant', 'instance of', '~owned by', '~replaced by', 'significant event']
[Your Task]
Statement : To get when Nazi Germany occupied, let's see triples '~occupant' linked with Nazi Germany and '~position held' linked with Governor of Idaho.
Helper function : exploreKG['Governor of Idaho']=['~position held'] ## exploreKG['Nazi Germany']=[['~occupant']
[User]
Execution result : ['Governor of Idaho', '~position held', 'H. C. Baldridge', '1927', '1931'], ['Governor of Idaho', '~position held', 'Dirk Kempthorne', '1999', '2006'], ['Governor of Idaho', '~position held', 'Leonard B. Jordan', '1951', '1955'], ['Governor of Idaho', '~position held', 'Chase A. Clark', '1941', '1943'], ['Governor of Idaho', '~position held', 'Cecil D. Andrus', '1987', '1995'], ['Governor of Idaho', '~position held', 'C. A. Bottolfsen', '1939', '1941'], ['Governor of Idaho', '~position held', 'C. A. Bottolfsen', '1943', '1945'], ['Governor of Idaho', '~position held', 'Phil Batt', '1995', '1999'], ['Governor of Idaho', '~position held', 'Jim Risch', '2006', '2007'],['Nazi Germany', '~occupant', 'Kransberg Castle', '1939', '1945']
[Your Task]
Statement :  According to the triples, Nazi Germnay occupation ended in 1945, so the person who held position of governor of Idaho after 1945 is Leonard B. Jordan
Helper function : Verification['Leonard B. Jordan']


Example 3) 
Question : Who was Minister of Communications when Llin Golding, Baroness Golding was a Member of the 51st Parliament of the United Kingdom
Given entity : ['Minister of Communications', 'Member of the 51st Parliament of the United Kingdom', 'Llin Golding, Baroness Golding']

[Your Task]
Statement : Let's see what relations linked to 'Minister of Communications, Member of the 51st Parliament of the United Kingdom and Llin Golding, Baroness Golding.
Helper function : getRelation['Minister of Communications'] ## getRelation['Member of the 51st Parliament of the United Kingdom'] ## getRelation['Llin Golding, Baroness Golding']
[User]
Execution result :
Relation_list['Minister of Communications']=['~position held']
Relation_list['Member of the 51st Parliament of the United Kingdom']=['~position held']
Relation_list['Llin Golding, Baroness Golding']=['position held']
[Your Task]
Statement : To know when Llin Golding, Baroness Golding was a Member of the 51st Parliament of the United Kingdom, let's see triple of Llin Golding, Baroness Golding linked with relation 'position held'
Helper function : exploreKG['Llin Golding, Baroness Golding']=['position held']
[User]
Execution result : ['Llin Golding, Baroness Golding', 'position held', 'Member of the 52nd Parliament of the United Kingdom', '1997', '2001'], ['Llin Golding, Baroness Golding', 'position held', 'Member of the 51st Parliament of the United Kingdom', '1992', '1997'], ['Llin Golding, Baroness Golding', 'position held', 'Member of the 50th Parliament of the United Kingdom', '1987', '1992'], ['Llin Golding, Baroness Golding', 'position held', 'Member of the 49th Parliament of the United Kingdom', '1986', '1987']
[Your Task]
Statement : According to the triples, Llin Golding, Baroness Golding was a member of the 51sth parliament of UK from 1992 to 1997. Now let's see around Minister of Communications linked with '~position held' corresponding to this period.
Helper function : explorKG['Minister of Communications']=['~position held']
[User]
Execution result : ['Minister of Communications', '~position held', 'Meir Amit', '1977', '1978'], ['Minister of Communications', '~position held', 'Yitzhak Rabin', '1974', '1975'], ['Minister of Communications', '~position held', 'Amnon Rubinstein', '1984', '1987'], ['Minister of Communications', '~position held', 'Ariel Sharon', '2003', '2003'], ['Minister of Communications', '~position held', 'Mordechai Tzipori', '1981', '1984'], ['Minister of Communications', '~position held', "Yitzhak Moda'i", '1979', '1980'], ['Minister of Communications', '~position held', 'Moshe Kahlon', '2009', '2013'], ['Minister of Communications', '~position held', 'Mordechai Nurock', '1952', '1952'], ['Minister of Communications', '~position held', 'Moshe Shahal', '1992', '1993'], ['Minister of Communications', '~position held', 'Reuven Rivlin', '2001', '2003'], ['Minister of Communications', '~position held', 'Yisrael Barzilai', '1958', '1959'], ['Minister of Communications', '~position held', 'Dalia Itzik', '2005', '2005'], ['Minister of Communications', '~position held', 'Menachem Begin', '1977', '1977'], ['Minister of Communications', '~position held', 'Gilad Erdan', '2013', '2014'], ['Minister of Communications', '~position held', 'Binyamin Ben-Eliezer', '1999', '2001'], ['Minister of Communications', '~position held', 'Yosef Burg', '1952', '1958'], ['Minister of Communications', '~position held', 'Shimon Peres', '1970', '1974'], ['Minister of Communications', '~position held', 'Eliyahu Sasson', '1961', '1967'], ['Minister of Communications', '~position held', 'Benjamin Netanyahu', '2014', '2017'], ['Minister of Communications', '~position held', 'Ariel Atias', '2006', '2009'], ['Minister of Communications', '~position held', 'Gad Yaacobi', '1987', '1990'], ['Minister of Communications', '~position held', 'Avraham Hirschson', '2006', '2006'], ['Minister of Communications', '~position held', 'Yoram Aridor', '1981', '1981'], ['Minister of Communications', '~position held', 'Ehud Olmert', '2003', '2005'], ['Minister of Communications', '~position held', 'Shulamit Aloni', '1993', '1996'], ['Minister of Communications', '~position held', 'Elimelekh Rimalt', '1969', '1970'], ['Minister of Communications', '~position held', 'Limor Livnat', '1996', '1999']
[Your Task]
Statement : Now, we have enough evidence that who was minister of communication from 1992 to 1997.
Helper function : Verification['Moshe Shahal', 'Shulamit Aloni']

Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.

"""

pr_3 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

<Helper functions>
1. getRelation[entity]: Returns the list of relations connected to the entities.
2. exploreKG[entity]=[list of relations]: Returns the corresponding tail entities in graph data starts from single entity in given entity and given relation.
3. Verification[list of answers]: If you can answer the question, give all possible answers.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for my response. If response has made, continue your 'Statement and Helper function' task.
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use 'starred_actors' relation.

Here are some examples.

[Your Task]
Statement : First, we need to information about governor of connecticut and world war II. Let's get relations linked with them.
Helper function : getRelation['Governor of Connecticut'] ## getRelation['World War II']
[User]
Execution result : 
Relation_list['Governor of Connecticut']=['~position held']
Relation_list['World War II']=['~conflict', '~participant of', 'significant event']
[Your Task]
Statement : Let's see triple around Governor of Connecticut linked with '~position held' and to know the occurrent year of world war II, let's see triples around world war II linked with 'significant event'.
Helper function : exploreKG['Governor of Connecticut']=['~position held'] ## exploreKG['World War II]=['significant event']
[User]
Execution result :
['World War II', 'significant event', 'occurrence', '1939', '1945'],['Governor of Connecticut', '~position held', 'Marcus H. Holcomb', '1915', '1921'], ['Governor of Connecticut', '~position held', 'Abraham A. Ribicoff', '1955', '1961'], ['Governor of Connecticut', '~position held', 'Clark Bissell', '1847', '1849'], ['Governor of Connecticut', '~position held', 'Chester Bowles', '1949', '1951'], ['Governor of Connecticut', '~position held', 'John G. Rowland', '1995', '2004'], ['Governor of Connecticut', '~position held', 'Wilbur Lucius Cross', '1931', '1939'], ['Governor of Connecticut', '~position held', 'John Davis Lodge', '1951', '1955'], ['Governor of Connecticut', '~position held', 'James L. McConaughy', '1947', '1948'], ['Governor of Connecticut', '~position held', 'Henry W. Edwards', '1833', '1834'], ['Governor of Connecticut', '~position held', 'Hiram Bingham III', '1925', '1925'], ['Governor of Connecticut', '~position held', 'Raymond E. Baldwin', '1939', '1941'], ['Governor of Connecticut', '~position held', 'Samuel Huntington', '1786', '1796'], ['Governor of Connecticut', '~position held', 'William W. Ellsworth', '1838', '1842'], ['Governor of Connecticut', '~position held', 'Ella T. Grasso', '1975', '1980'], ['Governor of Connecticut', '~position held', 'Everett J. Lake', '1921', '1923'], ['Governor of Connecticut', '~position held', 'Isaac Toucey', '1846', '1847'], ['Governor of Connecticut', '~position held', 'Oliver Wolcott', '1817', '1827'], ['Governor of Connecticut', '~position held', 'Simeon Eben Baldwin', '1911', '1915'], ['Governor of Connecticut', '~position held', 'Thomas Joseph Meskill', '1971', '1975'], ['Governor of Connecticut', '~position held', 'Jonathan Trumbull', '1797', '1809'], ['Governor of Connecticut', '~position held', 'Lowell P. Weicker', '1991', '1995'], ['Governor of Connecticut', '~position held', 'Oliver Wolcott', '1796', '1797'], ['Governor of Connecticut', '~position held', 'Roger Sherman Baldwin', '1844', '1846']
[Your Task]
Statement : According to the triples, the world war II occured in 1939, so the person held as governor of connecticut is 'Wilbur Lucius Cross'
Helper function : Verification['Wilbur Lucius Cross']


Example 2)
Question : Who were Governor of Idaho after Nazi Germany
Given entity : ['Governor of Idaho', 'Nazi Germany']

[Your Task]
Statement : Let's see what relations linked to Governor of Idaho and Nazi Germany.
Helper function : getRelation['Governor of Idaho'] ## getRelation['Nazi Germany']
[User]
Execution result : 
Relation_list['Governor of Idaho']=['~position held']
Relation_list['Nazi Germany']=['~allegiance', '~country', 'replaces', 'head of state', '~located in the administrative territorial entity', '~country of citizenship', 'shares border with', '~occupant', 'instance of', '~owned by', '~replaced by', 'significant event']
[Your Task]
Statement : To get when Nazi Germany occupied, let's see triples '~occupant' linked with Nazi Germany and '~position held' linked with Governor of Idaho.
Helper function : exploreKG['Governor of Idaho']=['~position held'] ## exploreKG['Nazi Germany']=[['~occupant']
[User]
Execution result : ['Governor of Idaho', '~position held', 'H. C. Baldridge', '1927', '1931'], ['Governor of Idaho', '~position held', 'Dirk Kempthorne', '1999', '2006'], ['Governor of Idaho', '~position held', 'Leonard B. Jordan', '1951', '1955'], ['Governor of Idaho', '~position held', 'Chase A. Clark', '1941', '1943'], ['Governor of Idaho', '~position held', 'Cecil D. Andrus', '1987', '1995'], ['Governor of Idaho', '~position held', 'C. A. Bottolfsen', '1939', '1941'], ['Governor of Idaho', '~position held', 'C. A. Bottolfsen', '1943', '1945'], ['Governor of Idaho', '~position held', 'Phil Batt', '1995', '1999'], ['Governor of Idaho', '~position held', 'Jim Risch', '2006', '2007'],['Nazi Germany', '~occupant', 'Kransberg Castle', '1939', '1945']
[Your Task]
Statement :  According to the triples, Nazi Germnay occupation ended in 1945, so the person who held position of governor of Idaho after 1945 is Leonard B. Jordan
Helper function : Verification['Leonard B. Jordan']


Example 3) 
Question : Who was Minister of Communications when Llin Golding, Baroness Golding was a Member of the 51st Parliament of the United Kingdom
Given entity : ['Minister of Communications', 'Member of the 51st Parliament of the United Kingdom', 'Llin Golding, Baroness Golding']

[Your Task]
Statement : Let's see what relations linked to 'Minister of Communications, Member of the 51st Parliament of the United Kingdom and Llin Golding, Baroness Golding.
Helper function : getRelation['Minister of Communications'] ## getRelation['Member of the 51st Parliament of the United Kingdom'] ## getRelation['Llin Golding, Baroness Golding']
[User]
Execution result :
Relation_list['Minister of Communications']=['~position held']
Relation_list['Member of the 51st Parliament of the United Kingdom']=['~position held']
Relation_list['Llin Golding, Baroness Golding']=['position held']
[Your Task]
Statement : To know when Llin Golding, Baroness Golding was a Member of the 51st Parliament of the United Kingdom, let's see triple of Llin Golding, Baroness Golding linked with relation 'position held'
Helper function : exploreKG['Llin Golding, Baroness Golding']=['position held']
[User]
Execution result : ['Llin Golding, Baroness Golding', 'position held', 'Member of the 52nd Parliament of the United Kingdom', '1997', '2001'], ['Llin Golding, Baroness Golding', 'position held', 'Member of the 51st Parliament of the United Kingdom', '1992', '1997'], ['Llin Golding, Baroness Golding', 'position held', 'Member of the 50th Parliament of the United Kingdom', '1987', '1992'], ['Llin Golding, Baroness Golding', 'position held', 'Member of the 49th Parliament of the United Kingdom', '1986', '1987']
[Your Task]
Statement : According to the triples, Llin Golding, Baroness Golding was a member of the 51sth parliament of UK from 1992 to 1997. Now let's see around Minister of Communications linked with '~position held' corresponding to this period.
Helper function : explorKG['Minister of Communications']=['~position held']
[User]
Execution result : ['Minister of Communications', '~position held', 'Meir Amit', '1977', '1978'], ['Minister of Communications', '~position held', 'Yitzhak Rabin', '1974', '1975'], ['Minister of Communications', '~position held', 'Amnon Rubinstein', '1984', '1987'], ['Minister of Communications', '~position held', 'Ariel Sharon', '2003', '2003'], ['Minister of Communications', '~position held', 'Mordechai Tzipori', '1981', '1984'], ['Minister of Communications', '~position held', "Yitzhak Moda'i", '1979', '1980'], ['Minister of Communications', '~position held', 'Moshe Kahlon', '2009', '2013'], ['Minister of Communications', '~position held', 'Mordechai Nurock', '1952', '1952'], ['Minister of Communications', '~position held', 'Moshe Shahal', '1992', '1993'], ['Minister of Communications', '~position held', 'Reuven Rivlin', '2001', '2003'], ['Minister of Communications', '~position held', 'Yisrael Barzilai', '1958', '1959'], ['Minister of Communications', '~position held', 'Dalia Itzik', '2005', '2005'], ['Minister of Communications', '~position held', 'Menachem Begin', '1977', '1977'], ['Minister of Communications', '~position held', 'Gilad Erdan', '2013', '2014'], ['Minister of Communications', '~position held', 'Binyamin Ben-Eliezer', '1999', '2001'], ['Minister of Communications', '~position held', 'Yosef Burg', '1952', '1958'], ['Minister of Communications', '~position held', 'Shimon Peres', '1970', '1974'], ['Minister of Communications', '~position held', 'Eliyahu Sasson', '1961', '1967'], ['Minister of Communications', '~position held', 'Benjamin Netanyahu', '2014', '2017'], ['Minister of Communications', '~position held', 'Ariel Atias', '2006', '2009'], ['Minister of Communications', '~position held', 'Gad Yaacobi', '1987', '1990'], ['Minister of Communications', '~position held', 'Avraham Hirschson', '2006', '2006'], ['Minister of Communications', '~position held', 'Yoram Aridor', '1981', '1981'], ['Minister of Communications', '~position held', 'Ehud Olmert', '2003', '2005'], ['Minister of Communications', '~position held', 'Shulamit Aloni', '1993', '1996'], ['Minister of Communications', '~position held', 'Elimelekh Rimalt', '1969', '1970'], ['Minister of Communications', '~position held', 'Limor Livnat', '1996', '1999']
[Your Task]
Statement : Now, we have enough evidence that who was minister of communication from 1992 to 1997.
Helper function : Verification['Moshe Shahal', 'Shulamit Aloni']

Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.

"""