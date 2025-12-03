import socket
import json


class ClientTaches:
    def __init__(self, hote="server", port=5000):
        self.hote = hote
        self.port = port

    def envoyer_requete(self, requete):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.hote, self.port))

            sock.sendall((json.dumps(requete) + "\n").encode("utf-8"))

            tampon = ""
            while True:
                donnees = sock.recv(1024).decode("utf-8")
                if not donnees:
                    break
                tampon += donnees
                if "\n" in tampon:
                    break

            sock.close()

            try:
                return json.loads(tampon.strip())
            except:
                return {"success": False, "erreur": "Réponse invalide du serveur"}

        except Exception as e:
            return {"success": False, "erreur": f"Erreur de connexion : {e}"}

    def ajouter_tache(self):
        print("\nAjouter une nouvelle tâche")
        titre = input("Titre : ")
        description = input("Description : ")
        auteur = input("Auteur (optionnel) : ") or "Anonyme"

        requete = {
            "action": "ajouter",
            "titre": titre,
            "description": description,
            "auteur": auteur
        }

        reponse = self.envoyer_requete(requete)
        if reponse.get("success"):
            print("Tâche ajoutée avec succès")
        else:
            print("Échec de l'ajout :", reponse.get("erreur"))

    def lister_taches(self):
        print("\nListe des tâches")
        requete = {"action": "lister"}
        reponse = self.envoyer_requete(requete)

        if reponse.get("success"):
            taches = reponse.get("taches", [])
            if not taches:
                print("Aucune tâche")
                return

            for t in taches:
                print("-" * 30)
                print(f"ID : {t['id']}")
                print(f"Titre : {t['titre']}")
                print(f"Description : {t['description']}")
                print(f"Statut : {t['statut']}")
                print(f"Auteur : {t['auteur']}")
        else:
            print("Impossible de récupérer les tâches :", reponse.get("erreur"))

    def supprimer_tache(self):
        print("\nSupprimer une tâche")
        self.lister_taches()

        try:
            id_tache = int(input("\nEntrez l'ID de la tâche à supprimer : "))
            requete = {"action": "supprimer", "id": id_tache}
            reponse = self.envoyer_requete(requete)

            if reponse.get("success"):
                print("Tâche supprimée avec succès")
            else:
                print("Échec de la suppression :", reponse.get("erreur"))
        except ValueError:
            print("ID invalide")

    def changer_statut(self):
        print("\nChanger le statut d'une tâche")
        self.lister_taches()

        try:
            id_tache = int(input("\nEntrez l'ID de la tâche : "))
            nouveau_statut = input("Nouveau statut (TODO, DOING, DONE) : ").upper()

            if nouveau_statut not in ["TODO", "DOING", "DONE"]:
                print("Statut invalide")
                return

            requete = {
                "action": "changer_statut",
                "id": id_tache,
                "statut": nouveau_statut
            }

            reponse = self.envoyer_requete(requete)

            if reponse.get("success"):
                print("Statut modifié avec succès")
            else:
                print("Échec du changement de statut :", reponse.get("erreur"))
        except ValueError:
            print("ID invalide")

    def menu_principal(self):
        while True:
            print("\n" + "=" * 40)
            print("Gestionnaire de tâches")
            print("=" * 40)
            print("1. Ajouter une tâche")
            print("2. Lister les tâches")
            print("3. Supprimer une tâche")
            print("4. Changer le statut d'une tâche")
            print("5. Quitter")
            print("=" * 40)

            choix = input("Votre choix : ")

            if choix == "1":
                self.ajouter_tache()
            elif choix == "2":
                self.lister_taches()
            elif choix == "3":
                self.supprimer_tache()
            elif choix == "4":
                self.changer_statut()
            elif choix == "5":
                print("Au revoir")
                break
            else:
                print("Choix invalide")


if __name__ == "__main__":
    client = ClientTaches()
    client.menu_principal()