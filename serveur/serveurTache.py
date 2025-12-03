import socket
import json
import threading
from Gestionnaire_Taches import Gestionnaire_Taches

class ServeurTaches:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.gestionnaire = Gestionnaire_Taches()
        self.gestionnaire.charger()
        self.running = True

    def demarrer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        print(f"Serveur démarré sur {self.host}:{self.port}")

        try:
            while self.running:
                client_socket, addr = self.socket.accept()
                print(f"Client connecté depuis {addr}")

                thread = threading.Thread(
                    target=self.gerer_client,
                    args=(client_socket,),
                    daemon=True
                )
                thread.start()

        except KeyboardInterrupt:
            print("\nArrêt du serveur demandé")

        finally:
            self.socket.close()
            print("Serveur arrêté")

    def gerer_client(self, client_socket):
        buffer = ""

        try:
            while True:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break

                buffer += data

                # Process only when \n is detected
                if "\n" in buffer:
                    ligne, buffer = buffer.split("\n", 1)

                    if ligne.strip() == "":
                        continue

                    try:
                        requete = json.loads(ligne)
                    except json.JSONDecodeError:
                        print("JSON invalide reçu :", ligne)
                        continue

                    # traiter la requête
                    reponse = self.traiter_requete(requete)

                    # envoyer réponse + \n
                    client_socket.sendall(
                        (json.dumps(reponse) + "\n").encode("utf-8")
                    )

        except Exception as e:
            print(f"Erreur client : {e}")

        finally:
            client_socket.close()
            print("Connexion fermée")

    def traiter_requete(self, requete):
        try:
            action = requete.get("action")

            if action == "ajouter":
                titre = requete.get("titre")
                description = requete.get("description")
                auteur = requete.get("auteur", "Anonyme")

                if not titre or not description:
                    return {"success": False, "erreur": "Titre ou description manquant"}

                tache = self.gestionnaire.ajouter_tache(titre, description, auteur)
                self.gestionnaire.sauvegarder()

                return {"success": True, "tache": tache.to_dict()}

            elif action == "lister":
                taches = [t.to_dict() for t in self.gestionnaire.lister_taches()]
                return {"success": True, "taches": taches}

            elif action == "supprimer":
                id_val = int(requete.get("id"))
                success = self.gestionnaire.supprimer_tache(id_val)

                if success:
                    self.gestionnaire.sauvegarder()

                return {"success": success}

            elif action == "changer_statut":
                id_val = int(requete.get("id"))
                nouveau_statut = requete.get("statut")

                if not nouveau_statut:
                    return {"success": False, "erreur": "Statut manquant"}

                success = self.gestionnaire.changer_statut(id_val, nouveau_statut)

                if success:
                    self.gestionnaire.sauvegarder()

                return {"success": success}

            else:
                return {"success": False, "erreur": "Action inconnue"}

        except Exception as e:
            return {"success": False, "erreur": str(e)}

if __name__ == "__main__":
    serveur = ServeurTaches()
    serveur.demarrer()