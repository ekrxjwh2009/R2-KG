pr_1 = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, find proper labels for given question.
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choose what relation information is more needed.
The triple set takes the form [Head, Relation, Tail, start_time, end_time], which means 'Head's relation is tail and the period lasted from the start_time to the end_time. 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head and the period lasted from the start_time to the end_time.' 
The following cases may arise: Choose one option from 'Executable ([list of labels])' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
If multiple answers are possible, Choose all possible answers.
Refer to the explanations of the two options below to answer the Statement and Evaluation.


<Cases> 
1. If there is a sufficient triple set to answer the question, you must select all possible answers if multiple answers seem possible --> Executable ([list of possible answers])
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 

<Example 1>
[User]
Question : Freie Universität Berlin employed Wolf-Dieter Heilmeyer in the course of which years
Triple sets : [['Wolf-Dieter Heilmeyer', 'employer', 'Freie Universität Berlin', '1977', '2002'], ['Wolf-Dieter Heilmeyer', 'employer', 'University of Tübingen', '1971', '1977'], ['Wolf-Dieter Heilmeyer', 'employer', 'German Archaeological Institute at Athens', '1967', '1970'], ['Wolf-Dieter Heilmeyer', 'employer', 'Antikensammlung Berlin', '1978', '2002'], ['Wolf-Dieter Heilmeyer', 'employer', 'German Archaeological Institute at Rome', '1965', '1965']]
Relations of Entity:
Relation_list['Wolf-Dieter Heilmeyer']=['award received', 'employer']
Relation_list['Freie Universität Berlin']=['rector']
[ChatGPT]
Statement : According to the triple sets, Freie Universität Berlin employed in Wolf-Dieter Heilmeyer in '1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002'.
Evaluation : Executable([1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002])

<Example 2>
[User]
Question : 'Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom'
Triple sets : [['J. D. Rees', 'position held', 'Member of the 28th Parliament of the United Kingdom', '1906', '1910'], ['J. D. Rees', 'position held', 'Member of the 29th Parliament of the United Kingdom', '1910', '1910'], ['J. D. Rees', 'position held', 'Member of the 30th Parliament of the United Kingdom', '1912', '1918'], ['J. D. Rees', 'position held', 'Member of the 31st Parliament of the United Kingdom', '1918', '1922'],['district attorney', '~position held', 'Jim Chapman', '1976', '1985'], ['district attorney', '~position held', 'Kamala Harris', '1990', '1998'], ['district attorney', '~position held', 'Merlin Hull', '1907', '1909'], ['district attorney', '~position held', 'Thomas Jefferson Murray', '1922', '1933'], ['district attorney', '~position held', 'James E. Rogan', '1985', '1990'], ['district attorney', '~position held', 'Leverett Saltonstall', '1921', '1922'], ['district attorney', '~position held', 'Milton Horace West', '1922', '1925'], ['district attorney', '~position held', 'John Albert Carroll', '1937', '1941'], ['district attorney', '~position held', 'Steven Schiff', '1980', '1988'], ['district attorney', '~position held', 'Charles Russell Clason', '1922', '1926']]
Relations of Entity : 
Relation_list['Member of the 31st Parliament of the United Kingdom']=['~position held']
Relation_list['district attorney']=['~position held', '~occupation']
Relation_list['J. D. Rees']=['position held']
[ChatGPT]
Statement : According to the triple sets, the person that district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom was 'Leverett Saltonstall','Milton Horace West','Thomas Jefferson Murray'.
Evaluation : Executable([Leverett Saltonstall, Milton Horace West, Thomas Jefferson Murray])

<Example 3>
[User]
Question : Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom
Triple sets : [['J. D. Rees', 'position held', 'Member of the 28th Parliament of the United Kingdom', '1906', '1910'], ['J. D. Rees', 'position held', 'Member of the 29th Parliament of the United Kingdom', '1910', '1910'], ['J. D. Rees', 'position held', 'Member of the 30th Parliament of the United Kingdom', '1912', '1918'], ['J. D. Rees', 'position held', 'Member of the 31st Parliament of the United Kingdom', '1918', '1922']]
Relations of Entity : 
Relation_list['district attorney']=['~position held', '~occupation']
Relation_list['Member of the 31st Parliament of the United Kingdom']=['~position held']
Relation_list['J. D. Rees']=['position held']
[ChatGPT]
Statement : We need more evidence. Try to see relation '~position held' of 'district attorney' from 1918 to 1922.
Evalution : Not executable(Insufficient evidence)


Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Question : <<<<CLAIM>>>>
Triple sets : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>


