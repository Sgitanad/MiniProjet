from Tache import Tache

class GestionnaireTaches:
    def __init__(self):
        self.taches = {}
        self.prochain_id = 1

    def ajouter_tache(self, titre, description, auteur=""):
        t = Tache(self.prochain_id, titre, description, auteur)
        self.taches[self.prochain_id] = t
        self.prochain_id += 1
        return t

    def supprimer_tache(self, id):
        return self.taches.pop(id, None)

    def lister_taches(self):
        return [t.to_dict() for t in self.taches.values()]

    def changer_statut(self, id, nouveau_statut):
        if id in self.taches:
            self.taches[id].statut = nouveau_statut
            return True
        return False
