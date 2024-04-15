
###############  ANÁLISIS EXPLORATORIO

#Entorno de trabajo

library(readxl)
setwd("C:/Users/Maria.Granda/OneDrive - Cushman & Wakefield/Desktop/EAE/TFM")


#Lectura del fichero de radiacion

Radiacion <- read_excel("Radiacion.xlsx")
View(Radiacion)

library(tidyr)
colnames(Radiacion)

#Convertimos la varaible fecha en año y mes
Radiacion <- separate(Radiacion, Fecha, into = c("Anio", "Mes"), sep = "_")

#Hacemos un unpivot para tener en una sola variable, la provincia y su valor de radiacion
Radiacion<- pivot_longer(Radiacion, 
                      cols = c("Jaen", "Granada", "Almeria", "Malaga", "Cordoba", "Sevilla",
                               "Cadiz","Huelva", "Murcia", "Caceres","Badajoz","Toledo", "Ciudad Real",          
                               "Albacete","Cuenca", "Guadalajara","Castellon","Valencia","Alicante" ,             
                               "Baleares", "Ceuta", "Melilla", "Santa Cruz de Tenerife", "Las Palmas","Madrid",                
                               "Soria","Segovia", "Avila","Salamanca","Zamora", "Leon",              
                               "Palencia","Burgos","Valladolid","Huesca","Zaragoza","Teruel",                
                              "Gerona","Lerida", "Tarragona","Barcelona","Navarra", "La Rioja",            
                              "Vizcaya" ,"Guipuzcoa","Alava","Cantabria","Asturias", "La Coruña","Lugo","Orense","Pontevedra"),
                            names_to = "Provincia",
                            values_to = "valor_radiacion")


#Pasamos a numerico nuestra variable a analizar
Radiacion$valor_radiacion<-as.numeric(Radiacion$valor_radiacion)
summary(Radiacion$valor_radiacion)

#Comprobamos que no hay valores faltantes
sum(is.na(Radiacion$valor_radiacion))

# Evolucion de la radiacion en España
install.packages("ggplot2")
library(ggplot2)

plot(Radiacion$Anio, Radiacion$valor_radiacion, type = "l", col = "lightblue", lwd = 5,
     xlab="Año", ylab="Radiación (kWh/m2)")

#Vamos a ver cómo se comportan por meses
datos_2010<-subset(Radiacion, Radiacion$Anio==2010)
datos_2020<-subset(Radiacion, Radiacion$Anio==2020)

plot(datos_2010$Mes, datos_2010$valor_radiacion, type = "l", col = "lightblue", lwd = 5,
     xlab="Mes", ylab="Radiación (kWh/m2)")

plot(datos_2020$Mes, datos_2020$valor_radiacion, type = "l", col = "lightblue", lwd = 5,
     xlab="Mes", ylab="Radiación (kWh/m2)")


#Hacemos para cada año, el valor de radiacion
install.packages("dplyr")
library(dplyr)


# Media de la radiacion para cada año
radiacion_media_anio <- Radiacion %>%
  group_by(Anio)%>% 
             summarise(media_kWh = mean(valor_radiacion, na.rm = TRUE))

plot(radiacion_media_anio$Anio, radiacion_media_anio$media_kWh, type = "l", col = "lightblue", lwd = 5,
     xlab="Año", ylab="Radiación (kWh/m2)")

#Distribucion por Comunidades Autonomas

