### 255 Week 5 ###
#this week we will learn how to classify texts using the process of machine learning

setwd("~/Documents/6. Teaching/255 Intro to Text Mining/255 - Data")

##### Classification Using Machine Learning #######
library("kernlab")
library("caret")
library("tm")
library("SnowballC")
library("splitstackshape")
library("e1071")

#Step 1: read in corpus1
corpus1 <- VCorpus(DirSource("NovelEnglishGenderSample", encoding = "UTF-8"), readerControl=list(language="English"))

#clean your data
corpus1 <- tm_map(corpus1, content_transformer(stripWhitespace))
corpus1 <- tm_map(corpus1, content_transformer(tolower))
corpus1 <- tm_map(corpus1, content_transformer(removeNumbers))
#corpus1 <- tm_map(corpus1, removeWords, stopwords("English")) ## inspect your stopword lists
corpus1 <- tm_map(corpus1, content_transformer(removePunctuation))
#corpus1 <- tm_map(corpus1, stemDocument, language = "english") # stem your words

#create your document term matrix
corpus1.dtm<-DocumentTermMatrix(corpus1, control=list(wordLengths=c(1,Inf)))
corpus1.matrix<-as.matrix(corpus1.dtm, stringsAsFactors=F)

#perform transformations on the raw counts

#Remove sparse terms
corpus1.dtm.sparse<-removeSparseTerms(corpus1.dtm, 0.4) #lower number = requiring that a word be in more documents
corpus1.matrix.sparse<-as.matrix(corpus1.dtm.sparse, stringsAsFactors=F)

#Scale your data
scaling1<-rowSums(corpus1.matrix) #get total word counts for each work
corpus1.scaled<-corpus1.matrix.sparse/scaling1 

## OR decide on most frequent term ranges
#establish the number of words to use
n=3000

#get top N words
top.words<-sort(colSums(corpus1.matrix), decreasing = T)[1:n]
corpus1.matrix.sub<-corpus1.matrix[,colnames(corpus1.matrix) %in% names(top.words)]
scaling1<-rowSums(corpus1.matrix) #get total word counts for each work
corpus1.scaled<-corpus1.matrix.sub/scaling1 

#Label your data

#if the data is prelabeled use this section
label.df<-data.frame(row.names(corpus1.scaled))
colnames(label.df)<-c("filenames")
label.df<-cSplit(label.df, 'filenames', sep="_", type.convert=FALSE)
corpus1.scaled<-data.frame(corpus1.scaled)
corpus1.scaled$corpus<-label.df$filenames_1
df<-corpus1.scaled

#Step 2: Run classification test using SVM learning algorithm

#first create folds
folds<-createFolds(df$corpus, k=10) # k = number of folds (1-10) where 10 is best

#use this section to run 1x and inspect your confusion matrix
x<-folds$Fold01 #use this line of k = 10
#x<-folds$Fold1 #use this line if k is less than 10; change to Fold2 for the second fold etc.
df.train<-df[-x,]
df.test<-df[x,]
df.model<-ksvm(corpus ~ ., data=df.train, kernel="rbfdot")
df.pred<-predict(df.model, df.test)
con.matrix<-confusionMatrix(df.pred, df.test$corpus, positive = "Male")
con.matrix$byClass[[7]] #F1 score (combination of precision and recall)
con.matrix$overall[[6]] #pvalue

#run x-fold cross validation
cv.results<-lapply(folds, function(x){
  df.train<-df[-x,]
  df.test<-df[x,]
  df.model<-ksvm(corpus ~ ., data=df.train, kernel="rbfdot")
  df.pred<-predict(df.model, df.test)
  con.matrix<-confusionMatrix(df.pred, df.test$corpus, positive = "Female")
  f1<-con.matrix$byClass[[7]] 
})
unlist(cv.results) #this shows you the F1 score for each fold
mean(unlist(cv.results)) #this is the average F1 score for all folds
sd(unlist(cv.results))

#### if you have two separate directories ####

#read in corpus1
corpus1 <- VCorpus(DirSource("Pop_Songs_Sample", encoding = "UTF-8"), readerControl=list(language="English"))

#clean your data
corpus1 <- tm_map(corpus1, content_transformer(stripWhitespace))
corpus1 <- tm_map(corpus1, content_transformer(tolower))
corpus1 <- tm_map(corpus1, content_transformer(removeNumbers))
corpus1 <- tm_map(corpus1, removeWords, stopwords("English"))
corpus1 <- tm_map(corpus1, content_transformer(removePunctuation))
#corpus1 <- tm_map(corpus1, stemDocument, language = "english")

#create your document term matrix
corpus1.dtm<-DocumentTermMatrix(corpus1, control=list(wordLengths=c(1,Inf)))
corpus1.matrix<-as.matrix(corpus1.dtm, stringsAsFactors=F)

