library("readxl")
library("optparse")
library("stringr")
library("dplyr")
library("factoextra")

option_list = list(make_option(c("-f", "--file"), type="character", default="ENDORE_relab_0.01%.xlsx", 
                               help="dataset file name", metavar="character"),
                   make_option(c("-o", "--out"), type="character", default="out.png", 
                               help="output file name [default= %default]", metavar="character")); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

if (is.null(opt$file)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
}

data_cervix <- read_excel(opt$file)
data_cervixR <- data_cervix[,9:ncol(data_cervix)]

colnames(data_cervixR) <- lapply(colnames(data_cervixR), function(i) {paste("C", sub(".*D_5_","",i), sep = "")})
colnames(data_cervixR) <- lapply(colnames(data_cervixR), function(i) {
  if(str_detect(i, "D_4")){paste("CD_4", sub(".*D_4","",i), sep = "")}
  else{
    i
  }})
colnames(data_cervixR) <- lapply(colnames(data_cervixR), function(i) {
  if(str_detect(i, "D_3")){paste("CD_3", sub(".*D_3","",i), sep = "")}
  else{
    i
  }})
colnames(data_cervixR) <- lapply(colnames(data_cervixR), function(i) {
  if(str_detect(i, "D_2")){paste("CD_2", sub(".*D_2","",i), sep = "")}
  else{
    i
  }})
colnames(data_cervixR) <- lapply(colnames(data_cervixR), function(i) {
  if(str_detect(i, "D_1")){paste("CD_1", sub(".*D_1","",i), sep = "")}
  else{
    i
  }})
data_cervix <- cbind(data_cervix[,c(1,2,3,4,5,6,7,8)],data_cervixR)

data_cervix <- subset(data_cervix, select = -`CD_0__Bacteria;__;__;__;__;__`)
data_cervixBI <- data_cervix %>% dplyr::select(starts_with(c("C_","CD_")), group) %>% 
  filter(group == 'MALE_FACTOR' | group == 'TUBAL_FACTOR'| group == 'ENDOMETRIOSIS' | group == 'RIF' | group == 'RM') %>%  
  mutate(Group = case_when(group == 'MALE_FACTOR' | group == 'TUBAL_FACTOR' ~ 'favorable', TRUE ~ 'no favorable')) %>%  
  dplyr::select(-contains("uncultured"))

X_cervixBI <- data_cervixBI[,1:(ncol(data_cervixBI)-2)]
constant_columns <- sapply(X_cervixBI, function(col) var(col) == 0)
# colcolnames(X_cervixBI[,constant_columns])
X_cervixBI <- X_cervixBI[, !constant_columns]

PCAcervix <- prcomp(X_cervixBI, scale = TRUE)

png(file=opt$out, width=600, height=350)
fviz_pca_ind(PCAcervix,
             geom.ind = "point", # show points only (nbut not "text")
             col.ind = data_cervixBI$group, # color by groups
             palette = c("#CC0099", "#00CCCC", "#CC0099", "#CC0099", "#00CCCC", "#868686FF"),
             addEllipses = TRUE, ellipse.type= "confidence",
             legend.title = "Groups")
dev.off()