Radiacion$Comunidad<-ifelse (Radiacion$Provincia %in% c("Jaen", "Granada", "Almeria", "Malaga",
                                               "Cordoba", "Sevilla","Cadiz","Huelva"), "Andalucia",
                             ifelse(Radiacion$Provincia %in% c("Murcia"), "Murcia",
                                    ifelse(Radiacion$Provincia %in% c("Caceres","Badajoz"), "Extremadura",
                                           ifelse(Radiacion$Provincia %in% c("Toledo", "Ciudad Real","Albacete","Cuenca", "Guadalajara"), "Castilla La Mancha",
                                                  ifelse(Radiacion$Provincia %in% c("Castellon","Valencia","Alicante"), "Comunidad Valenciana",
                                                         ifelse(Radiacion$Provincia %in% c("Baleares"), "Islas Baleares",
                                                                ifelse(Radiacion$Provincia %in% c("Ceuta"), "Ceuta",
                                                                       ifelse(Radiacion$Provincia %in% c("Melilla"), "Melilla",
                                                                              ifelse(Radiacion$Provincia %in% c("Santa Cruz de Tenerife", "Las Palmas"), "Canarias",
                                                                                     ifelse(Radiacion$Provincia %in% c("Madrid"), "Comunidad de Madrid",
                                                                                            ifelse(Radiacion$Provincia %in% c("Soria","Segovia", "Avila","Salamanca","Zamora", "Leon",              
                                                                                                                              "Palencia","Burgos","Valladolid"), "Castilla Leon",
                                                                                                   ifelse(Radiacion$Provincia %in% c("Huesca","Zaragoza","Teruel"), "Aragon",
                                                                                                          ifelse(Radiacion$Provincia %in% c("Gerona","Lerida", "Tarragona","Barcelona"), "Cataluña",
                                                                                                                 ifelse(Radiacion$Provincia %in% c("La Rioja"), "La Rioja",
                                                                                                                        ifelse(Radiacion$Provincia %in% c("Navarra"), "Comunidad Foral de Navarra",
                                                                                                                               ifelse(Radiacion$Provincia %in% c("Vizcaya" ,"Guipuzcoa","Alava"), "Pais Vasco",
                                                                                                                                      ifelse(Radiacion$Provincia %in% c("Cantabria"), "Cantabria",
                                                                                                                                             ifelse(Radiacion$Provincia %in% c("Asturias"), "Principado de Asturias",
                                                                                                                                                    ifelse(Radiacion$Provincia %in% c("La Coruña","Lugo","Orense","Pontevedra"), "Galicia",NA)))))))))))))))))))

                                                                                                                                                    
                                                                                                   
                                                                              
#Comprobamos que no haya nulos   

sum(is.na(Radiacion$Comunidad))  

#Vemos para comunidad, cual sería la radiacion media

radiacion_media_ccaa<- Radiacion %>%
  group_by(Comunidad) %>%
  summarise(media_ccaa= mean (valor_radiacion))

media_total<-mean(radiacion_media_ccaa$media_ccaa)


ggplot(radiacion_media_ccaa, aes(x = Comunidad, y = media_ccaa)) +
  geom_bar(stat = "identity", fill = "skyblue") + #Para las barras
  geom_text(aes(label = round(media_ccaa, 0)), vjust = -0.5, color='black')+ #Etiquetas de la variacion media
  labs( x = "Comunidad Autónoma", y = "Media de Radiación (kWh/m2)")+ #Nombre de los ejes
  geom_hline(yintercept = media_total, color = "red", linetype = "dashed", size = 1) + #Linea media de radiacion del total de las comunidades
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) #Para que se vean bien las etiquetas de comunidad

#Exportacion del fichero a un formato xlsx                                                                                                  
install.packages("openxlsx")
library(openxlsx)
write.xlsx(Radiacion, file = "C:/Users/Maria.Granda/OneDrive - Cushman & Wakefield/Desktop/EAE/TFM/Datos_radiacion_depurados.xlsx")



#Lectura del fichero de precio medio
precio <- read_excel("Precio euro_m2.xlsx")
View(precio)


#Valores de las provincias
unique(precio$Lugar)

#Hacemos un unpivot para tener en una sola variable, la provincia y su valor precio
library(tidyr)
precio<- pivot_longer(precio, 
                         cols = c("2004","2005",	"2006",	"2007",	"2008",	"2009",
                         "2010",	"2011",	"2012",	"2013",	"2014",	"2015",	"2016",
                         "2017",	"2018",	"2019",	"2020",	"2021",	"2022",	"2023"),
                         names_to = "Anio",
                         values_to = "precio_medio")

comunidades<- c("Andalucía", "Aragón", "Asturias (Principado de )",
                "Balears (Illes)", "Canarias", "Cantabria", "Castilla y León",
                "Castilla-La Mancha", "Cataluña", "Comunitat Valenciana", 
                "Extremadura", "Galicia", "Madrid (Comunidad de)", "Murcia (Región de)",
                "Navarra (Comunidad Foral de)", "País Vasco", "Rioja (La)")

#Creamos 2 dataframes más, uno con el total nacional y otro por comunidades autonomas

#Data frame del total nacional
precio_nacional<-subset(precio, precio$Lugar=="TOTAL NACIONAL")

#Data frame por provincias
precio_provincias<-subset(precio, !(Lugar %in% comunidades))
precio_provincias<-subset(precio_provincias, Lugar!='TOTAL NACIONAL')

#Data frame por ccaa
precio_ccaa<-subset(precio, Lugar %in% comunidades)


#Evolucion precio medio del total nacional
install.packages("ggplot2")
library(ggplot2)

años<-c(2004:2023)
plot(precio_nacional$Anio, precio_nacional$precio_medio, type = "l", col = "lightblue", lwd = 3,
     xlab="Año", ylab="Precio medio €/m2", cex.axis = 0.8, axes=FALSE)

axis(1, at = años, labels = años)
axis(2)

# Dibuja los bordes del recuadro del gráfico
box()
