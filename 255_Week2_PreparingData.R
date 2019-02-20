### 255 - Week 2 ###
#this week we are going to learn how to ingest a directory of text files and
#prepare them for analysis
#we can do this by using the TM package

### TM Package ###
library("tm")
library("SnowballC")

#set your working directory
setwd("~/Documents/6. Teaching/255 Intro to Text Mining/255 - Data")

#read in yoru corpus
corpus1 <- VCorpus(DirSource("NonNovel_English_Contemporary_Mixed", encoding = "UTF-8"), readerControl=list(language="English"))

#clean your data
#strip white space
corpus1 <- tm_map(corpus1, content_transformer(stripWhitespace)) 
#make all lowercase
corpus1 <- tm_map(corpus1, content_transformer(tolower))
#remove numbers
corpus1 <- tm_map(corpus1, content_transformer(removeNumbers))
#remove stopwords
corpus1 <- tm_map(corpus1, removeWords, stopwords("English"))
#remove punctuation
corpus1 <- tm_map(corpus1, content_transformer(removePunctuation))
#stem words
#corpus1 <- tm_map(corpus1, stemDocument, language = "english")

#create a document term matrix
corpus1.dtm<-DocumentTermMatrix(corpus1, control=list(wordLengths=c(1,Inf)))
corpus1.matrix<-as.matrix(corpus1.dtm, stringsAsFactors=F)

#perform transformations on the raw counts

#Method 0: Remove sparse terms
#lower number = requires that a word be in more documents
#so 0.1 says that words need to be in 90% of documents to be included
corpus1.dtm.sparse<-removeSparseTerms(corpus1.dtm, 0.4) 
corpus1.matrix.sparse<-as.matrix(corpus1.dtm.sparse, stringsAsFactors=F)

#inspect your column names
colnames(corpus1.matrix.sparse)

#Method 1: Scaling
#first get total word count for each work and save in a variable
scaling1<-rowSums(corpus1.matrix)
#then divide word counts by total words to turn values into percentages
corpus1.scaled<-corpus1.matrix.sparse/scaling1 

#Method 2: tfidf
#tfidf = term frequency * inverse document frequency
#this weights words by how infrequent they are in the corpus
#the more infrequent they are across documents the higher the word's score
corpus1.tfidf<-weightTfIdf(corpus1.dtm, normalize = TRUE)
corpus1.tfidf.matrix<-as.matrix(corpus1.tfidf, stringsAsFactors=F)


