from scraper.doctolib_scraper import scrape_doctolib
from scraper.config import get_user_inputs

def print_results(doctors):
    """
    Print the scraped doctor information in a formatted way
    """
    print("\n" + "="*50)
    print(f"RÉSULTATS DE LA RECHERCHE: {len(doctors)} médecins trouvés")
    print("="*50)
    
    for i, doctor in enumerate(doctors, 1):
        print(f"\n{i}. {doctor['name']}")
        print(f"   Spécialité: {doctor['specialty']}")
        print(f"   Adresse: {doctor['address']}")
        print("-"*50)

def main():
    print("=== Doctolib Scraper ===")
    user_inputs = get_user_inputs()
    
    print("\nDémarrage de la recherche...")
    print(f"Recherche de \"{user_inputs['query']}\" à \"{user_inputs['location']}\"")
    
    results = scrape_doctolib(user_inputs)
    
    if results:
        print_results(results)
    else:
        print("\nAucun résultat trouvé ou une erreur est survenue.")

if __name__ == "__main__":
    main()