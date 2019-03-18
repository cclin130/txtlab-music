### 255 - Week 3 ###
#this week we are going to learn a variety of ways of comparing features between
#two text collections

### Part 1: Comparing a single feature between two collections ###

#load your packages
library("tm")
library("SnowballC")

#set your working directory
setwd("~/Documents/6. Teaching/255 Intro to Text Mining/255 - Data")

#read in corpus1
corpus1 <- VCorpus(DirSource("Novel_Combined", encoding = "UTF-8"), readerControl=list(language="English"))

#clean your data
corpus1 <- tm_map(corpus1, content_transformer(stripWhitespace))
corpus1 <- tm_map(corpus1, content_transformer(tolower))
corpus1 <- tm_map(corpus1, content_transformer(removeNumbers))
#corpus1 <- tm_map(corpus1, removeWords, stopwords("English"))
corpus1 <- tm_map(corpus1, content_transformer(removePunctuation))
corpus1 <- tm_map(corpus1, stemDocument, language = "english")

#create your document term matrix
corpus1.dtm<-DocumentTermMatrix(corpus1, control=list(wordLengths=c(1,Inf)))
corpus1.matrix<-as.matrix(corpus1.dtm, stringsAsFactors=F)

#perform transformations on the raw counts
scaling1<-rowSums(corpus1.matrix) #get total word counts for each work
corpus1.scale<-corpus1.matrix/scaling1 #turn counts into percentages 

#read corpus 2
corpus2 <- VCorpus(DirSource("ShortStories_English", encoding = "UTF-8"), readerControl=list(language="English"))
corpus2 <- tm_map(corpus2, content_transformer(stripWhitespace))
corpus2 <- tm_map(corpus2, content_transformer(tolower))
corpus2 <- tm_map(corpus2, content_transformer(removeNumbers))
#corpus2 <- tm_map(corpus1, removeWords, stopwords("English"))
corpus2 <- tm_map(corpus2, content_transformer(removePunctuation))
#corpus2 <- tm_map(corpus2, stemDocument, language = "english")
corpus2.dtm<-DocumentTermMatrix(corpus2, control=list(wordLengths=c(1,Inf)))
corpus2.matrix<-as.matrix(corpus2.dtm, stringsAsFactors=F)
scaling2<-rowSums(corpus2.matrix)
corpus2.scale<-corpus2.matrix/scaling2 

#extract feature of interest

#list all words in the corpus
colnames(corpus1.matrix)
#find the column # where your word of interest is
which(colnames(corpus1.matrix) == "clue")
#create a list of words to extract
myWords<-c("the", "this", "that", "these", "those")
#myWords<-c("i", "me", "my", "mine")
#myWords<-c("she", "he")

#extract list of words for each corpus
corpus1.feature<-corpus1.scale[,colnames(corpus1.scale) %in% myWords]
corpus2.feature<-corpus2.scale[,colnames(corpus2.scale) %in% myWords]

#add code for reading in csv

#sum their frequencies
feature.sum1<-rowSums(corpus1.feature)
feature.sum2<-rowSums(corpus2.feature)

#compare their means / medians

#Step 1: observe the distribution of your feature in your data
#this creates a histogram
#a histogram allows you to observe the frequency with which a given value appears
#i.e. how many documents have a feature that appears 10% of the time
hist(feature.sum1)
hist(feature.sum2)

#another way to understand the distribution of your feature is to run a summary
#this tells you min/max, median/mean, and quartile values
summary(feature.sum1)
summary(feature.sum2)

#Step 2: observe it relative to a normal distribution
hist(feature.sum1, prob=T)
curve(dnorm(x, mean=mean(feature.sum1), sd=sd(feature.sum1)), add=TRUE)
hist(feature.sum2, prob=T)
curve(dnorm(x, mean=mean(feature.sum2), sd=sd(feature.sum2)), add=TRUE)

