import socket
import json
from GestionnaireTaches import GestionnaireTaches

class ServeurTaches:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.gestion = GestionnaireTaches()

    def demarrer(self):
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.bind((self.host, self.port))
        serveur.listen(5)
        print(f"Serveur en écoute sur {self.host}:{self.port}")

        while True:
            client, addr = serveur.accept()
            print("Client connecté :", addr)

            data = client.recv(4096).decode()
            if not data:
                continue

            try:
                requete = json.loads(data)
                action = requete.get("action")

                if action == "add":
                    t = self.gestion.ajouter_tache(
                        requete["titre"],
                        requete["description"],
                        requete.get("auteur", "")
                    )
                    reponse = {"status": "ok", "tache": t.to_dict()}

                elif action == "list":
                    reponse = {"status": "ok", "taches": self.gestion.lister_taches()}

                elif action == "delete":
                    id = requete["id"]
                    ok = self.gestion.supprimer_tache(id)
                    reponse = {"status": "ok" if ok else "error"}

                elif action == "status":
                    id = requete["id"]
                    statut = requete["statut"]
                    ok = self.gestion.changer_statut(id, statut)
                    reponse = {"status": "ok" if ok else "error"}

                else:
                    reponse = {"status": "error", "message": "Action inconnue"}

            except Exception as e:
                reponse = {"status": "error", "message": str(e)}

            client.send(json.dumps(reponse).encode())
            client.close()
