# API Choice

- Étudiant : Othman Dounit
- API choisie : ipify
- URL base : https://api.ipify.org
- Documentation officielle / README : https://www.ipify.org/
- Auth : None
- Endpoints testés :
  - GET /?format=json
  - GET /?format=text
- Hypothèses de contrat (champs attendus, types, codes) :
  - Pour ?format=json : HTTP 200, Content-Type JSON, réponse = objet JSON avec champ "ip" (string) contenant une IPv4/IPv6 valide.
  - Pour ?format=text : HTTP 200, réponse = texte contenant une IP.
- Limites / rate limiting connu :
  - Non documenté précisément ; on limite à quelques requêtes par run (ex: 10 max).
- Risques (instabilité, downtime, CORS, etc.) :
  - API publique → possible downtime ou limitation temporaire ; on ajoute timeout (3s) + 1 retry.