#step 3: test for normality
shapiro.test(feature.sum1) # when p < 0.05 it means it is NOT normally distributed
shapiro.test(feature.sum2)

#step 4: IF there is a normal distribution, then run a Welch's two sample t-test
t.test(feature.sum1, feature.sum2)

#remember to report standard deviations with your means
sd(feature.sum1)
sd(feature.sum2)

#plot the two distributions on the same graph
plot(density(feature.sum1))
lines(density(feature.sum2), lty=2)
abline(v=mean(feature.sum1))
abline(v=mean(feature.sum2), lty=2)

#step 4a: IF your data is not normally distributed, then run a Wilcoxon Rank Sum Test
wilcox.test(feature.sum1, feature.sum2)
#report the medians rather than the means
median(feature.sum1)
median(feature.sum2)
#report how much higher/lower median1 is to median2
median(feature.sum1)/median(feature.sum2)
#2.5 = "The median value of my feature is 2.5 times higher in group 1 than it is in group 2..."

#here is a dummy example of normally distributed data with a normal distribution curve attached
hist(rnorm(100, mean = 5, sd = 3), prob=T)
curve(dnorm(x, mean=5, sd=3), add=TRUE)

### Fisher's Exact Test ###

#this test doesn't consider the distribution of a word/feature in a collection but simply
#looks at the overall count within a group to assess whether the ratio is considerably higher
#in one group versus another
#chi.sq test is similar

#first step is construct what is called a contingency table

#         Corpus A    Corpus B
#Word       x           y
#NotWord    z           w

#make new features using raw counts
corpus1.feature.raw<-corpus1.matrix[,colnames(corpus1.matrix) %in% myWords]
corpus2.feature.raw<-corpus2.matrix[,colnames(corpus2.matrix) %in% myWords]

#fill table values
x<-sum(corpus1.feature.raw) #sum of the feature of interest in A
y<-sum(corpus2.feature.raw) #sum of the feature of interest in B
z<-sum(corpus1.matrix)-sum(corpus1.feature.raw) #all words in A minus feature of interest
w<-sum(corpus2.matrix)-sum(corpus2.feature.raw) #all words in B minus feature of interest

#create table
df<-data.frame(c(x,z), c(y,w))
row.names(df)<-c("Word", "NotWord")
colnames(df)<-c("A", "B")

#run test
fisher.test(df) #odds ratio tells you how much more prevalent the feature is in A v. B

### Part 2 Testing for Distinctive Words ###

#this section uses the two DTMs from above:
#corpus1.scale
#corpus2.scale

#In order to understand what words are distinctive of a target corpus, we need to run
#a statistical test in order to understand if that word's occurrence is significantly
#more or less frequent in one group than another.
#the following approaches can be used depending on your goals:

#a. Wilcoxon Rank Sum Test
#this test is useful because it looks at the overall distribution of a word in a given sample
#if a single document or just a few documents have very high counts of that word
#this test won't be biased in their favor. 
#This test is less appropriate for short documents or words with very small counts or if you 
#want to consider your documents all together rather than individually.

#b. Fisher's Exact Test
#this test is useful because it gives you the exact odds ratio between a word's appearance
#in one group versus another. It is good at answering how much more likely a given word is going to appear in 
#group A versus group B. It allows you to look at both increased and decreased likelihood,
#as well as subset by significance -- keeping only those words that have a p-value of less
#than 0.05, i.e. those words whose increase/decrease is statistically significant.
#its weakness is that very infrequent words are more likely to have a higher odds ratio
#because the swings on a few occurrences will look much higher than swings on words that appear
#very often (like pronouns). One way around this is to set an arbitrary cut-off: only
#keep words that appear more than N times, where N is some meaningful cut-off (roughly 1x or
#2x per document etc.)

#c. Dunning's Log-Likelihood Ratio, known as G2 (g-squared)
#this test is very good because it finds a balance between words that appear often and those
#that don't. It cannot give you a statistical cut-off however and it requires that you 
#consider all your documents together -- so words that appear extra-high in a few
#documents could impact your results. It tends to favor words that appear more often versus those
#that appear more rarely. So it will give different results than Fisher's.

