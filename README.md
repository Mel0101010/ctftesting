# CTF Testing with Dagger

Automatise le build, l'exécution et la validation des challenges CTF via [Dagger](https://dagger.io).  
Chaque challenge est buildé dans un container isolé, la solve est executée contre ce service, et le flag récupéré est comparé au flag attendu.

## Structure attendue

```
<ctf_path>/
  <categorie>/
    <challenge>/
      Dockerfile          # build du service challenge
      <sources>           # code source du challenge
      solve.py            # script de solve — doit afficher le flag sur stdout
      flag.txt            # flag attendu (une ligne)
      requirements.txt    # (optionnel) dépendances pip pour solve.py
```

Exemple :

```
challenges/
  web/
    chall1/
      app.py  Dockerfile  solve.py  flag.txt  requirements.txt
  crypto/
    chall1/
      chall.py  Dockerfile  solve.py  flag.txt
  pwn/
    chall1/
      chall.py  Dockerfile  solve.py  flag.txt
```

> Le port est lu automatiquement depuis la directive `EXPOSE` du `Dockerfile`.  
> L'hôte du service est `challenge` depuis le container solve.

## Prérequis

- Docker
- Python 3.11+
- Dagger SDK Python

```bash
cd dagger
python -m venv .venv && source .venv/bin/activate
pip install dagger-io
```

## Utilisation

```bash
# Dossier par défaut (./challenges)
python dagger/main.py

# Chemin personnalisé
python dagger/main.py /chemin/vers/ctf
```

## Résultat

```
=== CTF Challenge Testing ===
  Path  : /home/.../challenges
  Found : 3 challenge(s)

  ✅  [WEB   ] chall1  →  fakeflag
  ✅  [CRYPTO] chall1  →  fakeflag{xor_is_not_crypto}
  ❌  [PWN   ] chall1
       expected : fakeflag{overflow_go_brrr}
       got      : Nope

  2/3 challenge(s) passed.
```

## Ajouter un challenge

Créer un dossier avec les 4 fichiers requis (`Dockerfile`, `solve.py`, `flag.txt`, sources) — aucune modification du script principal nécessaire.
