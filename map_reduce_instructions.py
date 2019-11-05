# DON'T RUN THIS SCRIPT INDIVIDUALLY

# clean previous results if needed
# rm -r ~/DataMngAssignmentTwo/results/*

# copy cleaned data to the dataset directory for map/reduce program
# cp -i ~/DataMngAssignmentTwo/content.txt ~/spark/spark-2.4.4-bin-hadoop2.7/datasets

# optional
sc = SparkContext("local", "Tweerts and News word count")

text_file = sc.textFile("datasets/content.txt")

# words = sc.parallelize(text_file.flatMap(lambda line: line.split(" ")), 2)
# split the text inline into individual words
words = text_file.flatMap(lambda line: line.split(" "))

# set up keywords that we are looking for
keywords = ['education', 'canada', 'university', 'dalhousie', 'expensive', 'faculty', 'graduate',
            'goodschool', 'goodschools', 'badschool', 'badschools', 'poorschool', 'poorschools', 'computerscience']

# count all the words
counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
# filter those that required by the assignment
counts = counts.filter(lambda x: x[0] in keywords)

counts.saveAsTextFile("reduce_result")

# copy final results
# cp -i ~/spark/spark-2.4.4-bin-hadoop2.7/datasets/reduce_result/* ~/DataMngAssignmentTwo/results
