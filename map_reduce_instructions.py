# copy cleaned data to the dataset directory for map/reduce program
# cp -i ~/DataMngAssignmentTwo/content.txt ~/spark/spark-2.4.4-bin-hadoop2.7/datasets

# optional
sc = SparkContext("local", "Tweerts and News word count")

text_file = sc.textFile("datasets/content.txt")

# words = sc.parallelize(text_file.flatMap(lambda line: line.split(" ")), 2)
words = text_file.flatMap(lambda line: line.split(" "))

counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

counts.saveAsTextFile("reduce_result")

# copy final results
# cp -i ~/spark/spark-2.4.4-bin-hadoop2.7/datasets/reduce_result/* ~/DataMngAssignmentTwo/results
