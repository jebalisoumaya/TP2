def get_user_inputs():
    query = input("Requête médicale (ex : dermatologue) : ")
    location = input("Adresse/ville/code postal : ")
    
    
    return {
        "query": query,
        "location": location,
    
    }