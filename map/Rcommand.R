
setwd('~/Desktop/SAR_metadata')
require (rworldmap)
require(rworldxtra)
dataGB <- read.table("map_gps_speciesv2.txt", sep="\t", stringsAsFactors = FALSE, quote = "", header = TRUE)
attach(dataGB)
mapPies( dataGB,nameX="LON", nameY="LAT", nameZs=c('Globigerina_bulloides','Globigerinella_siphonifera','Amphisorus_hemprichii','Phyllostaurus_cuspidatus','Globoquadrina_conglomerata','Virgulinella_fragilis','Sorites_orbiculus','Neidium_amphigomphus'),mapRegion='world', oceanCol = "white",landCol = "gray80")


