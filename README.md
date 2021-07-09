# Script utilizzati nel lavoro di ricerca "Predizione di attività future in base a dati di contesto"

<h2>create_feature_vector</h2>

<p>
Script utilizzato per la creazione dei feature vector dei dateset "HH\*" forniti dal CASAS.<br />
Lo script va utilizzato all'interno della cartella che contiene i file "formattedhh\*.txt" che son stati creati durante la creazione del database (https://github.com/Piier/activity_forecasting_db).<br />
Lo script utilizza sia i dataset formattati (per creare le tabelle di stato) che il database che contiene le informazioni dei dataset. Per selezionare i dataset da cui creare i feature vector è neccessario modificare la lista "case" in riga 10. <br />
  In output vengono forniti i feature vector creati.<br />

<h2>reduce_activity</h2>

Script utilizzato per la selezione della attività.<br />
Lo script va utilizzato all'interno della cartella che contiene il file "formattedhh\*.txt" e il file "feature_vectorHH\*.csv".<br />
Lo script utilizza il dataset formattato, il database che contiene le informazioni dei dataset e il feature vector da cui si vogliono ridurre le attività. Per selezionare il dataset da cui ridurre le attività è neccessario modificare la variabile "case".<br />
All'interno del file "removed_activity.txt" viene fornita la lista della attività che sono state eliminate da ogni dataset nel lavoro di ricerca. La lista è anche già presente nello script.<br />
In output viene fornito il dataset con le attività ridotte di numero.<br />


<h2>chi_squared</h2>

Script utilizzato per la selezione della feature.<br />
Lo script va utilizzato all'interno della cartella che contiene i file "feature_vectorHH\*.csv".<br />
Lo script utilizza i feature vector su cui si vuole eseguire la feature selection. Per selezionare il dataset da cui ridurre le attività è neccessario modificare la variabile "case".<br />
In output viene fornito il dataset con le feature selezionate tramite il metodo Chi Squared.<br />

<h2>forecasting</h2>

Script utilizzato per la predizione della attività future. Lo script si basa sul software Weka<br />
Lo script va utilizzato all'interno della cartella che contiene i file "feature_vectorHH\*.csv".<br />
Lo script, utilizzando i 27 feature vector creati, esegue la predizione delle attività.<br />
In output viene fornito un riepilogo con le prestazioni ottenute da ogni dataset con ogni algoritmo utilizzato. Inoltre, viene fornito un riepilogo del numero di attività da predire che compaiono come attività predetta o nelle prime 5 posizioni rispetto all'output del modello. Il file mostra l'andamento delle prestazioni per ogni datest utilizzato, quindi bisogna tenere in considerazione solo le ultime righe dell'output di ogni algoritmo (visto che sono basate su tutti i dataset e non solo su una parte di essi)<br />
 
