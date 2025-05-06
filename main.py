from scraper.doctolib_scraper import scrape_doctolib
from scraper.config import get_user_inputs
import os

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
        
        # Print availability if available
        if doctor.get('availability') and doctor['availability'] != "Unknown":
            print(f"   Disponibilité: {doctor['availability']}")
            
        # Print tarif if available
        if doctor.get('tarif') and doctor['tarif'] != "Unknown":
            print(f"   Tarif: {doctor['tarif']}")
            
        # Print convention if available
        if doctor.get('convention') and doctor['convention'] != "Unknown":
            print(f"   Convention: {doctor['convention']}")
            
        print("-"*50)
    
    # Inform user about the CSV export
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    print(f"\nLes résultats ont également été exportés au format CSV dans le dossier:\n{data_dir}")

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