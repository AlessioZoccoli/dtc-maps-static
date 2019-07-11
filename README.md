# DTC regione Lazio

Il Centro di Eccellenza del Distretto Tecnologico per le nuove tecnologie per i beni e le attività Culturali della regione Lazio
https://dtclazio.it/

## Mappatura big data + sentiment analysis - app dimostrativa e statica
Utilizzando alcuni tweet [tweet](https://github.com/RyanMullins/Tutorial-LeafletMongoDB/blob/master/src/primer_tweets.json) si vogliono creare delle mappe geografiche che mettano in relazione flussi di dati provenienti dai social network e informazioni geospaziali.
Nelle mappe è possibile associare il colore dell'icona (a goccia) al sentimento espresso dal tweet: da rosso scuro per molto negativo a verde scuro per molto positivo, grigio qualora il sentimento sia neutro, il tweet non è soggettivo o il testo non è analizzabile.
Questo mini progetto è eseguito in locale, non comunica con il web.

Tecnologie:
- **Folium**: creazione delle mappe
- **MongoDB** (driver PyMongo): base di dati per i tweet
- **translate**: traduzione verso l'inglese di tutte le lingue (in futuro verrà usato un modello apposito per l'italiano)
- **TextBlob**: per la sentiment analysis


