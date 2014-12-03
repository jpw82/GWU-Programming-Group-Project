#to get RMySQL in Ubuntu: sudo apt-get install r-cran-rmysql  (it would install using install.packages in RStudio)
library(RMySQL)

##ADJUST THESE PARAMETERS IF YOU ARE RUNNING THIS PROGRAM ON A NEW COMPUTER
Rdbcnx <- dbConnect(MySQL(), user="root", password = "root", dbname="MLB", host="localhost")

#import the data frame from RMySQL
MLBDF2014 <- dbReadTable(Rdbcnx, "mlbdf2014")

#Rename dataframe and columns to match earlier code
colnames(MLBDF2014) <- c("Team", "Win.", "avgSB", "avgSO", "avgHits","avgDoubles","avgTriples","avgHRs")

#Now Bring in each of the individual stat tables
SBtable       <- dbReadTable(Rdbcnx, "SBtable")
SOtable       <- dbReadTable(Rdbcnx, "SOtable")
Hitstable     <- dbReadTable(Rdbcnx, "Hitstable")
Doublestable  <- dbReadTable(Rdbcnx, "Doubletable")
Triplestable  <- dbReadTable(Rdbcnx, "Tripletable")
HRtable       <- dbReadTable(Rdbcnx, "HRtable")
Wintable      <- dbReadTable(Rdbcnx, "Wintable")


#if transferring data via CSV instead of MySQL table, use this:
#MLBDF2014 = read.csv("C:\\Users\\Nayden\\Desktop\\MSBA Files\\Programming for Analytics\\Group Project\\mlbdf2014.csv")

MLBNovTwitter = read.csv("NovTwitterScore.csv")
library(ggplot2)


r2WinsvsSB = format(summary(lm(MLBDF2014$Win.~MLBDF2014$avgSB))$r.squared, digits = 3)
WinsVsSBPlot = qplot(MLBDF2014$avgSB, MLBDF2014$Win., geom=c("point", "smooth"), method="lm", xlab="Average Stolen Bases", ylab="Percent Wins in Season")

r2WinsvsSO = format(summary(lm(MLBDF2014$Win.~MLBDF2014$avgSO))$r.squared, digits = 3)
WinsVsSOPlot = qplot(MLBDF2014$avgSO, MLBDF2014$Win., geom=c("point", "smooth"), method="lm", xlab="Average Strikeouts", ylab="Percent Wins in Season")

r2WinsvsHits = format(summary(lm(MLBDF2014$Win.~MLBDF2014$avgHits))$r.squared, digits = 3)
WinsVsHitsPlot = qplot(MLBDF2014$avgHits, MLBDF2014$Win., geom=c("point", "smooth"), method="lm", xlab="Average Hits", ylab="Percent Wins in Season")

r2WinsvsDoubles = format(summary(lm(MLBDF2014$Win.~MLBDF2014$avgDoubles))$r.squared, digits = 3)
WinsVsDoublesPlot = qplot(MLBDF2014$avgDoubles, MLBDF2014$Win., geom=c("point", "smooth"), method="lm", xlab="Average Doubles", ylab="Percent Wins in Season")

r2WinsvsTriples = format(summary(lm(MLBDF2014$Win.~MLBDF2014$avgTriples))$r.squared, digits = 3)
WinsVsTriplesPlot = qplot(MLBDF2014$avgTriples, MLBDF2014$Win., geom=c("point", "smooth"), method="lm", xlab="Average Triples", ylab="Percent Wins in Season")

r2WinsvsHRs = format(summary(lm(MLBDF2014$Win.~MLBDF2014$avgHRs))$r.squared, digits = 3)
WinsVsHRsPlot = qplot(MLBDF2014$avgHRs, MLBDF2014$Win., geom=c("point", "smooth"), method="lm", xlab="Average Homeruns", ylab="Percent Wins in Season")

require(grid)
vp.layout <- function(x, y) viewport(layout.pos.row=x, layout.pos.col=y)
arrange_ggplot2 <- function(..., nrow=NULL, ncol=NULL, as.table=FALSE) {
  dots <- list(...)
  n <- length(dots)
  if(is.null(nrow) & is.null(ncol)) { nrow = floor(n/2) ; ncol = ceiling(n/nrow)}
  if(is.null(nrow)) { nrow = ceiling(n/ncol)}
  if(is.null(ncol)) { ncol = ceiling(n/nrow)}
  grid.newpage()
  pushViewport(viewport(layout=grid.layout(nrow,ncol) ) )
  ii.p <- 1
  for(ii.row in seq(1, nrow)){
    ii.table.row <- ii.row
    if(as.table) {ii.table.row <- nrow - ii.table.row + 1}
    for(ii.col in seq(1, ncol)){
      ii.table <- ii.p
      if(ii.p > n) break
      print(dots[[ii.table]], vp=vp.layout(ii.table.row, ii.col))
      ii.p <- ii.p + 1
    }
  }
}

arrange_ggplot2(WinsVsSBPlot,WinsVsSOPlot,WinsVsHitsPlot,WinsVsDoublesPlot,WinsVsTriplesPlot,WinsVsHRsPlot,ncol=3)

r2TwitterVsWins = format(summary(lm(MLBNovTwitter$NovTwitterScore~MLBDF2014$Win.))$r.squared, digits = 3)
TwitterVsWins = qplot(MLBDF2014$Win., MLBNovTwitter$NovTwitterScore, geom=c("point", "smooth"), method="lm", xlab="Win Percentage", ylab="Twitter Sentiment Score")
TwitterVsWins

RSquared = c(r2WinsvsSB, r2WinsvsSO, r2WinsvsHits, r2WinsvsDoubles, r2WinsvsTriples, r2WinsvsHRs, r2TwitterVsWins)
Analysis = c("Wins vs Stolen Bases R Squared", "Wins vs Strikeouts R Squared", "Wins vs Hits R Squared", "Wins vs Doubles R Squared", "Wins vs Triples R Squared", "Wins vs Homeruns R Squared","Twitter Sentiment Score vs Wins R Squared")
R2Table = data.frame(Analysis, RSquared)
