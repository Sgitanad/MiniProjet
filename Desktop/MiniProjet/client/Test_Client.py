from client.client_taches import ClientTaches

def menu():
    client = ClientTaches()

    while True:
        print("\n--- MENU ---")
        print("1. Ajouter une tâche")
        print("2. Lister les tâches")
        print("3. Supprimer une tâche")
        print("4. Changer statut")
        print("5. Quitter")

        choix = input("> ")

        if choix == "1":
            titre = input("Titre : ")
            desc = input("Description : ")
            res = client.envoyer({"action": "add", "titre": titre, "description": desc})
            print("→ Réponse :", res)

        elif choix == "2":
            res = client.envoyer({"action": "list"})
            for t in res["taches"]:
                print(f"[{t['id']}] {t['titre']} - {t['statut']}")

        elif choix == "3":
            id = int(input("ID à supprimer : "))
            res = client.envoyer({"action": "delete", "id": id})
            print("→", res)

        elif choix == "4":
            id = int(input("ID : "))
            statut = input("Nouveau statut (TODO/DOING/DONE) : ")
            res = client.envoyer({"action": "status", "id": id, "statut": statut})
            print(res)

        elif choix == "5":
            break

        else:
            print("Choix invalide")
