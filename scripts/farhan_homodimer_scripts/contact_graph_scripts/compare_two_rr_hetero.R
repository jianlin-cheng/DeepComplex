#usage: Rscript compare_two_rr.R <interchain.rr> <predictedintrachain.dncon2.rr> <true_intrachain_from_pdb.rr> <output_image_file>
args=commandArgs(trailingOnly = TRUE)
infile=args[1] # true interchain RR file
#infile2 =args[2] # intrachain (DNCON2) RR file
pdbfile=args[2] #predicted interchain RR
outfile=args[3] #ouput image file
png(outfile, width=1600, height=1600, res=300)
#png(outfile, width=14, height=14, units="in",res=300)
#Final output:
#True_Interchain_color: Blue
#Predicted_Interchain_color: Red

#Interchain (multimer) file info
con <- file(infile, "rt")
tag=readLines(con,1)
seqlenA <- readLines(con, 1)
seqlenB <- readLines(con, 1)
L_A <- nchar(seqlenA)
L_B <- nchar(seqlenB)
data <- read.table(infile, skip = 3, header = FALSE)
col_count <- ncol(data)
sp<-strsplit(tag,split = "_")
A<-sp[[1]][1]
A<-substr(A,2,nchar(A))
B<-sp[[1]][2]
#par(mar=c(2,2,0.5,0.5))
# Plot for an RR file with multiple sources
native<-data
plot(native$V1, native$V2, col="blue", pch=0, xlab = paste0("Seq_B: ",B), ylab = paste0("Seq_A: ",A), ylim=c(L_B, 0), xlim=c(0, L_A))

#Predicted contacts file info
con3 <- file(pdbfile, "rt")
tag2 <- readLines(con3, 1)
seqlen3A <- readLines(con3, 1)
seqlen3B <- readLines(con3, 1)
L3_A <- nchar(seqlen3A)
L3_B <- nchar(seqlen3B)
data3 <- read.table(pdbfile, skip = 3, header = FALSE)
col_count3 <- ncol(data3)

######
##Change the threshold below to desired L/k value
######
pdb=data3[1:(L3_A+L3_B)/10,]
points(pdb$V1, pdb$V2, col="red", xlab = paste0("Seq_B: ",B), ylab = paste0("Seq_A: ",A), ylim=c(L3_B, 0), xlim=c(0, L3_A), pch = 1)
dev.off()

