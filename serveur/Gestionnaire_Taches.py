import json
from Tache import Tache

class Gestionnaire_Taches:
    def __init__(self):
        self.taches = {}
        self.compteur = 1

    def ajouter_tache(self, titre, description, auteur):
        tache = Tache(self.compteur, titre, description, auteur)
        self.taches[self.compteur] = tache
        self.compteur += 1
        return tache

    def lister_taches(self):
        return list(self.taches.values())

    def supprimer_tache(self, id_tache):
        if id_tache in self.taches:
            del self.taches[id_tache]
            return True
        return False

    def changer_statut(self, id_tache, statut):
        if id_tache in self.taches:
            self.taches[id_tache].changer_statut(statut)
            return True
        return False

    def sauvegarder(self, fichier="taches.json"):
        data = {str(id_tache): self.taches[id_tache].to_dict() for id_tache in self.taches}
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def charger(self, fichier="taches.json"):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)

            for id_str, infos in data.items():
                id_num = int(id_str)
                tache = Tache(
                    infos["id"],
                    infos["titre"],
                    infos["description"],
                    infos["auteur"]
                )
                tache.statut = infos["statut"]
                self.taches[id_num] = tache

                if id_num >= self.compteur:
                    self.compteur = id_num + 1

        except FileNotFoundError:
            pass