#Test for top N words
n=3000

#merge your tables
df3<-merge(corpus1.matrix, corpus2.matrix, all=T)

#get top N words
top.words<-sort(colSums(df3), decreasing = T)[1:3000]

#subset by top words
df1<-corpus1.scale[,colnames(corpus1.scale) %in% names(top.words)]
df2<-corpus2.scale[,colnames(corpus2.scale) %in% names(top.words)]

#create matching tables of raw counts
df1.raw<-corpus1.matrix[,colnames(corpus1.matrix) %in% names(top.words)]
df2.raw<-corpus2.matrix[,colnames(corpus2.matrix) %in% names(top.words)]

#check to see if the column names are identical
which(!colnames(df1) %in% colnames(df2))

### Rank Sum Test ###

#run a test for each feature (i.e. word)
rank.df<-NULL
for (j in 1:ncol(df1)){
  rnk<-wilcox.test(df1[,j], df2[,j])
  median.a<-median(df1[,j])
  median.b<-median(df2[,j])
  p<-rnk$p.value
  word<-colnames(df1)[j]
  ratio<-median.a/median.b
  temp.df<-data.frame(word, median.a, median.b, p, ratio)
  rank.df<-rbind(rank.df, temp.df)
}
#sort your table by the ratio of the medians for each word
wilcox.df<-rank.df[order(-rank.df$ratio),]
#remove any words that are not statistically significant
#here we use 0.05 as our threshold
#but we also use a bonferoni correction and divide 0.05 by the total number of words tested

#establish new p-value
cut<-0.05/ncol(df1)

#remove all words above this threshold (i.e. not significant)
wilcox.df<-wilcox.df[wilcox.df$p < cut,]

#save the table to your hard drive
#write.csv(final.sort, file="MDW_Sherlock_RankSum.csv", row.names=F)

### Dunning's Log Likelihood + Fisher's ###
H = function(k) {N = sum(k); return(sum(k/N*log(k/N+(k==0))))}
word1<-colSums(df1.raw)
word2<-colSums(df2.raw)
all1<-sum(word1)
all2<-sum(word2)
results <- data.frame(word = colnames(df1.raw), 
                      group1=word1,
                      group2=word2,
                      G2 = 0,
                      fisher.OR = 0,
                      fisher.p = 0)
for (j in 1:ncol(df1.raw)){
  cont.table<-data.frame(c(word1[j], all1-word1[j]), c(word2[j], all2-word2[j]))
  fish<-fisher.test(cont.table)
  LLR = 2*sum(cont.table)*(H(cont.table)-H(rowSums(cont.table))-H(colSums(cont.table)))
  results$G2[j] = LLR
  results$fisher.OR[j] = fish$estimate
  results$fisher.p[j] = fish$p.value
}
#sort by G2
dunning.df<-results[order(-results$G2),]
#establish correction
cut<-0.05/ncol(df1.raw)
#remove non-significant words
dunning.df<-dunning.df[dunning.df$fisher.p < cut,] 
#the above ranks by strength either over or under expected values
#if you want to sort by above and below, then run the following code
dunning.sort<-dunning.df
dunning.sort$diff<-dunning.sort$group1-dunning.sort$group2
G2_Sort.v<-vector()
for (i in 1:nrow(dunning.sort)){
  if (dunning.sort$diff[i] <= 0){
    G2_Sort<--dunning.sort$G2[i]
  } else {
    G2_Sort<-dunning.sort$G2[i]
  }
  G2_Sort.v<-append(G2_Sort.v, G2_Sort)
}
dunning.sort<-cbind(dunning.sort, G2_Sort.v)
dunning.sort<-dunning.sort[order(-dunning.sort$G2_Sort.v),]
#write.csv(dunning.sort, file="MDW_Sherlock_G2.csv")




