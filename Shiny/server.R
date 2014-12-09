library(shiny)
library(ggplot2)
setwd('~/Downloads/Shiny/')
mlbdf2014 <- read.csv("~/Downloads/Shiny/mlbdf2014.csv")
MLBNovTwitter <- read.csv("~/Downloads/Shiny/NovTwitterScore.csv")
R2Table <- read.csv("~/Downloads/Shiny/R2Table.csv")

#Rename the columns for better looking output
colnames(mlbdf2014) = c("Team", 
                        "WinningPercentage", 
                        "Avg. Stolen Bases", 
                        "Avg. Strikeouts", 
                        "Avg. Hits", 
                        "Avg. Doubles",
                        "Avg. Triples",
                        "Avg. HRs")

# Define a server for the Shiny app
shinyServer(function(input, output, session) {
  
  # Fill in the spot we created for a plot
  output$mlbPlot <- renderPlot({
    
    # Render a scatterplot for each indicator
    qplot(as.numeric(mlbdf2014[,input$statistic]), as.numeric(mlbdf2014$WinningPercentage),
          main= paste(input$statistic, "vs. Win Percentage", sep=" "),
          geom=c("point","smooth"),
          method="lm",
          ylab="Winning Percentage",
          xlab=input$statistic) + aes(group = 1)
  })
  
  # Render a summary of the model fit
  output$summary <- renderPrint({
    fit = lm(as.numeric(mlbdf2014[,input$statistic]) ~ as.numeric(mlbdf2014$WinningPercentage))
    summary(fit)
  })
  
  # Render a scatterplot and table of Twitter Sentiment
  output$twitter <- renderPlot({
    qplot(mlbdf2014$WinningPercentage, MLBNovTwitter$NovTwitterScore, geom=c("point", "smooth"), method="lm", xlab="Win Percentage", ylab="Twitter Sentiment Score")    
  })
  output$twitterdata <- renderTable({
    R2Table
  }, include.rownames=FALSE)
  
  # Render a data table of all MLB data
  output$mytable <- renderDataTable({
    mlbdf2014[,input$show_vars, drop = FALSE]
  })
  
  # Create a random name for the log file for MLB Predictor
  logfilename <- paste0('logfile',
                        floor(runif(1, 1e+05, 1e+06 - 1)),
                        '.txt')
  
  # This observer adds an entry to the log file every time
  # input$n changes.
  obs <- observe({    
    cat(input$StolenBases, 
        input$Strikeouts, 
        input$Hits,
        input$Doubles,
        input$Triples,
        input$HomeRuns, 
        '\n', file = logfilename, append = TRUE)
  })
  
  
  # When the client ends the session, suspend the observer.
  # Otherwise, the observer could keep running after the client
  # ends the session.
  session$onSessionEnded(function() {
    obs$suspend()
    
    # Also clean up the log file for this example
    unlink(logfilename)
  })
  
  #This is the Linear Regression Model we developed to predict winning percentage
  PredictionValue = function() {
    wins = (0.511960 + input$StolenBases*-0.009179 + input$Strikeouts*-0.030672 + input$Hits*0.033937 + input$Doubles*-0.047376 + input$Triples*-0.272945 + input$HomeRuns*0.076746)
    if(wins < 0){
      return("less than 0%. Please insert some coins and try again.")
    } else if(wins > 1){
      return("greater than 100%. This is sort of impossible, please try again.")
    }
    return(wins)  
  }
  
  #Output the Winning Percentage
  output$text1 <- renderText({
    paste0("The estimated winning percentage would be: ", PredictionValue())
  })
   
})
