### 255 - Week 1 ###

#load libraries
library("ggplot2")

#set working directory
setwd("~/Documents/6. Teaching/255 Intro to Text Mining/255 - Lesson Plans/255 - Week 1")

#### TTR - First 10K Words ####

#load work
work<-scan("1813_Austen,Jane_PrideandPrejudice_Novel.txt", what="character", quote="") 
#work<-scan("1922_Joyce,James_Ulysses_Novel.txt", what="character", quote="")
#clean -- good hygiene is essential!
work.clean<-tolower(work) #all lowercase
work.clean<-gsub("'", "", work.clean) #remove apostrophes
work.clean<-gsub("\\d", "", work.clean) #remove numbers
work.clean<-unlist(strsplit(work.clean, "\\W")) #remove punctuation
work.clean<-work.clean[work.clean != ""] #remove blanks
#test for whole work
length(unique(work.clean))/length(work.clean)
#test for first N words
section<-work.clean[1:50000] #subset your novel by first N words
length(unique(section))/length(section) #calculate your measure
  
#test correlations
#does your measure correlate with the length of the document?
#if so, then you have discovered a way of predicting how long something is!
#load table
ttr.test<-read.csv("English150_Master.csv", header=T)

#plot
plot(ttr.test$count, ttr.test$ttr_all)

#run cor.test for all words v. length (=count)
cor.test(ttr.test$count, ttr.test$ttr_all)

#run cor.test for first 23K words
cor.test(ttr.test$count, ttr.test$ttr_23K)
plot(ttr.test$count, ttr.test$ttr_23K)

#test on date
cor.test(ttr.test$date, ttr.test$ttr_23K)
plot(ttr.test$date, ttr.test$ttr_23K)
hist(ttr.test$date)

#nicer visualization
ggplot(ttr.test, aes(x=count, y=ttr_all)) +
  geom_point() +
  geom_text(aes(label=author_unique), size=4, hjust=0) +
  xlab("Length in Words") +
  ylab("Percentage of Unique Words") +
  ggtitle("Correlation between Length and Vocabulary Richness") + 
  stat_smooth(method=loess)
  #stat_smooth(method=loess, colour="black")
  #stat_smooth(method=lm, colour="black")
  #stat_smooth(method=lm)

### Zipf's Law ###
#this takes work.clean from above
novel.freqs<-sort(table(work.clean), decreasing=T) #this creates a table of word frequencies in descending order
plot(novel.freqs[1:2000]) # plots raw frequency of top 2000 words
rel.freqs<-100*(novel.freqs/sum(novel.freqs)) # turning raw hits into percentages
plot(rel.freqs[1:100], type="b", xlab="Top Ten Words in Pride and Prejudice by Frequency", ylab="Percentage of Full Text",xaxt = "n")
axis(1,1:100, labels=names(rel.freqs [1:100]))

### LINEAR REGRESSION ###

#load your data
inter<-read.csv("Christie_Data.csv", header=T)

#plot your data
#x = Age (Predictor), y = TTR (Response)
plot(inter$age, inter$types, xlab="Age", ylab="Unique Words", main="No. Word Types in Agatha Christie")

#run a linear regression model
inter.lm<-lm(types ~ age, data=inter) #predictor (x) goes second, response (y) goes first
lines(inter$age, predict(inter.lm), col="black") #use predictor (x) as first variable
#influence.measures(inter.lm) #this identifies potential outliers with an asterisk

#get a summary of your model to assess goodness of fit
summary(inter.lm)

#for other Christie measures
plot(inter$age, inter$repeats, xlab="Age", ylab="Repeated Phrases", main="No. Repeated Phrases in Agatha Christie")
inter.lm<-lm(repeats ~ age, data=inter) # measure goes first, x value second
lines(inter$age, predict(inter.lm), col="black") #x-axis as first variable
#influence.measures(inter.lm) #this identifies potential outliers with an asterisk
summary(inter.lm)

plot(inter$age, inter$indefinite, xlab="Age", ylab="Indefinite Words", main="Percentage Indefinite Words in Agatha Christie")
inter.lm<-lm(indefinite ~ age, data=inter) # measure goes first, x value second
lines(inter$age, predict(inter.lm), col="black") #x-axis as first variable
#influence.measures(inter.lm) #this identifies potential outliers with an asterisk
summary(inter.lm)

#Extra Credit: increase polynomial
inter.lm2<-lm(types ~ age + I(age^2), data=inter)
lines(inter$age, predict(inter.lm2), col="red")
summary(inter.lm2)
inter.lm3<-lm(comma ~ id + I(id^2) + I(id^3), data=inter)
lines(inter$id, predict(inter.lm3), col="blue")
summary(inter.lm3)
inter.lm4<-lm(punct.dist ~ index + I(index^2) + I(index^3) + I(index^4), data=rhythm)