"""

pr_2 = """
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, find proper labels for given question.
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choose what relation information is more needed.
The triple set takes the form [Head, Relation, Tail, start_time, end_time], which means 'Head's Relation is Tail and started' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head and the period lasted from the start_time to the end_time.' 
The following cases may arise: Choose one option from 'Executable ([list of labels])' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
If multiple answers are possible, Choose all possible answers.
Refer to the explanations of the two options below to answer the Statement and Evaluation.


<Cases> 
1. If there is a sufficient triple set to answer the question, you must select all possible answers if multiple answers seem possible --> Executable ([list of possible answers])
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 

<Example 1>
[User]
Question : 'What person had been Governor of Connecticut before World War II'
Triple sets : [['World War II', 'significant event', 'occurrence', '1939', '1945'],['Governor of Connecticut', '~position held', 'Marcus H. Holcomb', '1915', '1921'], ['Governor of Connecticut', '~position held', 'Abraham A. Ribicoff', '1955', '1961'], ['Governor of Connecticut', '~position held', 'Clark Bissell', '1847', '1849'], ['Governor of Connecticut', '~position held', 'Chester Bowles', '1949', '1951'], ['Governor of Connecticut', '~position held', 'John G. Rowland', '1995', '2004'], ['Governor of Connecticut', '~position held', 'Wilbur Lucius Cross', '1931', '1939'], ['Governor of Connecticut', '~position held', 'John Davis Lodge', '1951', '1955'], ['Governor of Connecticut', '~position held', 'James L. McConaughy', '1947', '1948'], ['Governor of Connecticut', '~position held', 'Henry W. Edwards', '1833', '1834'], ['Governor of Connecticut', '~position held', 'Hiram Bingham III', '1925', '1925'], ['Governor of Connecticut', '~position held', 'Raymond E. Baldwin', '1939', '1941'], ['Governor of Connecticut', '~position held', 'Samuel Huntington', '1786', '1796'], ['Governor of Connecticut', '~position held', 'William W. Ellsworth', '1838', '1842'], ['Governor of Connecticut', '~position held', 'Ella T. Grasso', '1975', '1980'], ['Governor of Connecticut', '~position held', 'Everett J. Lake', '1921', '1923'], ['Governor of Connecticut', '~position held', 'Isaac Toucey', '1846', '1847'], ['Governor of Connecticut', '~position held', 'Oliver Wolcott', '1817', '1827'], ['Governor of Connecticut', '~position held', 'Simeon Eben Baldwin', '1911', '1915'], ['Governor of Connecticut', '~position held', 'Thomas Joseph Meskill', '1971', '1975'], ['Governor of Connecticut', '~position held', 'Jonathan Trumbull', '1797', '1809'], ['Governor of Connecticut', '~position held', 'Lowell P. Weicker', '1991', '1995'], ['Governor of Connecticut', '~position held', 'Oliver Wolcott', '1796', '1797'], ['Governor of Connecticut', '~position held', 'Roger Sherman Baldwin', '1844', '1846']]
Relations of Entity : 
Relation_list['Governor of Connecticut']=['~position held']
Relation_list['World War II']=['~conflict', '~participant of', 'significant event']
[ChatGPT]
Statement : According to the triples, the world war II occured in 1939, so the person held as governor of connecticut is 'Wilbur Lucius Cross'
Evaluation : Executable([Wilbur Lucius Cross])

