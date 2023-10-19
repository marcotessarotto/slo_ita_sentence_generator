# slo_ita_sentence_generator
servizio web che consente agli utenti autenticati di fornire una lista di parole slovene e ottenere esempi di frasi in slovene generate casualmente che contengano le parole fornite come input. 

Utilizza chatGPT per generare i testi. Strumento di studio della lingua slovena.

Esempio:

Input: 
```
["kruh", "mleko", "sir"]
```

Output:
```
{
    "data": {
        "language": "slo_to_ita",
        "result": {
            "6": {
                "id": 6,
                "italian_text": "Ho comprato del pane fresco, del latte e del formaggio.",
                "slovenian_text": "Kupil sem kruh, ki je bil sve\u017e, ter mleko in sir.",
                "words_list": [
                    "kruh",
                    "mleko",
                    "sir"
                ]
            }
        }
    },
    "success": true
}
```


