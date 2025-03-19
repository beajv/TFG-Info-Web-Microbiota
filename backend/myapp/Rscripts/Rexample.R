#!/usr/bin/env Rscript
library("optparse")
 
option_list = list(make_option(c("-f", "--file"), type="character", default=NULL, 
		     help="dataset file name", metavar="character"),

	           make_option(c("-p", "--params"), type="character", 
		     help="output file name [default= %default]", metavar="character"), 

	           make_option(c("-o", "--out"), type="character", default="out.txt", 
		     help="output file name [default= %default]", metavar="character")); 
 
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);


print(opt$params)
if (is.null(opt$file)){
	  print_help(opt_parser)
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
}

data <- read.table(file = opt$file, header = TRUE, sep=',')
head(data)
png(file=opt$out, width=600, height=350)
hist(data$sepal.width, col="gold")
dev.off()


