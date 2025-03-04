pr_1 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].
Importantly, Do not change the format of the entity or relation including '~'.

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
Helper function : Verification[]


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
Execution result : Verification[]


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
Helper function : Verification[]


Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.
"""

pr_2 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].
Importantly, Do not change the format of the entity or relation including '~'.

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
Helper function : Verification[]


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
Statement : Now, we know when Nazi German occupation lasted and who held position for governor of Idaho.
Helper function : Verification[]


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
Helper function : Verification[]

Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.

"""

pr_3 = """
Your task is finding proper labels for given claim based on the graph data without your base knowledge.
You can use below helper functions to find the evidence for finding labels.

Helper Functions
1.getRelation[entity]: Returns the list of relations linked to the entity. You can choose several relations from the list that seem related to the claim.
2.exploreKG[entity]=[relation_1,relation_2, ... relation_K]: Returns the triple set around the entity. For example, [entity, relation_1, tail entity] etc. You can choose relation from [User]'s execution result.
3.Verification[]: After getting enough evidence after exploreKG() helper function and if verification can be done, call this function. If [User] requires more information, you need to collect more triples in following steps.

You must follow the exact format of the given helper function.

Now, I will give you a claim and Given Entity that you can refer to.
However, some of the entities needed in verification are not included in Given Entity.
You have to use proper helper functions to find proper information to verify the given claim.
Once you give a response about helper function, stop for [User] response. If response has made, continue your [Your Task] (Do not make multiple 'Helper function: ' lines).
Importantly, you have to use inverse relation if you need. For example, if you want to find films starred by certain actors (when only actors were given), you have to use '~starred_actors' relation such as exploreKG['actor']=['~starred_actors'].
Importantly, Do not change the format of the entity or relation including '~'.

Here are some examples.


Example 1)
Question : Who preceded David I of Scotland as monarch of Scotland
Given entity : ['David I of Scotland', 'monarch of Scotland']

[Your Task]
Statement : To get information about David I of Scotland and monarch of Scotland, let's see relations linked to them.
Helper function : getRelation['David I of Scotland'] ## getRelation['monarch of Scotland']
[User]
Execution : 
Relation_list['David I of Scotland']=['position held']
Relation_list['monarch of Scotland']=['~position held']
[Your Task]
Statement : Now, let's see triple around David I of Scotland linked with 'position held' and triples around monarch of Scotland linked with '~position held'.
Helper function : exploreKG['David I of Scotland']=['position held'] ## exploreKG['monarch of Scotland']=['~position held']
[User]
Execution result : ['David I of Scotland', 'position held', 'monarch of Scotland', '1124', '1153'], ['monarch of Scotland', '~position held', 'Malcolm III of Scotland', '1058', '1093'], ['monarch of Scotland', '~position held', 'James III of Scotland', '1460', '1488'], ['monarch of Scotland', '~position held', 'James V of Scotland', '1513', '1542'], ['monarch of Scotland', '~position held', 'Alexander III of Scotland', '1249', '1286'], ['monarch of Scotland', '~position held', 'David I of Scotland', '1124', '1153'], ['monarch of Scotland', '~position held', 'James I of Scotland', '1406', '1437'], ['monarch of Scotland', '~position held', 'William III', '1689', '1702'], ['monarch of Scotland', '~position held', 'Mary II of England', '1689', '1694'], ['monarch of Scotland', '~position held', 'David II of Scotland', '1329', '1371'], ['monarch of Scotland', '~position held', 'Mary, Queen of Scots', '1542', '1567'], ['monarch of Scotland', '~position held', 'James VI and I', '1587', '1625'], ['monarch of Scotland', '~position held', 'James IV of Scotland', '1488', '1513'], ['monarch of Scotland', '~position held', 'Robert I of Scotland', '1306', '1329'], ['monarch of Scotland', '~position held', 'James II of Scotland', '1437', '1460'], ['monarch of Scotland', '~position held', 'Charles II of England', '1649', '1651'], ['monarch of Scotland', '~position held', 'Charles I of England', '1625', '1649'], ['monarch of Scotland', '~position held', 'Anne of Great Britain', '1702', '1707'], ['monarch of Scotland', '~position held', 'Alexander I of Scotland', '1107', '1124'], ['monarch of Scotland', '~position held', 'James VII and II', '1685', '1688']
[Your Task]
Statement : Now, we have all information about the position held period of each moarch of Scotland. 
Helper function : Verification[]


Example 2)
Question : When Godman Irvine was the Member of the 44th Parliament of the United Kingdom who was the member of the Cortes franquistas
Given entity : ['member of the Cortes franquistas','Godman Irvine','Member of the 44th Parliament of the United Kingdom']

[Your Task]
Statement : Let's see what relations linked to each entity 'member of the Cortes franquistas','Godman Irvine','Member of the 44th Parliament of the United Kingdom'.
Helper function : getRelation['member of the Cortes franquistas'] ## getRelation['Godman Irvine'] ## getRelation['Member of the 44th Parliament of the United Kingdom']
[User]
Execution result :
Relation_list['member of the Cortes franquistas']=['~position held']
Relation_list['Godman Irvine']=['position held']
Relation_list['Member of the 44th Parliament of the United Kingdom']=['~position held']
[Your Task]
Statement : Now, let's see when Godman Irvine was the Member of the 44th Parliament of the United Kingdom.
Helper function : exploreKG['Godman Irvine']=['position held']
[User]
Execution result : ['Godman Irvine', 'position held', 'Member of the 42nd Parliament of the United Kingdom', '1959', '1964'], ['Godman Irvine', 'position held', 'Member of the 43rd Parliament of the United Kingdom', '1964', '1966'], ['Godman Irvine', 'position held', 'Member of the 44th Parliament of the United Kingdom', '1966', '1970'], ['Godman Irvine', 'position held', 'Member of the 46th Parliament of the United Kingdom', '1974', '1974'], ['Godman Irvine', 'position held', 'Member of the 48th Parliament of the United Kingdom', '1979', '1983'], ['Godman Irvine', 'position held', 'Member of the 41st Parliament of the United Kingdom', '1955', '1959'], ['Godman Irvine', 'position held', 'Member of the 45th Parliament of the United Kingdom', '1970', '1974'], ['Godman Irvine', 'position held', 'Member of the 47th Parliament of the United Kingdom', '1974', '1979']
[Your Task]
Statement : According to the triples, Godman Irvine was the Member of the 44th Parliament of the United Kingdom from 1966 to 1970. Now, let's see who was the member Cortes franquistas in this period.
Helper function : exploreKG['member of the Cortes franquistas']=['~position held']
[User]
Execution result : ['member of the Cortes franquistas', '~position held', 'Jesús Esperabé de Arteaga González', '1967', '1971'], ['member of the Cortes franquistas', '~position held', 'Carlos Ollero Gómez', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Armando Muñoz Calero', '1946', '1971'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1944', '1946'], ['member of the Cortes franquistas', '~position held', 'José María Sentís Simeón', '1964', '1967'], ['member of the Cortes franquistas', '~position held', 'Claudi Colomer i Marqués', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'José Utrera Molina', '1958', '1977'], ['member of the Cortes franquistas', '~position held', 'Juan Antonio Samaranch', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Fernando María Castiella y Maíz', '1943', '1948'], ['member of the Cortes franquistas', '~position held', 'Jaime Alba Delibes', '1951', '1952'], ['member of the Cortes franquistas', '~position held', 'José Félix de Lequerica y Erquiza', '1943', '1963'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Camilo Alonso Vega', '1943', '1969'], ['member of the Cortes franquistas', '~position held', 'Ángel González Álvarez', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1967', '1971'], ['member of the Cortes franquistas', '~position held', 'José Millán Astray', '1943', '1954'], ['member of the Cortes franquistas', '~position held', 'Bartolomé Barba Hernández', '1946', '1947'], ['member of the Cortes franquistas', '~position held', 'Jesús Esperabé de Arteaga González', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Ramón Serrano Suñer', '1943', '1967'], ['member of the Cortes franquistas', '~position held', 'José Moreno Torres', '1946', '1952'], ['member of the Cortes franquistas', '~position held', 'Euloxio Gómez Franqueira', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Luis Ortiz Muñoz', '1943', '1951'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1952', '1955'], ['member of the Cortes franquistas', '~position held', 'Tomás Suñer Ferrer', '1946', '1947'], ['member of the Cortes franquistas', '~position held', 'José Finat y Escrivá de Romaní', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Blas Piñar', '1958', '1977'], ['member of the Cortes franquistas', '~position held', 'Leopoldo Calvo-Sotelo', '1975', '1976'], ['member of the Cortes franquistas', '~position held', 'Gabriel Cisneros', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Gregorio Marañón Moya', '1961', '1971'], ['member of the Cortes franquistas', '~position held', 'José Maldonado y Fernández del Torco', '1956', '1958'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Luis Díez del Corral', '1946', '1949'], ['member of the Cortes franquistas', '~position held', 'Antoni Maria Simarro i Puig', '1951', '1957'], ['member of the Cortes franquistas', '~position held', 'Eduardo Navarro Álvarez', '1974', '1977'], ['member of the Cortes franquistas', '~position held', 'Manuel Halcón', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'José Martínez Emperador', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Segismundo Royo-Villanova y Fernández-Cavada', '1951', '1964'], ['member of the Cortes franquistas', '~position held', 'Leopoldo Calvo-Sotelo', '1976', '1977'], ['member of the Cortes franquistas', '~position held', 'Álvaro de Figueroa, 1st Count of Romanones', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Pilar Primo de Rivera', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Euloxio Gómez Franqueira', '1967', '1971'], ['member of the Cortes franquistas', '~position held', 'José María Sánchez-Ventura Pascual', '1975', '1975'], ['member of the Cortes franquistas', '~position held', 'Miquel Mateu i Pla', '1943', '1945'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1961', '1964'], ['member of the Cortes franquistas', '~position held', 'Víctor Hellín', '1944', '1961'], ['member of the Cortes franquistas', '~position held', 'Torcuato Luca de Tena', '1964', '1977'], ['member of the Cortes franquistas', '~position held', 'José Fernández-Villaverde', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'José Clua Queixalós', '1969', '1971'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1952', '1955'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'Fernando María Castiella y Maíz', '1957', '1969'], ['member of the Cortes franquistas', '~position held', 'Claudi Colomer i Marqués', '1958', '1961'], ['member of the Cortes franquistas', '~position held', 'Leopoldo Calvo-Sotelo', '1971', '1976'], ['member of the Cortes franquistas', '~position held', 'Carlos González-Bueno', '1965', '1976'], ['member of the Cortes franquistas', '~position held', 'Rafael Ruiz Gallardón', '1970', '1974'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1949', '1952'], ['member of the Cortes franquistas', '~position held', 'Fernando Martín-Sánchez Juliá', '1958', '1970'], ['member of the Cortes franquistas', '~position held', 'Luis Carrero Blanco', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'José Clua Queixalós', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Elías Tormo', '1949', '1952'], ['member of the Cortes franquistas', '~position held', 'Carlos Ollero Gómez', '1949', '1961'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1958', '1961'], ['member of the Cortes franquistas', '~position held', 'José María de Areilza, Count of Motrico', '1946', '1958'], ['member of the Cortes franquistas', '~position held', 'Fernando Herrero Tejedor', '1957', '1975'], ['member of the Cortes franquistas', '~position held', 'Emilio Rodríguez Tarduchy', '1951', '1964'], ['member of the Cortes franquistas', '~position held', 'Francisco Javier Conde García', '1943', '1956'], ['member of the Cortes franquistas', '~position held', 'Carlos Ruiz del Castillo', '1951', '1951'], ['member of the Cortes franquistas', '~position held', 'Carlos González-Bueno', '1946', '1949'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1964', '1967'], ['member of the Cortes franquistas', '~position held', 'Manuel de Mora-Figueroa', '1943', '1964'], ['member of the Cortes franquistas', '~position held', 'Manuel Díez-Alegría', '1970', '1977'], ['member of the Cortes franquistas', '~position held', 'Alberto Alcocer y Ribacoba', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Juan José Espinosa San Martín', '1964', '1969'], ['member of the Cortes franquistas', '~position held', 'Florentino Pérez Embid', '1958', '1967'], ['member of the Cortes franquistas', '~position held', 'Santiago de Cruïlles de Peratallada Bosch', '1970', '1977'], ['member of the Cortes franquistas', '~position held', 'José Monasterio Ituarte', '1943', '1952'], ['member of the Cortes franquistas', '~position held', 'Francisco Labadie Otermin', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Adolfo Suárez', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1946', '1949'], ['member of the Cortes franquistas', '~position held', 'Ernesto Giménez Caballero', '1943', '1958'], ['member of the Cortes franquistas', '~position held', 'José Luis de Arrese', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Carlos Asensio Cabanillas', '1943', '1970'], ['member of the Cortes franquistas', '~position held', 'Antonio Barroso y Sánchez-Guerra', '1967', '1977'], ['member of the Cortes franquistas', '~position held', "Joaquim Buxó Dulce d'Abaigar", '1949', '1967'], ['member of the Cortes franquistas', '~position held', 'José María Pemán', '1945', '1946'], ['member of the Cortes franquistas', '~position held', 'Ricardo Oreja', '1952', '1965'], ['member of the Cortes franquistas', '~position held', 'Rodolfo Martín Villa', '1964', '1977'], ['member of the Cortes franquistas', '~position held', 'Luis Díez del Corral', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Pedro Muguruza', '1943', '1949'], ['member of the Cortes franquistas', '~position held', 'Antonio Barroso y Sánchez-Guerra', '1957', '1962']
[Your Task]
Statement : Now we now who was the member of Corteds franquistas from 1966 to 1970.
Helper function : verification[]


Example 3)
Question : Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom
Given entity : ['district attorney', 'Member of the 31st Parliament of the United Kingdom', 'J. D. Rees']

[Your Task]
Statement : Let's see what relations linked to each entity, 'district attorney', 'Member of the 31st Parliament of the United Kingdom', 'J. D. Rees'.
Helper function : getRelation['district attorney'] ## getRelation['Member of the 31st Parliament of the United Kingdom'] ## getRelation['J. D. Rees']
[User]
Execution result : 
Relation_list['district attorney']=['~position held', '~occupation']
Relation_list['Member of the 31st Parliament of the United Kingdom']=['~position held']
Relation_list['J. D. Rees']=['position held']
[Your Task]
Statement : I need to know when J. D. Rees was the Member of the 31st Parliament of the United Kingdom
Helper function : exploreKG['J. D. Rees']=['position held']
[User]
Execution result : ['J. D. Rees', 'position held', 'Member of the 28th Parliament of the United Kingdom', '1906', '1910'], ['J. D. Rees', 'position held', 'Member of the 29th Parliament of the United Kingdom', '1910', '1910'], ['J. D. Rees', 'position held', 'Member of the 30th Parliament of the United Kingdom', '1912', '1918'], ['J. D. Rees', 'position held', 'Member of the 31st Parliament of the United Kingdom', '1918', '1922']
[Your Task]
Statement : According to the triples, J.D. Rees was member of 31st Parliament of the United Kingdom from 1918 to 1922.
Helper function : Verification[]
[User]
Execution result : We need more evidence. Try to see relation '~position held' of 'district attorney' from 1918 to 1922.
[Your Task]
Statement : Okay, let's see triples of district attorney linked with '~position held' to know person who was district during 1918 to 1922.
Helper function : exploreKG['district attorney']=['~position held']
[User]
Execution result : ['district attorney', '~position held', 'Jim Chapman', '1976', '1985'], ['district attorney', '~position held', 'Kamala Harris', '1990', '1998'], ['district attorney', '~position held', 'Merlin Hull', '1907', '1909'], ['district attorney', '~position held', 'Thomas Jefferson Murray', '1922', '1933'], ['district attorney', '~position held', 'James E. Rogan', '1985', '1990'], ['district attorney', '~position held', 'Leverett Saltonstall', '1921', '1922'], ['district attorney', '~position held', 'Milton Horace West', '1922', '1925'], ['district attorney', '~position held', 'John Albert Carroll', '1937', '1941'], ['district attorney', '~position held', 'Steven Schiff', '1980', '1988'], ['district attorney', '~position held', 'Bert H. Miller', '1918', '1921'], ['district attorney', '~position held', 'George Armistead Smathers', '1940', '1942'], ['district attorney', '~position held', 'John James Rooney', '1940', '1944'], ['district attorney', '~position held', 'Mike DeWine', '1977', '1981'], ['district attorney', '~position held', 'William Homer Thornberry', '1941', '1942'], ['district attorney', '~position held', 'Arthur Thomas Stewart', '1923', '1939'], ['district attorney', '~position held', 'Bill Delahunt', '1975', '1996'], ['district attorney', '~position held', 'William Henry Stevenson', '1924', '1926'], ['district attorney', '~position held', 'Thomas Augustus Pickett', '1935', '1945'], ['district attorney', '~position held', 'Thomas Abernethy', '1936', '1942'], ['district attorney', '~position held', 'Isidore Dollinger', '1960', '1968'], ['district attorney', '~position held', 'Ted Poe', '1973', '1981'], ['district attorney', '~position held', 'Howard Coble', '1969', '1973'], ['district attorney', '~position held', 'Morgan M. Moulder', '1928', '1938'], ['district attorney', '~position held', 'Sean Duffy', '2002', '2010'], ['district attorney', '~position held', 'Trent Kelly', '2012', '2015'], ['district attorney', '~position held', 'John Albert Carroll', '1933', '1934'], ['district attorney', '~position held', 'Kathleen Rice', '2005', '2014'], ['district attorney', '~position held', 'Albert Thomas', '1930', '1936'], ['district attorney', '~position held', 'Bernard W. Kearney', '1931', '1942'], ['district attorney', '~position held', 'Charles Russell Clason', '1922', '1926'], ['district attorney', '~position held', 'Eric Swalwell', '2006', '2012'], ['district attorney', '~position held', 'William Josiah Crow', '1928', '1932'], ['district attorney', '~position held', 'Kamala Harris', '2004', '2011'], ['district attorney', '~position held', 'John W. Heselton', '1939', '1944'], ['district attorney', '~position held', 'Tom Marino', '1992', '2002'], ['district attorney', '~position held', 'William Meyers Colmer', '1928', '1933'], ['district attorney', '~position held', 'Jimmy Panetta', '1996', '2010'], ['district attorney', '~position held', 'Jamie Lloyd Whitten', '1933', '1941'], ['district attorney', '~position held', 'Mo Brooks', '1991', '1993'], ['district attorney', '~position held', 'Alexander Wiley', '1909', '1915'], ['district attorney', '~position held', 'Louis E. Graham', '1912', '1924'], ['district attorney', '~position held', 'Guy Gillette', '1907', '1909'], ['district attorney', '~position held', 'George H. Mahon', '1927', '1933'], ['district attorney', '~position held', 'John Cornelius Stennis', '1932', '1937'], ['district attorney', '~position held', 'Ed Gossett', '1933', '1937'], ['district attorney', '~position held', 'Bill Keating', '1998', '2010'], ['district attorney', '~position held', 'Robert E. Cramer', '1981', '1990'], ['district attorney', '~position held', 'Jimmy Panetta', '2010', '2016'], ['district attorney', '~position held', 'Dennis Moore', '1977', '1989'], ['district attorney', '~position held', 'Jeanine Pirro', '1994', '2005'], ['district attorney', '~position held', 'Patrick Anthony McCarran', '1907', '1909'], ['district attorney', '~position held', 'Charles Russell Clason', '1927', '1930'], ['district attorney', '~position held', 'William Henry Stevenson', '1935', '1941'], ['district attorney', '~position held', 'George William Andrews', '1931', '1943'], ['district attorney', '~position held', 'John William Wright Patman', '1924', '1929'], ['district attorney', '~position held', 'Timothy Griffin', '2006', '2007'], ['district attorney', '~position held', 'Hugh Scott', '1926', '1941'], ['district attorney', '~position held', 'Mike Arcuri', '1994', '2006'], ['district attorney', '~position held', 'Guy Cordon', '1923', '1935']
[Your Task]
Statement : There are several people who was distric attorney from 1918 to 1922.
Helper function : Verification[]


Now, it's your turn.
Claim : <<<Question>>>
Given entity: <<<Entity set>>>

Let's start the process.

"""