<Example 2>
[User]
Question : Who were Governor of Idaho after Nazi Germany
Triple sets :[['Governor of Idaho', '~position held', 'H. C. Baldridge', '1927', '1931'], ['Governor of Idaho', '~position held', 'Dirk Kempthorne', '1999', '2006'], ['Governor of Idaho', '~position held', 'Leonard B. Jordan', '1951', '1955'], ['Governor of Idaho', '~position held', 'Chase A. Clark', '1941', '1943'], ['Governor of Idaho', '~position held', 'Cecil D. Andrus', '1987', '1995'], ['Governor of Idaho', '~position held', 'C. A. Bottolfsen', '1939', '1941'], ['Governor of Idaho', '~position held', 'C. A. Bottolfsen', '1943', '1945'], ['Governor of Idaho', '~position held', 'Phil Batt', '1995', '1999'], ['Governor of Idaho', '~position held', 'Jim Risch', '2006', '2007'],['Nazi Germany', '~occupant', 'Kransberg Castle', '1939', '1945']]
Relations of Entity : 
Relation_list['Governor of Idaho']=['~position held']
Relation_list['Nazi Germany']=['~allegiance', '~country', 'replaces', 'head of state', '~located in the administrative territorial entity', '~country of citizenship', 'shares border with', '~occupant', 'instance of', '~owned by', '~replaced by', 'significant event']
[ChatGPT]
Statement : According to the triples, Nazi Germnay occupation ended in 1945, so the person who held position of governor of Idaho after 1945 is Leonard B. Jordan
Evaluation : Executable([Leonard B. Jordan])

