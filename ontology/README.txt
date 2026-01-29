* Dans M2_Metaconcepts.jsonld
- les "namespaces" requis (dans "@context") sont les suivants (valider avec Claude):
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld#",
    "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#",
    "m3:eagle_eye": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld#",
    "m3:sphinx_eye": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld#"
	
- encore des erreurs d'encodage (dans les formules tensorielles): "¢ ¢"

- Il manque "Imbrication" dans M2_Metaconcepts.jsonld

- Check présence de: Behavior, Tropism, Step, Action => OK

- l'"owl:imports" nécessaire et suffidsant est: 
  "owl:imports": [
        "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld"
  ]
  
  
* Mettre a jour les "extensions M1" (dans ontology/M1_extensions)
- utiliser la propriété "m3:ontologyCategory" avec la valeur "m3:DomainExtension" 

* Dans TSCG_Research_Paper_Draft_v1.md


* Dans les "Inputs":
- Rédiger un "TSCG_Modelling_Genesis.md"