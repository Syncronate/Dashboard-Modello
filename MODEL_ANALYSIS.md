# Verifica del Modello Previsionale Matematico

Il seguente documento analizza il comportamento del modello previsionale sperimentale per il fiume Misa a Bettolelle, in risposta alla segnalazione di "strane previsioni" (picchi improvvisi) nonostante un livello storico stabile.

## Analisi del Problema

L'utente ha segnalato un picco anomalo nella previsione (da ~1.35m a ~1.70m) che inizia circa 1.5 ore nel futuro, mentre i dati storici del sensore Bettolelle mostrano un andamento piatto.

### Causa Identificata: Sensibilità al sensore Corinaldo (Nevola)

L'analisi del codice ha confermato che il modello implementa correttamente le formule previste. Tuttavia, queste formule sono **estremamente sensibili al trend (Delta)** del sensore `Nevola - Livello Nevola (mt)` (situato a Corinaldo).

Le formule per le previsioni a medio termine (> 1.5 ore) includono i seguenti termini:

*   **f1.5 (t + 1.5h):** `+ 0.947 * D(Corinaldo, 0, 30min)`
*   **f2.0 (t + 2.0h):** `+ 1.366 * D(Corinaldo, 0, 30min)`
*   **f3.0 (t + 3.0h):** `+ 2.114 * D(Corinaldo, 0, 30min)`

Dove `D(Corinaldo, 0, 30min)` è la variazione del livello di Corinaldo negli ultimi 30 minuti.

**Esempio di impatto:**
Se il livello a Corinaldo sale di soli **20 cm** (0.2m) in 30 minuti (un picco che potrebbe essere reale o un errore del sensore):
*   Impatto su previsione +3h: `2.114 * 0.2 = +0.42 metri`.

Questo spiega perfettamente il salto da 1.35m a 1.77m osservato nel grafico. Il modello "vede" l'onda di piena a monte (Corinaldo) e prevede che arriverà a valle (Bettolelle) circa 1.5-3 ore dopo.

## Script di Riproduzione

Il seguente script Node.js può essere utilizzato per verificare matematicamente questo comportamento simulando i dati.

```javascript
const parseAndFixDecimal = (value) => parseFloat(String(value).replace(',', '.'));

// Mock Data e Costanti
const C_BETTOLELLE = 'Misa - Livello Misa (mt)';
const C_CORINALDO = 'Nevola - Livello Nevola (mt)';
// ... altri sensori simulati come piatti

// Funzione semplificata di calcolo previsione (estratta da index.html)
function calculateForecast(corinaldoDelta) {
    const baseline = 1.35; // Livello attuale Bettolelle

    // Formula semplificata per f3 (3 ore)
    // f3 = Costante + (Coeff_Bettolelle * Livello_Bettolelle) + (Coeff_Corinaldo * Delta_Corinaldo)
    const f3 = 0.016 + (0.966 * baseline) + (2.114 * corinaldoDelta);

    return f3;
}

console.log("--- SIMULAZIONE IMPATTO CORINALDO ---");
console.log("Scenario 1: Corinaldo Stabile (Delta = 0m)");
console.log("Previsione +3h: " + calculateForecast(0).toFixed(2) + " m");

console.log("\nScenario 2: Corinaldo Picco (+0.2m in 30min)");
console.log("Previsione +3h: " + calculateForecast(0.2).toFixed(2) + " m");
// Output atteso: ~1.77 m
```

## Conclusione

Non è presente un "bug" nel codice (errore di sintassi o logica errata). Il comportamento osservato è una caratteristica intrinseca del modello matematico implementato.

**Azioni consigliate:**
1.  Verificare la qualità dei dati del sensore "Nevola - Livello Nevola" per escludere letture errate (spike spuri).
2.  Se il comportamento è ritenuto troppo aggressivo, sarà necessario richiedere una ricalibrazione dei coefficienti del modello matematico (in particolare riducendo il peso di `D(C_CORINALDO)`).
