# Ergonomie du lecteur

Comment écrire des notes, des documents et des fichiers qui coûtent le moins possible au lecteur, d'après ce que
les sciences cognitives, la psycholinguistique et le génie logiciel ont mesuré. Pour les personnes qui écrivent,
et pour les modèles de langue qui écrivent.

[Read in English](README.md)

## Trois portes

| Vous êtes | Commencez par |
|---|---|
| quelqu'un qui écrit, ou un modèle sur le point d'écrire | [standard.md](standard.md) : une page, chaque principe avec son niveau de preuve, et comment vérifier son texte |
| un lecteur qui veut les raisons | [evidence/](evidence/) : une revue de littérature par thème, avec les arguments contre chaque principe |
| quelqu'un qui écrit pour un lecteur connu | [reader-styles/](reader-styles/) : ce qui change pour un novice, un expert, un lecteur visuel, un modèle de langue |

## Contenu

| Dossier | Rôle |
|---|---|
| [principles/](principles/) | l'optimum général, un fichier par principe, rangé par échelle : collection, document, phrase, page |
| [reader-styles/](reader-styles/) | les ajustements pour un lecteur connu, car le véritable optimum dépend de qui lit |
| [shapes/](shapes/) | des squelettes fixes par type de document : note, README de dossier, rapport, message de commit |
| [evidence/](evidence/) | les revues derrière les principes, et une [bibliographie](evidence/bibliography.md) commune |
| [checks/](checks/) | des programmes qui vérifient ce qu'un programme peut vérifier ; des questions pour le jugement sinon |

## Pourquoi des niveaux de preuve

Un principe ne vaut que ses preuves. Chacun indique s'il a été mesuré (**measured**), s'il est soutenu avec réserve
(**supported with caveat**), s'il est une convention que personne n'a testée (**convention**), ou s'il a été testé sans
résultat (**not supported**). Certaines règles connues tombent dans les deux derniers groupes, et le standard le dit.

## Vérifier un dépôt

```sh
git clone https://github.com/Tewf/reader-ergonomics
python3 reader-ergonomics/checks/run.py chemin/vers/votre/depot
```

Seule la bibliothèque standard de Python est nécessaire. Les constats exacts font échouer l'exécution ; les questions
qu'un programme ne peut pas trancher sont écrites dans `checks/out/needs-judgment.md`. Voir [checks/](checks/).

## Langue

Le contenu est en anglais ; seules les deux pages d'accueil sont bilingues.

## Licence et citation

Code sous [licence Apache 2.0](LICENSE) ; textes sous [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Réutilisez-les librement en
citant la source : [CITATION.cff](CITATION.cff).
