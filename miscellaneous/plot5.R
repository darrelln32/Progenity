plot5 <- function()
{
  NEI <- readRDS("summarySCC_PM25.rds")
  SCC <- readRDS("Source_Classification_Code.rds")
  
  # create the baltimore data set
  BAL <- NEI[NEI$fips=="24510",]
  
  # extract motor vehicle related sources 
  # using "On-Road" and "Vehicle" from the EI.Sector variable as the definition
  MOTOR_SCC_CODES <- as.character(SCC[grep("On-Road",SCC$EI.Sector),1])
  
  # Create Baltimore Totals for the SCCs
  BAL_SCC_sum <-tapply(BAL$Emissions,list(BAL$SCC,BAL$year),sum,na.rm=TRUE) 
  
  # convert matrix into nice data frame
  BAL_SCC_sum <- data.frame(BAL_SCC_sum)
  BAL_SCC_sum <- cbind(row.names(BAL_SCC_sum),BAL_SCC_sum)
  colnames(BAL_SCC_sum) <- c("SCC","1999","2002","2005","2008")  
  
  # locate the SCC codes for Motor Vehicles in the BAL Totals for the SCCs
  BAL_MOTOR_sum <- BAL_SCC_sum[as.character(BAL_SCC_sum$SCC) %in% MOTOR_SCC_CODES,]
      
  # create a vector with the sums of the emmissions according to year
   TOTAL_BAL_MOTOR <- colSums(BAL_MOTOR_sum[,-1],na.rm=TRUE)
  
    
  # create barplot for total emissions according to year
   barplot(TOTAL_BAL_MOTOR,main="Total Emmissions from Motor Vehicle Sources in Baltimore, MD",xlab="Year",ylab="Total Emmissions (in tons)",col=heat.colors(8))
    
  # write plot to PNG file
  dev.copy(png,file="plot5.png",width=800,height=800)     # save plot to file
  dev.off()                                               # close PNG device
  
  
}  

