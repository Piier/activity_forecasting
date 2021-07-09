import os
import pickle
import tempfile
import traceback
import javabridge
from numpy.core.numeric import correlate

import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.core.dataset import Instances
from weka.classifiers import Classifier
from weka.core.classes import serialization_read, serialization_write, serialization_read_all, serialization_write_all

from weka.classifiers import Evaluation
from weka.core.classes import Random
from weka.classifiers import FilteredClassifier
from weka.filters import Filter


def main():
    """
    Just runs some example code.
    """

    f=open("stats.txt","w+")
    
    name_feature_vector = "feature_vector"

    case=['HH101','HH102','HH103','HH104','HH105','HH106','HH108','HH109','HH110','HH111','HH112','HH113','HH114','HH116','HH117','HH118','HH119','HH120','HH122','HH123','HH124','HH125','HH126','HH127','HH128','HH129','HH130']

    alg = ["weka.classifiers.meta.Bagging", "weka.classifiers.meta.RandomSubSpace", "weka.classifiers.trees.J48","weka.classifiers.meta.LogitBoost"]

    for i in alg:
        f.write("-----------\n")
        f.write(i)
        f.write("\n")
        print("---------------")
        print(i)
        cont_giuste_2_tot=0
        cont_giuste_3_tot=0
        cont_giuste_4_tot=0
        cont_giuste_5_tot=0        

        for casa in case:
    
            feature_vector = name_feature_vector+casa+".arff"

            loader = Loader("weka.core.converters.ArffLoader")
            data = loader.load_file(feature_vector)
            data.class_is_last()
       
            remove = Filter(classname="weka.filters.unsupervised.attribute.Remove")
            i=i.strip()
            cls = Classifier(classname=i)
       
            fc = FilteredClassifier()
            fc.filter = remove
            fc.classifier = cls
          
            evl = Evaluation(data)
            evl.crossvalidate_model(fc, data, 10, Random(1))
            
            print(evl.summary())
            res = evl.predictions

            
            cont=0
            cont_giuste_2=0
            cont_giuste_3=0
            cont_giuste_4=0
            cont_giuste_5=0

            for linea in res:

                listato = list(linea.distribution)
                listato_ord = list(linea.distribution)
                listato_ord.sort()
               
                primo = listato.index(listato_ord[-1])
                secondo = listato.index(listato_ord[-2])                
                terzo = listato.index(listato_ord[-3])   
                quarto = listato.index(listato_ord[-4])
                quinto = listato.index(listato_ord[-5])
                corretto = int(linea.actual)

                if corretto==primo or corretto==secondo:
                    cont_giuste_2+=1
                    cont_giuste_3+=1
                    cont_giuste_4+=1
                    cont_giuste_5+=1
                elif corretto==terzo:
                    cont_giuste_3+=1
                    cont_giuste_4+=1
                    cont_giuste_5+=1
                elif corretto==quarto:
                    cont_giuste_4+=1
                    cont_giuste_5+=1
                elif corretto==quinto:
                    cont_giuste_5+=1
                
                cont+=1
            
            cont_giuste_2_tot+=cont_giuste_2
            cont_giuste_3_tot+=cont_giuste_3
            cont_giuste_4_tot+=cont_giuste_4
            cont_giuste_5_tot+=cont_giuste_5
            perc_2=(cont_giuste_2_tot/44252)*100
            perc_3=(cont_giuste_3_tot/44252)*100
            perc_4=(cont_giuste_4_tot/44252)*100
            perc_5=(cont_giuste_5_tot/44252)*100
            
            f.write(f"casa {casa} top 2 = {cont_giuste_2}. Totale = {cont_giuste_2_tot}. {perc_2}\n")
            f.write(f"casa {casa} top 3 = {cont_giuste_3}. Totale = {cont_giuste_3_tot}. {perc_3}\n")
            f.write(f"casa {casa} top 4 = {cont_giuste_4}. Totale = {cont_giuste_4_tot}. {perc_4}\n")
            f.write(f"casa {casa} top 5 = {cont_giuste_5}. Totale = {cont_giuste_5_tot}. {perc_5}\n")
            print(f"casa {casa} top 2 = {cont_giuste_2}. Totale = {cont_giuste_2_tot}. {perc_2}")
            print(f"casa {casa} top 3 = {cont_giuste_3}. Totale = {cont_giuste_3_tot}. {perc_3}")
            print(f"casa {casa} top 4 = {cont_giuste_4}. Totale = {cont_giuste_4_tot}. {perc_4}")
            print(f"casa {casa} top 5 = {cont_giuste_5}. Totale = {cont_giuste_5_tot}. {perc_5}")

        
    #f.close()
            
if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
    finally:
        jvm.stop()