<Example 3>
[User]
Question : When Godman Irvine was the Member of the 44th Parliament of the United Kingdom who was the member of the Cortes franquistas
Triple sets : [['Godman Irvine', 'position held', 'Member of the 42nd Parliament of the United Kingdom', '1959', '1964'], ['Godman Irvine', 'position held', 'Member of the 43rd Parliament of the United Kingdom', '1964', '1966'], ['Godman Irvine', 'position held', 'Member of the 44th Parliament of the United Kingdom', '1966', '1970'], ['Godman Irvine', 'position held', 'Member of the 46th Parliament of the United Kingdom', '1974', '1974'], ['Godman Irvine', 'position held', 'Member of the 48th Parliament of the United Kingdom', '1979', '1983'], ['Godman Irvine', 'position held', 'Member of the 41st Parliament of the United Kingdom', '1955', '1959'], ['Godman Irvine', 'position held', 'Member of the 45th Parliament of the United Kingdom', '1970', '1974'], ['Godman Irvine', 'position held', 'Member of the 47th Parliament of the United Kingdom', '1974', '1979'],['member of the Cortes franquistas', '~position held', 'Jesús Esperabé de Arteaga González', '1967', '1971'], ['member of the Cortes franquistas', '~position held', 'Carlos Ollero Gómez', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Armando Muñoz Calero', '1946', '1971'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1944', '1946'], ['member of the Cortes franquistas', '~position held', 'José María Sentís Simeón', '1964', '1967'], ['member of the Cortes franquistas', '~position held', 'Claudi Colomer i Marqués', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'José Utrera Molina', '1958', '1977'], ['member of the Cortes franquistas', '~position held', 'Juan Antonio Samaranch', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Fernando María Castiella y Maíz', '1943', '1948'], ['member of the Cortes franquistas', '~position held', 'Jaime Alba Delibes', '1951', '1952'], ['member of the Cortes franquistas', '~position held', 'José Félix de Lequerica y Erquiza', '1943', '1963'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Camilo Alonso Vega', '1943', '1969'], ['member of the Cortes franquistas', '~position held', 'Ángel González Álvarez', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1967', '1971'], ['member of the Cortes franquistas', '~position held', 'José Millán Astray', '1943', '1954'], ['member of the Cortes franquistas', '~position held', 'Bartolomé Barba Hernández', '1946', '1947'], ['member of the Cortes franquistas', '~position held', 'Jesús Esperabé de Arteaga González', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Ramón Serrano Suñer', '1943', '1967'], ['member of the Cortes franquistas', '~position held', 'José Moreno Torres', '1946', '1952'], ['member of the Cortes franquistas', '~position held', 'Euloxio Gómez Franqueira', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Luis Ortiz Muñoz', '1943', '1951'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1952', '1955'], ['member of the Cortes franquistas', '~position held', 'Tomás Suñer Ferrer', '1946', '1947'], ['member of the Cortes franquistas', '~position held', 'José Finat y Escrivá de Romaní', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Blas Piñar', '1958', '1977'], ['member of the Cortes franquistas', '~position held', 'Leopoldo Calvo-Sotelo', '1975', '1976'], ['member of the Cortes franquistas', '~position held', 'Gabriel Cisneros', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Gregorio Marañón Moya', '1961', '1971'], ['member of the Cortes franquistas', '~position held', 'José Maldonado y Fernández del Torco', '1956', '1958'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Luis Díez del Corral', '1946', '1949'], ['member of the Cortes franquistas', '~position held', 'Antoni Maria Simarro i Puig', '1951', '1957'], ['member of the Cortes franquistas', '~position held', 'Eduardo Navarro Álvarez', '1974', '1977'], ['member of the Cortes franquistas', '~position held', 'Manuel Halcón', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'José Martínez Emperador', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Segismundo Royo-Villanova y Fernández-Cavada', '1951', '1964'], ['member of the Cortes franquistas', '~position held', 'Leopoldo Calvo-Sotelo', '1976', '1977'], ['member of the Cortes franquistas', '~position held', 'Álvaro de Figueroa, 1st Count of Romanones', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Pilar Primo de Rivera', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Euloxio Gómez Franqueira', '1967', '1971'], ['member of the Cortes franquistas', '~position held', 'José María Sánchez-Ventura Pascual', '1975', '1975'], ['member of the Cortes franquistas', '~position held', 'Miquel Mateu i Pla', '1943', '1945'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1961', '1964'], ['member of the Cortes franquistas', '~position held', 'Víctor Hellín', '1944', '1961'], ['member of the Cortes franquistas', '~position held', 'Torcuato Luca de Tena', '1964', '1977'], ['member of the Cortes franquistas', '~position held', 'José Fernández-Villaverde', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'José Clua Queixalós', '1969', '1971'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1952', '1955'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1955', '1958'], ['member of the Cortes franquistas', '~position held', 'Fernando María Castiella y Maíz', '1957', '1969'], ['member of the Cortes franquistas', '~position held', 'Claudi Colomer i Marqués', '1958', '1961'], ['member of the Cortes franquistas', '~position held', 'Leopoldo Calvo-Sotelo', '1971', '1976'], ['member of the Cortes franquistas', '~position held', 'Carlos González-Bueno', '1965', '1976'], ['member of the Cortes franquistas', '~position held', 'Rafael Ruiz Gallardón', '1970', '1974'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1949', '1952'], ['member of the Cortes franquistas', '~position held', 'Fernando Martín-Sánchez Juliá', '1958', '1970'], ['member of the Cortes franquistas', '~position held', 'Luis Carrero Blanco', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'José Clua Queixalós', '1971', '1977'], ['member of the Cortes franquistas', '~position held', 'Elías Tormo', '1949', '1952'], ['member of the Cortes franquistas', '~position held', 'Carlos Ollero Gómez', '1949', '1961'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1958', '1961'], ['member of the Cortes franquistas', '~position held', 'José María de Areilza, Count of Motrico', '1946', '1958'], ['member of the Cortes franquistas', '~position held', 'Fernando Herrero Tejedor', '1957', '1975'], ['member of the Cortes franquistas', '~position held', 'Emilio Rodríguez Tarduchy', '1951', '1964'], ['member of the Cortes franquistas', '~position held', 'Francisco Javier Conde García', '1943', '1956'], ['member of the Cortes franquistas', '~position held', 'Carlos Ruiz del Castillo', '1951', '1951'], ['member of the Cortes franquistas', '~position held', 'Carlos González-Bueno', '1946', '1949'], ['member of the Cortes franquistas', '~position held', 'Blas Tello', '1964', '1967'], ['member of the Cortes franquistas', '~position held', 'Manuel de Mora-Figueroa', '1943', '1964'], ['member of the Cortes franquistas', '~position held', 'Manuel Díez-Alegría', '1970', '1977'], ['member of the Cortes franquistas', '~position held', 'Alberto Alcocer y Ribacoba', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Juan José Espinosa San Martín', '1964', '1969'], ['member of the Cortes franquistas', '~position held', 'Florentino Pérez Embid', '1958', '1967'], ['member of the Cortes franquistas', '~position held', 'Santiago de Cruïlles de Peratallada Bosch', '1970', '1977'], ['member of the Cortes franquistas', '~position held', 'José Monasterio Ituarte', '1943', '1952'], ['member of the Cortes franquistas', '~position held', 'Francisco Labadie Otermin', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Adolfo Suárez', '1967', '1977'], ['member of the Cortes franquistas', '~position held', 'Alfonso Pérez Viñeta', '1946', '1949'], ['member of the Cortes franquistas', '~position held', 'Ernesto Giménez Caballero', '1943', '1958'], ['member of the Cortes franquistas', '~position held', 'José Luis de Arrese', '1943', '1977'], ['member of the Cortes franquistas', '~position held', 'Carlos Asensio Cabanillas', '1943', '1970'], ['member of the Cortes franquistas', '~position held', 'Antonio Barroso y Sánchez-Guerra', '1967', '1977'], ['member of the Cortes franquistas', '~position held', "Joaquim Buxó Dulce d'Abaigar", '1949', '1967'], ['member of the Cortes franquistas', '~position held', 'José María Pemán', '1945', '1946'], ['member of the Cortes franquistas', '~position held', 'Ricardo Oreja', '1952', '1965'], ['member of the Cortes franquistas', '~position held', 'Rodolfo Martín Villa', '1964', '1977'], ['member of the Cortes franquistas', '~position held', 'Luis Díez del Corral', '1943', '1946'], ['member of the Cortes franquistas', '~position held', 'Pedro Muguruza', '1943', '1949'], ['member of the Cortes franquistas', '~position held', 'Antonio Barroso y Sánchez-Guerra', '1957', '1962']]
Relations of Entity : 
Relation_list['member of the Cortes franquistas']=['~position held']
Relation_list['Godman Irvine']=['position held']
Relation_list['Member of the 44th Parliament of the United Kingdom']=['~position held']
[ChatGPT]
Statement : According to the triples, Godman Irvine was the Member of the 44th Parliament of the United Kingdom from 1966 to 1970. So, there are several people who was member of Corteds franquistas from 1966 to 1970. 
Evaluation : Executable([Ángel González Álvarez, Ramón Serrano Suñer, José Martínez Emperador, Rafael Ruiz Gallardón, Euloxio Gómez Franqueira, Joaquim Buxó Dulce d'Abaigar, Francisco Labadie Otermin, Manuel Díez-Alegría, Juan Antonio Samaranch, Fernando María Castiella y Maíz, José María Sentís Simeón, Gregorio Marañón Moya, Adolfo Suárez, Carlos González-Bueno, Florentino Pérez Embid, Santiago de Cruïlles de Peratallada Bosch, José Luis de Arrese, Jesús Esperabé de Arteaga González, Armando Muñoz Calero, Camilo Alonso Vega, Fernando Herrero Tejedor, Blas Tello, Carlos Asensio Cabanillas, Fernando Martín-Sánchez Juliá, Antonio Barroso y Sánchez-Guerra, José Finat y Escrivá de Romaní, Torcuato Luca de Tena, Juan José Espinosa San Martín, Rodolfo Martín Villa, José Clua Queixalós, Blas Piñar, Pilar Primo de Rivera, José Utrera Molina])

<Example 4>
[User]
Question : Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom
Triple sets : [['J. D. Rees', 'position held', 'Member of the 28th Parliament of the United Kingdom', '1906', '1910'], ['J. D. Rees', 'position held', 'Member of the 29th Parliament of the United Kingdom', '1910', '1910'], ['J. D. Rees', 'position held', 'Member of the 30th Parliament of the United Kingdom', '1912', '1918'], ['J. D. Rees', 'position held', 'Member of the 31st Parliament of the United Kingdom', '1918', '1922']]
Relations of Entity : 
Relation_list['district attorney']=['~position held', '~occupation']
Relation_list['Member of the 31st Parliament of the United Kingdom']=['~position held']
Relation_list['J. D. Rees']=['position held']
[ChatGPT]
Statement : We need more evidence. Try to see relation '~position held' of 'district attorney' from 1918 to 1922.
Evalution : Not executable(Insufficient evidence)


Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Question : <<<<CLAIM>>>>
Triple sets : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>
"""

pr_3 ="""
You are the evaluator. I will show you a claim and a triple set extracted from a graph. 
Based on the given triple set and relation list of each entity, find proper labels for given question.
If given triple sets are lack of information to verify the claim, give the the combination of entity and relation you need. You can refer the given relations list and choose what relation information is more needed.
The triple set takes the form [Head, Relation, Tail, start_time, end_time], which means 'Head's Relation is Tail and started' 
If the relation starts with '~', it indicates a reverse relation, meaning 'Tail's relation is head and the period lasted from the start_time to the end_time.' 
The following cases may arise: Choose one option from 'Executable ([list of labels])' or 'Not executable(Insufficient evidence)'.
If you choose 'Not executable(Insufficient evidence)', You must specify in the statement which additional relation information is needed for a particular entity. However, the relation can only be selected from the given Relation_list and cannot be created arbitrarily.
If multiple answers are possible, Choose all possible answers.
Refer to the explanations of the two options below to answer the Statement and Evaluation.


<Cases> 
1. If there is a sufficient triple set to answer the question, you must select all possible answers if multiple answers seem possible --> Executable ([list of possible answers])
2. If the triple set is insufficient or ambiguos to determine the True/False of the claim --> Not executable (Insufficient evidence) 


<Example 1>
[User]
Question : 'Who preceded David I of Scotland as monarch of Scotland'
Triple sets : [['David I of Scotland', 'position held', 'monarch of Scotland', '1124', '1153'], ['monarch of Scotland', '~position held', 'Malcolm III of Scotland', '1058', '1093'], ['monarch of Scotland', '~position held', 'James III of Scotland', '1460', '1488'], ['monarch of Scotland', '~position held', 'James V of Scotland', '1513', '1542'], ['monarch of Scotland', '~position held', 'Alexander III of Scotland', '1249', '1286'], ['monarch of Scotland', '~position held', 'David I of Scotland', '1124', '1153'], ['monarch of Scotland', '~position held', 'James I of Scotland', '1406', '1437'], ['monarch of Scotland', '~position held', 'William III', '1689', '1702'], ['monarch of Scotland', '~position held', 'Mary II of England', '1689', '1694'], ['monarch of Scotland', '~position held', 'David II of Scotland', '1329', '1371'], ['monarch of Scotland', '~position held', 'Mary, Queen of Scots', '1542', '1567'], ['monarch of Scotland', '~position held', 'James VI and I', '1587', '1625'], ['monarch of Scotland', '~position held', 'James IV of Scotland', '1488', '1513'], ['monarch of Scotland', '~position held', 'Robert I of Scotland', '1306', '1329'], ['monarch of Scotland', '~position held', 'James II of Scotland', '1437', '1460'], ['monarch of Scotland', '~position held', 'Charles II of England', '1649', '1651'], ['monarch of Scotland', '~position held', 'Charles I of England', '1625', '1649'], ['monarch of Scotland', '~position held', 'Anne of Great Britain', '1702', '1707'], ['monarch of Scotland', '~position held', 'Alexander I of Scotland', '1107', '1124'], ['monarch of Scotland', '~position held', 'James VII and II', '1685', '1688']]
Relations of Entity : 
Relation_list['David I of Scotland']=['position held']
Relation_list['monarch of Scotland']=['~position held']
[ChatGPT]
Statement : According to the triples. David I of Scotland held position of monarch in 1124, so the precedor of David I of Scotland is Alexander I of Scotland who help position from 1107 to 1124.
Evaluation : Executable([Alexander I of Scotland])

<Example 2>
[User]
Question : Who was district attorney when J. D. Rees was the Member of the 31st Parliament of the United Kingdom
Triple sets : [['J. D. Rees', 'position held', 'Member of the 28th Parliament of the United Kingdom', '1906', '1910'], ['J. D. Rees', 'position held', 'Member of the 29th Parliament of the United Kingdom', '1910', '1910'], ['J. D. Rees', 'position held', 'Member of the 30th Parliament of the United Kingdom', '1912', '1918'], ['J. D. Rees', 'position held', 'Member of the 31st Parliament of the United Kingdom', '1918', '1922'], ['district attorney', '~position held', 'Jim Chapman', '1976', '1985'], ['district attorney', '~position held', 'Kamala Harris', '1990', '1998'], ['district attorney', '~position held', 'Merlin Hull', '1907', '1909'], ['district attorney', '~position held', 'Thomas Jefferson Murray', '1922', '1933'], ['district attorney', '~position held', 'James E. Rogan', '1985', '1990'], ['district attorney', '~position held', 'Leverett Saltonstall', '1921', '1922'], ['district attorney', '~position held', 'Milton Horace West', '1922', '1925'], ['district attorney', '~position held', 'John Albert Carroll', '1937', '1941'], ['district attorney', '~position held', 'Steven Schiff', '1980', '1988'], ['district attorney', '~position held', 'Bert H. Miller', '1918', '1921'], ['district attorney', '~position held', 'George Armistead Smathers', '1940', '1942'], ['district attorney', '~position held', 'John James Rooney', '1940', '1944'], ['district attorney', '~position held', 'Mike DeWine', '1977', '1981'], ['district attorney', '~position held', 'William Homer Thornberry', '1941', '1942'], ['district attorney', '~position held', 'Arthur Thomas Stewart', '1923', '1939'], ['district attorney', '~position held', 'Bill Delahunt', '1975', '1996'], ['district attorney', '~position held', 'William Henry Stevenson', '1924', '1926'], ['district attorney', '~position held', 'Thomas Augustus Pickett', '1935', '1945'], ['district attorney', '~position held', 'Thomas Abernethy', '1936', '1942'], ['district attorney', '~position held', 'Isidore Dollinger', '1960', '1968'], ['district attorney', '~position held', 'Ted Poe', '1973', '1981'], ['district attorney', '~position held', 'Howard Coble', '1969', '1973'], ['district attorney', '~position held', 'Morgan M. Moulder', '1928', '1938'], ['district attorney', '~position held', 'Sean Duffy', '2002', '2010'], ['district attorney', '~position held', 'Trent Kelly', '2012', '2015'], ['district attorney', '~position held', 'John Albert Carroll', '1933', '1934'], ['district attorney', '~position held', 'Kathleen Rice', '2005', '2014'], ['district attorney', '~position held', 'Albert Thomas', '1930', '1936'], ['district attorney', '~position held', 'Bernard W. Kearney', '1931', '1942'], ['district attorney', '~position held', 'Charles Russell Clason', '1922', '1926'], ['district attorney', '~position held', 'Eric Swalwell', '2006', '2012'], ['district attorney', '~position held', 'William Josiah Crow', '1928', '1932'], ['district attorney', '~position held', 'Kamala Harris', '2004', '2011'], ['district attorney', '~position held', 'John W. Heselton', '1939', '1944'], ['district attorney', '~position held', 'Tom Marino', '1992', '2002'], ['district attorney', '~position held', 'William Meyers Colmer', '1928', '1933'], ['district attorney', '~position held', 'Jimmy Panetta', '1996', '2010'], ['district attorney', '~position held', 'Jamie Lloyd Whitten', '1933', '1941'], ['district attorney', '~position held', 'Mo Brooks', '1991', '1993'], ['district attorney', '~position held', 'Alexander Wiley', '1909', '1915'], ['district attorney', '~position held', 'Louis E. Graham', '1912', '1924'], ['district attorney', '~position held', 'Guy Gillette', '1907', '1909'], ['district attorney', '~position held', 'George H. Mahon', '1927', '1933'], ['district attorney', '~position held', 'John Cornelius Stennis', '1932', '1937'], ['district attorney', '~position held', 'Ed Gossett', '1933', '1937'], ['district attorney', '~position held', 'Bill Keating', '1998', '2010'], ['district attorney', '~position held', 'Robert E. Cramer', '1981', '1990'], ['district attorney', '~position held', 'Jimmy Panetta', '2010', '2016'], ['district attorney', '~position held', 'Dennis Moore', '1977', '1989'], ['district attorney', '~position held', 'Jeanine Pirro', '1994', '2005'], ['district attorney', '~position held', 'Patrick Anthony McCarran', '1907', '1909'], ['district attorney', '~position held', 'Charles Russell Clason', '1927', '1930'], ['district attorney', '~position held', 'William Henry Stevenson', '1935', '1941'], ['district attorney', '~position held', 'George William Andrews', '1931', '1943'], ['district attorney', '~position held', 'John William Wright Patman', '1924', '1929'], ['district attorney', '~position held', 'Timothy Griffin', '2006', '2007'], ['district attorney', '~position held', 'Hugh Scott', '1926', '1941'], ['district attorney', '~position held', 'Mike Arcuri', '1994', '2006'], ['district attorney', '~position held', 'Guy Cordon', '1923', '1935']]
Relations of Entity : 
Relation_list['district attorney']=['~position held', '~occupation']
Relation_list['Member of the 31st Parliament of the United Kingdom']=['~position held']
Relation_list['J. D. Rees']=['position held']
[ChatGPT]
Statement : According to the triples, J.D. Rees was member of 31st Parliament of the United Kingdom from 1918 to 1922. There are several people who held as minister of communication in corresponding periods.
Evaluation : Executable([Shulamit Aloni, Limor Livnat, Moshe Shahal])

<Example 3>
[User]
Question : What year did Yelena Bonner get the Thorolf Rafto Memorial Prize?
Triple sets : [['Yelena Bonner', 'award received', 'Giuseppe Motta Medal', '2004', '2004'], ['Yelena Bonner', 'award received', 'Robert Schuman Medal', '2001', '2001'], ['Yelena Bonner', 'award received', 'Recipient of the Order of Tomáš Garrigue Masaryk, 2nd class', '2003', '2003'], ['Yelena Bonner', 'award received', 'Thorolf Rafto Memorial Prize', '1991', '1991']]
Relations of Entity : 
Relation_list['Thorolf Rafto Memorial Prize']=['~award received']
Relation_list['Yelena Bonner']=['award received', '~winner']
[ChatGPT]
Statement : According to the triples, Yelena Bonner received Thorolf Rafto Memorial Prize in 1991.
Evaluation : Executable([1991])

<Exmaple 4>
[User]
Question : At what time did George Cubitt, 1st Baron Ashcombe hold the position of Member of the 18th Parliament of the United Kingdom
Triple sets : [['Member of the 18th Parliament of the United Kingdom', '~position held', 'Lord George Gordon-Lennox', '1860', '1865'], ['Member of the 18th Parliament of the United Kingdom', '~position held', 'William Hodgson Barrow', '1859', '1865'], ['Member of the 18th Parliament of the United Kingdom', '~position held', 'Frederick Hervey, 3rd Marquess of Bristol', '1859', '1864'], ['Member of the 18th Parliament of the United Kingdom', '~position held', 'Robert Stephenson', '1859', '1859']]
Relations of Entity :
Relation_list['Member of the 18th Parliament of the United Kingdom']=['~position held']
Relation_list['George Cubitt, 1st Baron Ashcombe']=['position held']
[ChatGPT]
Statement : We need more information. Try to look relation 'position held' linked with 'George Cubitt, 1st Baron Ashcombe'
Evaluation : Not executable(Insufficient evidence)

Now, it's your turn. Continue your 'Statement and Evaluation' task. Response must have same form with upper examples.
[User]
Question : <<<<CLAIM>>>>
Triple sets : <<<<Triple set>>>>
Relations of Entity : <<<<GOLD RELATIONS>>>>

"""