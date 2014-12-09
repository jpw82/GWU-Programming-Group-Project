# Rely on the 'WorldPhones' dataset in the datasets
# package (which generally comes preloaded).
library(datasets)
mlbdf2014 <- read.csv("~/Downloads/Shiny/mlbdf2014.csv")
MLBNovTwitter <- read.csv("~/Downloads/Shiny/NovTwitterScore.csv")
R2Table <- read.csv("~/Downloads/Shiny/R2Table.csv")

colnames(mlbdf2014) = c("Team", 
                        "WinningPercentage", 
                        "Avg. Stolen Bases", 
                        "Avg. Strikeouts", 
                        "Avg. Hits", 
                        "Avg. Doubles",
                        "Avg. Triples",
                        "Avg. HRs")

# Define the overall UI
shinyUI(
  
  # Use a fluid Bootstrap layout
  navbarPage("Baseball-Statististics",  
    # Give the page a title
    tabPanel("MLB Winning Percentage Indicators",
    
    # Generate a row with a sidebar
    sidebarLayout(      
      
      # Define the sidebar with one input
      sidebarPanel(
        selectInput("statistic", "Statistic:", 
                    choices= colnames(mlbdf2014[3:8])),
        hr(),
        helpText("Data from www.baseball-reference.com.")
      ),
      
      # Create a spot for the barplot
      mainPanel(
        plotOutput("mlbPlot")  
      )
    ),
    
  tabPanel("Summary",
           verbatimTextOutput("summary") 
      )
    ),
  
  #Twitter and R2 tab
  tabPanel("Analysis",
    plotOutput("twitter"),
    tableOutput('twitterdata')
  ),
  
  #MLB Data tab
  tabPanel("MLB Data",
  sidebarLayout(         
     sidebarPanel(
       conditionalPanel(
         'input.dataset === "mlbdf2014"',
         checkboxGroupInput('show_vars', 'Columns in dataset to show:',
                            names(mlbdf2014), selected = names(mlbdf2014))
       )
    ),
     mainPanel(
       tabsetPanel(
         id = 'dataset',
         tabPanel('mlbdf2014', dataTableOutput('mytable'))) 
     )         
    )       
  ),
  
  #Predictive Tools tab
  tabPanel("Predictive Tools",
  fluidPage(
    titlePanel("MLB Wins Calculator"),
    fluidRow(
      column(4, wellPanel(
        sliderInput("StolenBases", "Stolen Bases:",
                    min = 0, max = 1, value = 0, step = .01),
        sliderInput("Strikeouts", "Strikeouts:",
                    min = 0, max = 20, value = 0, step = .1),
        sliderInput("Hits", "Hits:",
                    min = 0, max = 20, value = 0, step = .1),
        sliderInput("Doubles", "Doubles:",
                    min = 0, max = 1, value = 0, step = .01),
        sliderInput("Triples", "Triples:",
                    min = 0, max = 1, value = 0, step = .01),
        sliderInput("HomeRuns", "Home Runs:",
                    min = 0, max = 5, value = 0, step = .1)
      )),
      column(8,
             verbatimTextOutput("text1"),
             br(),
             br()
             
      )
    )
  )
))
)

