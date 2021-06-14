
setwd('~/Documents/GitHub/SAR_dark_area-codes/map')
require (rworldmap)
require(rworldxtra)
dataGB <- read.table("map_gps_speciesv2.txt", sep="\t", stringsAsFactors = FALSE, quote = "", header = TRUE)
attach(dataGB)
mapPies( dataGB,nameX="LON", nameY="LAT", nameZs=c('Globigerinella_siphonifera','Globigerinoides_sacculifer','Globigerinoides_ruber','Globigerina_bulloides','Turborotalita_quinqueloba','Globigerinella_calida','Orbulina_universa','Pulleniatina_obliquiloculata','Neogloboquadrina_pachyderma','Globorotalia_inflata','Neogloboquadrina_incompta','Globigerinita_uvula','Globorotalia_truncatulinoides','Globorotalia_scitula','Globorotalia_hirsuta'),mapRegion='world', oceanCol = "white",landCol = "gray80")