#perform transformations on the raw counts
scaling1<-rowSums(corpus1.matrix) #get total word counts for each work
corpus1.scale<-corpus1.matrix/scaling1 #turn counts into percentages 

#read corpus 2
corpus2 <- VCorpus(DirSource("20thCSample2", encoding = "UTF-8"), readerControl=list(language="English"))
corpus2 <- tm_map(corpus2, content_transformer(stripWhitespace))
corpus2 <- tm_map(corpus2, content_transformer(tolower))
corpus2 <- tm_map(corpus2, content_transformer(removeNumbers))
corpus2 <- tm_map(corpus1, removeWords, stopwords("English"))
corpus2 <- tm_map(corpus2, content_transformer(removePunctuation))
#corpus2 <- tm_map(corpus2, stemDocument, language = "english")
corpus2.dtm<-DocumentTermMatrix(corpus2, control=list(wordLengths=c(1,Inf)))
corpus2.matrix<-as.matrix(corpus2.dtm, stringsAsFactors=F)
scaling2<-rowSums(corpus2.matrix)
corpus2.scale<-corpus2.matrix/scaling2 

#downsample your collections to speed up run time
df1.samp<-corpus1.scale[sample(nrow(corpus1.scale), 1000),]
df2.samp<-corpus2.scale[sample(nrow(corpus2.scale), 1000),]

df1.samp<-df1.samp[,colnames(df1.samp) %in% colnames(df2.samp)]
df2.samp<-df2.samp[,colnames(df2.samp) %in% colnames(df1.samp)]
which(!colnames(df2.samp) %in% colnames(df1.samp))

#merge
df3<-rbind(df1.samp, df2.samp)
df3<-df3[complete.cases(df3),]

#remove problem words
probs<-c("rsquo", "lsquo")
df3<-df3[,!colnames(df3) %in% probs]

#establish the number of words to use
n=3000

#get top N words
top.words<-sort(colSums(df3), decreasing = T)[1:3000]

#subset by top words
df1<-df1.samp[,colnames(df1.samp) %in% names(top.words)]
df2<-df2.samp[,colnames(df2.samp) %in% names(top.words)]

#check to see if the column names are identical
which(!colnames(df1) %in% colnames(df2))

#turn into data frames to add labels
df1<-data.frame(df1)
df2<-data.frame(df2)

#append a column with the corpus label to each data frame
df1$corpus<-c("POP")
df2$corpus<-c("POET")

#combine data frames
df<-rbind(df1, df2)

#remove bad rows
df<-df[complete.cases(df),]

#remove rows w sum 0
df<-df[which(rowSums(df[1:n]) != 0),]

#run your validation

#first create folds
folds<-createFolds(df$corpus, k=10) # k = number of folds (1-10) where 10 is best

#use this section to run 1x and inspect your confusion matrix
x<-folds$Fold01 #use this line of k = 10
#x<-folds$Fold1 #use this line if k is less than 10; change to Fold2 for the second fold etc.
df.train<-df[-x,]
df.test<-df[x,]
df.model<-ksvm(corpus ~ ., data=df.train, kernel="rbfdot")
df.pred<-predict(df.model, df.test)
con.matrix<-confusionMatrix(df.pred, df.test$corpus, positive = "POP")
con.matrix$byClass[[7]] #F1 score (combination of precision and recall)
con.matrix$overall[[6]] #pvalue

#run x-fold cross validation
cv.results<-lapply(folds, function(x){
  df.train<-df[-x,]
  df.test<-df[x,]
  df.model<-ksvm(corpus ~ ., data=df.train, kernel="rbfdot")
  df.pred<-predict(df.model, df.test)
  con.matrix<-confusionMatrix(df.pred, df.test$corpus, positive = "POP")
  f1<-con.matrix$byClass[[7]] 
})
unlist(cv.results) #this shows you the F1 score for each fold
mean(unlist(cv.results)) #this is the average F1 score for all folds
sd(unlist(cv.results))

#run this code to prepare your data to test individual words
#here you are matching your raw count tables to your scaled ones that have been sampled and reduced vocabulary
df1.raw<-corpus1.matrix[row.names(corpus1.matrix) %in% row.names(df1),colnames(corpus1.matrix) %in% colnames(df1)]
df2.raw<-corpus2.matrix[row.names(corpus2.matrix) %in% row.names(df2),colnames(corpus2.matrix) %in% colnames(df2)]
df1.raw<-df1.raw[,which(colnames(df1.raw) %in% colnames(df2.raw))]
df2.raw<-df2.raw[,which(colnames(df2.raw) %in% colnames(df1.raw))]
which(colnames(df1.raw) != colnames(df2.raw))

#now you can go run the code from Week 3 line 233

