class Tache:
    def __init__(self, id, titre, description, auteur, statut="TODO"):
        # les infos de la tache
        self.id = id
        self.titre = titre
        self.description = description
        self.auteur = auteur
        self.statut = statut  # TODO / DOING / DONE
    
    def changer_statut(self, nouveau_statut):
        """Changer le statut de la tâche."""
        self.statut = nouveau_statut

    def to_dict(self):
        
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "auteur": self.auteur,
            "statut": self.statut
        }
