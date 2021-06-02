#usage: Rscript compare_two_rr.R <interchain.rr> <predictedintrachain.dncon2.rr> <true_intrachain_from_pdb.rr> <output_image_file>
args=commandArgs(trailingOnly = TRUE)
#infile=args[1] # true interchain RR file
#infile2 =args[2] # intrachain (DNCON2) RR file
pdbfile=args[1] #predicted interchain RR
outfile=args[2] #ouput image file
png(outfile, width=1600, height=1600, res=300)

#Final output:
#True_Interchain_color: Blue
#Predicted_Interchain_color: Green

#Interchain (multimer) file info
#con <- file(infile, "rt")
#seqlen <- readLines(con, 1)
#L <- nchar(seqlen)
#data <- read.table(infile, skip = 1, header = FALSE)
#col_count <- ncol(data)
#data$V7 <- abs(data$V1-data$V2)
#par(mar=c(2,2,0.5,0.5))
# Plot for an RR file with multiple sources
#native <- subset(data, data$V4 == "8")
#native<-data
#plot(native$V1, native$V2, col="blue", pch=0, xlab = NULL, ylab = NULL, ylim=c(L, 0), xlim=c(0, L))
#points(native$V2, native$V1, col="red", pch=0, xlab = NULL, ylab = NULL, ylim=c(L, 0), xlim=c(0, L))

#Intrachain (monomer) file info
#con2 <- file(infile2, "rt")
#seqlen2 <- readLines(con2, 1)
#L2 <- nchar(seqlen2)
#data2 <- read.table(infile2, skip = 1, header = FALSE)
#col_count2 <- ncol(data2)
##data2$V7 <- abs(data2$V1-data2$V2)
#predic <- subset(data2, data2$V4 == "8")
#points(predic$V2, predic$V1, col="green", xlab = NULL, ylab = NULL, ylim=c(2*L, 0), xlim=c(0, L*2), pch = 1)
##points(predic$V1, predic$V2, col="red", xlab = NULL, ylab = NULL, ylim=c(L, 0), xlim=c(0, L), pch = 2)

#PDB file info
con3 <- file(pdbfile, "rt")
seqlen3 <- readLines(con3, 1)
L3 <- nchar(seqlen3)
L<-L3
data3 <- read.table(pdbfile, skip = 1, header = FALSE)
col_count3 <- ncol(data3)
#data3$V7 <- abs(data3$V1-data3$V2)
#pdb <- subset(data3, data3$V4 == "6")
######
##Change the threshold below to desired L/k value
######
pdb=data3[1:L/10,]
plot(pdb$V1, pdb$V2, col="blue", xlab = "", ylab = "", ylim=c(L, 0), xlim=c(0, L), pch = 1)
title("Homodimer Top-L/10 Contacts")
#legend("topright", bty="n", legend=c("Interchain","DNCON2","Intrachain_PDB"), pch = c(0,2,1),text.font=2,cex=1, col=c("red","green","blue"))
#text(0, L, "Top-2L", cex=2.0, adj = c(0,1), pos=4)
dev.off()
