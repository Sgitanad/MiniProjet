import socket
import json
import threading
from gestionnaire_taches import Gestionnaire_Taches  

class ServeurTaches:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port

      
        self.gestionnaire = Gestionnaire_Taches()
        self.gestionnaire.charger()

    def demarrer(self):
        """Démarrer le serveur TCP."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        print(f"Serveur démarré sur {self.host}:{self.port}")

        while True:
            client_socket, addr = self.socket.accept()
            print(f"🔗 Client connecté depuis {addr}")

            thread = threading.Thread(target=self.gerer_client, args=(client_socket,))
            thread.start()

    def gerer_client(self, client_socket):
        """Gérer la communication avec un seul client."""
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"📨 Requête reçue : {data}")

                reponse = self.traiter_requete(data)
                client_socket.send(reponse.encode('utf-8'))

        except Exception as e:
            print(f"Erreur client : {e}")

        finally:
            client_socket.close()
            print("🔌 Connexion fermée")

    def traiter_requete(self, data):
        """Traite la requête JSON et renvoie une réponse JSON."""
        try:
            requete = json.loads(data)
            action = requete.get("action")

            if action == "ajouter":
                titre = requete.get("titre")
                description = requete.get("description")
                auteur = requete.get("auteur", "Anonyme")

                tache = self.gestionnaire.ajouter_tache(titre, description, auteur)
                self.gestionnaire.sauvegarder()

                return json.dumps({"success": True, "tache": tache.to_dict()})

            elif action == "lister":
                taches = [t.to_dict() for t in self.gestionnaire.lister_taches()]
                return json.dumps({"success": True, "taches": taches})

            elif action == "supprimer":
                id_val = requete.get("id")
                if isinstance(id_val, str):
                    id_val = int(id_val)

                success = self.gestionnaire.supprimer_tache(id_val)
                if success:
                    self.gestionnaire.sauvegarder()

                return json.dumps({"success": success})

            elif action == "changer_statut":
                id_val = requete.get("id")
                if isinstance(id_val, str):
                    id_val = int(id_val)

                nouveau_statut = requete.get("statut")

                success = self.gestionnaire.changer_statut(id_val, nouveau_statut)
                if success:
                    self.gestionnaire.sauvegarder()

                return json.dumps({"success": success})

            else:
                return json.dumps({"success": False, "erreur": "Action inconnue"})

        except json.JSONDecodeError:
            return json.dumps({"success": False, "erreur": "JSON invalide"})
        except Exception as e:
            return json.dumps({"success": False, "erreur": str(e)})


if __name__ == "__main__":
    serveur = ServeurTaches()
    serveur.demarrer()