paraphrase_prompt = """
You are the paraphraser. Rewrite the following claim in a more formal tone, keeping the core idea intact.
If the given claim has a colloquial style format, paraphrase it into written style format.
Give three paraphrased sentences for given claim.

<Example 1>
[User]
Claim : Freie Universität Berlin employed Wolf-Dieter Heilmeyer in the course of which years?
[ChatGPT]
1. During which years was Wolf-Dieter Heilmeyer employed by Freie Universität Berlin?
2. What years encompass Wolf-Dieter Heilmeyer's period of employment at Freie Universität Berlin?
3. Freie Universität Berlin employed Wolf-Dieter Heilmeyer during which specific years?


<Example 2>
[User]
Claim : What person had been Governor of Connecticut before World War II?
[ChatGPT]
1. Who served as Governor of Connecticut in the period preceding World War II?
2. Which individual held the position of Governor of Connecticut prior to the onset of World War II?
3. Before the outbreak of World War II, who occupied the office of Governor of Connecticut?


<Example 3>
[User]
Claim : Who were Governor of Idaho after Nazi Germany?
[ChatGPT]
1. Who assumed the role of Governor of Idaho following the fall of Nazi Germany?
2. Which individuals served as Governor of Idaho in the post-Nazi Germany era?
3. After the dissolution of Nazi Germany, who held the office of Governor of Idaho?


<Example 4>
[User]
Claim : Who was Minister of Communications when Llin Golding, Baroness Golding was a Member of the 51st Parliament of the United Kingdom?
[ChatGPT]
1. During Llin Golding, Baroness Golding's tenure as a Member of the 51st Parliament of the United Kingdom, who held the position of Minister of Communications?
2. Who occupied the role of Minister of Communications while Llin Golding, Baroness Golding, served in the 51st Parliament of the United Kingdom?
3. When Llin Golding, Baroness Golding, was a member of the 51st Parliament, who was serving as the Minister of Communications?


<Example 5>
[User]
Claim : Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom?
[ChatGPT]
1. During J. D. Rees's tenure as a Member of the 31st Parliament of the United Kingdom, who served as district attorney?
2. Who held the position of district attorney while J. D. Rees was a member of the 31st Parliament of the United Kingdom?
3. While J. D. Rees was part of the 31st Parliament, who assumed the role of district attorney?


<Example 6>
[User]
Claim : Before the 2004 Summer Olympics, who held member of the Riksdag's position?
[ChatGPT]
1. Prior to the 2004 Summer Olympics, who held a position as a member of the Riksdag?
2. Who was a member of the Riksdag in the period leading up to the 2004 Summer Olympics?
3. Before the 2004 Summer Olympics commenced, who occupied a position as a member of the Riksdag?


<Example 7>
[User]
Claim : Who preceded David I of Scotland as monarch of Scotland?
[ChatGPT]
1. Who was the predecessor of David I of Scotland in the role of monarch?
2. Which individual ascended the Scottish throne prior to David I of Scotland?
3. Who held the position of monarch of Scotland before David I ascended to the throne?


<Example 8>
[User]
Claim : When Godman Irvine was the Member of the 44th Parliament of the United Kingdom who was the member of the Cortes franquistas?
[ChatGPT]
1. During Godman Irvine's tenure as a Member of the 44th Parliament of the United Kingdom, who was serving as a member of the Cortes franquistas?
2. While Godman Irvine was part of the 44th Parliament of the United Kingdom, who held membership in the Cortes franquistas?
3. When Godman Irvine served in the 44th Parliament, who was a member of the Cortes franquistas?


Now, it's your turn. Continue your paraphrasing task. Response must have same form with upper examples.
[User]
Claim : <<<<CLAIM>>>>
"""