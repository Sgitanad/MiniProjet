class Tache:
    def __init__(self, id, titre, description, auteur="", statut="TODO"):
        self.id = id
        self.titre = titre
        self.description = description
        self.auteur = auteur
        self.statut = statut

    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "auteur": self.auteur,
            "statut": self.statut
        }
