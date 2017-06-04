plot6 <- function()
{
  # get reshape2 and ggplot2 libraries
  library(reshape2)
  library(ggplot2)
  
  # open main data sets
  NEI <- readRDS("summarySCC_PM25.rds")
  SCC <- readRDS("Source_Classification_Code.rds")
  
  # create the baltimore data set
  BAL <- NEI[NEI$fips=="24510",]
  
  # create the los angeles data set
  LA <- NEI[NEI$fips=="06037",]
  
  # extract motor vehicle related sources 
  # using "On-Road" and "Vehicle" from the EI.Sector variable as the definition
  MOTOR_SCC_CODES <- as.character(SCC[grep("On-Road",SCC$EI.Sector),1])
  
  # get the sum of the emissions for baltimore county by SCC
  BAL_SCC_sum <-tapply(BAL$Emissions,list(BAL$SCC,BAL$year),sum,na.rm=TRUE) 
  
  # get the sum of the emissions for los angeles county by SCC
  LA_SCC_sum <-tapply(LA$Emissions,list(LA$SCC,LA$year),sum,na.rm=TRUE)
 
  # make data.frame for baltimore data
  BAL_SCC_sum <- data.frame(BAL_SCC_sum)
  BAL_SCC_sum <- cbind(row.names(BAL_SCC_sum),BAL_SCC_sum)
  colnames(BAL_SCC_sum) <- c("SCC","1999","2002","2005","2008")  
 
  # make data.frame for Los Angeles data
  LA_SCC_sum <- data.frame(LA_SCC_sum)
  LA_SCC_sum <- cbind(row.names(LA_SCC_sum),LA_SCC_sum)
  colnames(LA_SCC_sum) <- c("SCC","1999","2002","2005","2008")  
  
  # locate the SCC codes for Motor Vehicles in the BAL Totals for the SCCs
  BAL_MOTOR_sum <- BAL_SCC_sum[as.character(BAL_SCC_sum$SCC) %in% MOTOR_SCC_CODES,]
  
  # locate the SCC codes for Motor Vehicles in the LA Totals for the SCCs
  LA_MOTOR_sum <- LA_SCC_sum[as.character(LA_SCC_sum$SCC) %in% MOTOR_SCC_CODES,]
  
  # create a vector with the sums of the emmissions according to year (BAL)
  TOTAL_BAL_MOTOR <- colSums(BAL_MOTOR_sum[,-1],na.rm=TRUE)
  
  # create a vector with the sums of the emmissions according to year (LA)
  TOTAL_LA_MOTOR <- colSums(LA_MOTOR_sum[,-1],na.rm=TRUE)
  
  # arrange data to be used in ggplot command
  PLOT_DATA <- rbind(TOTAL_BAL_MOTOR,TOTAL_LA_MOTOR)
  PLOT_DATA <- data.frame(PLOT_DATA)
  
  # add a column in the data for the cities
  PLOT_DATA <- cbind(PLOT_DATA,c("BAL","LA"))
  colnames(PLOT_DATA) <- c("1999","2002","2005","2008","CITY")
  
  # transpose the data to allow for easier implementation of ggplot
  PLOT_DATA <- melt(PLOT_DATA)
 
  # add colnames for last version of data
  colnames(PLOT_DATA) <- c("CITY","year","emissions") 
  
  # format emissions column in PLOT_DATA
  PLOT_DATA[,3] <- format(PLOT_DATA$emissions,digits=0)
  
  # create a plot for the data
  ggplot(PLOT_DATA,aes(x=year,y=emissions,fill=CITY,label=emissions)) + 
         geom_bar(stat="identity", position=position_dodge()) + 
         ggtitle("Total Emissions from Motor Vehicles in Baltimore and Los Angeles") + 
         xlab("YEAR") + ylab("Total Emissions (in tons)") + 
         geom_text(vjust=-0.25,hjust=1,color="black")
 
 
  # write plot to PNG file
  ggsave("plot6.png")         # save plot to file 
  dev.off()                   # close PNG device                                              # close PNG device
 
}  


