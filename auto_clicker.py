import pyautogui
import keyboard
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor

class AutoClicker:
    def __init__(self):
        self.coordinates = []  # Format: [(x, y, nb_clics), ...]
        self.delay = 0
        self.is_capturing = False
        self.last_params = {
            'coordinates': [],
            'delay': 0
        }
        self.has_executed = False
        pyautogui.FAILSAFE = True
        
    def get_coordinates_interactive(self):
        """Lance le mode de capture interactive des coordonnées"""
        capture_thread = threading.Thread(target=self.start_coordinate_listener)
        capture_thread.start()
        capture_thread.join()

    def start_coordinate_listener(self):
        self.is_capturing = True
        print("\n📍 Mode Capture des Positions")
        print("---------------------------")
        print("→ F2: Capturer la position actuelle du curseur")
        print("→ F3: Terminer la capture")
        print("→ Échap: Quitter le programme\n")
        
        while self.is_capturing:
            if keyboard.is_pressed('F2'):
                x, y = pyautogui.position()
                nb_clics = self.get_click_count()
                self.coordinates.append((x, y, nb_clics))
                print(f"✅ Position capturée: ({x}, {y}) - {nb_clics} clics")
                time.sleep(0.3)
            elif keyboard.is_pressed('F3'):
                self.is_capturing = False
                print("\n✅ Capture terminée avec succès!")
                break
            elif keyboard.is_pressed('esc'):
                self.is_capturing = False
                print("\n❌ Programme terminé par l'utilisateur")
                exit()

    def get_click_count(self):
        while True:
            try:
                clicks = int(input("\nEntrez le nombre de fois que le clic doit être effectué à cette position : "))
                if clicks > 0:
                    return clicks
                print("❌ Le nombre de clics doit être supérieur à 0.")
            except ValueError:
                print("❌ Veuillez entrer un nombre entier valide.")

    def show_coordinates(self):
        if not self.coordinates:
            print("\n⚠️ Aucune position enregistrée.")
            print("→ Utilisez l'option 1 pour capturer des positions.")
            return False
        
        print("\n📋 Liste des positions enregistrées:")
        print("--------------------------------")
        for i, (x, y, clicks) in enumerate(self.coordinates, 1):
            print(f"{i}. Position ({x}, {y}) - {clicks} clics")
        return True

    def modify_coordinates(self):
        if not self.show_coordinates():
            return

        while True:
            try:
                print("\n✏️ Menu de Modification")
                print("-------------------")
                print("1. Modifier une position")
                print("2. Supprimer une position")
                print("3. Retour au menu principal")
                choice = input("\nVotre choix : ")
                
                if choice == '1':
                    idx = int(input(f"\nNuméro de la position à modifier (1-{len(self.coordinates)}) : ")) - 1
                    if 0 <= idx < len(self.coordinates):
                        print("\n1. Modifier les coordonnées")
                        print("2. Modifier le nombre de clics")
                        mod_choice = input("\nVotre choix : ")
                        
                        if mod_choice == '1':
                            print("\n→ Placez votre curseur à la nouvelle position et appuyez sur F2...")
                            while True:
                                if keyboard.is_pressed('F2'):
                                    x, y = pyautogui.position()
                                    self.coordinates[idx] = (x, y, self.coordinates[idx][2])
                                    print(f"✅ Nouvelle position enregistrée : ({x}, {y})")
                                    time.sleep(0.3)
                                    break
                        elif mod_choice == '2':
                            new_clicks = self.get_click_count()
                            self.coordinates[idx] = (self.coordinates[idx][0], 
                                                   self.coordinates[idx][1], 
                                                   new_clicks)
                            print(f"✅ Nombre de clics modifié : {new_clicks}")
                
                elif choice == '2':
                    idx = int(input(f"\nNuméro de la position à supprimer (1-{len(self.coordinates)}) : ")) - 1
                    if 0 <= idx < len(self.coordinates):
                        del self.coordinates[idx]
                        print("✅ Position supprimée avec succès.")
                
                elif choice == '3':
                    break
                
                self.show_coordinates()
            
            except (ValueError, IndexError):
                print("❌ Entrée invalide. Veuillez réessayer.")

    def get_delay(self):
        while True:
            try:
                print("\n💡 Note: 1000 ms = 1 seconde")
                print("Exemple: 100 ms = 0.1 seconde")
                delay_str = input("\nEntrez le délai entre les clics (en millisecondes) : ")
                self.delay = float(delay_str) / 1000  # Conversion en secondes
                if self.delay >= 0:
                    break
                print("❌ Le délai doit être positif ou nul.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")

    def perform_click(self, coord):
        x, y, nb_clics = coord
        try:
            for i in range(nb_clics):
                pyautogui.click(x, y)
                print(f"✅ Clic {i+1}/{nb_clics} effectué à ({x}, {y})")
                time.sleep(self.delay)
        except Exception as e:
            print(f"❌ Erreur lors du clic à ({x}, {y}): {str(e)}")

    def execute_clicks(self):
        if not self.coordinates:
            print("\n⚠️ Impossible d'exécuter les clics!")
            print("→ Aucune position n'a été capturée")
            print("→ Utilisez d'abord l'option 1 pour capturer des positions")
            return False

        print("\n🚀 Exécution des clics automatiques")
        print("--------------------------------")
        print(f"Nombre de positions : {len(self.coordinates)}")
        print(f"Délai entre les clics : {self.delay * 1000} millisecondes")
        
        self.last_params['coordinates'] = self.coordinates.copy()
        self.last_params['delay'] = self.delay
        self.has_executed = True
        
        with ThreadPoolExecutor(max_workers=len(self.coordinates)) as executor:
            executor.map(self.perform_click, self.coordinates)
        return True

    def execute_last_params(self):
        if not self.has_executed:
            print("\n⚠️ Aucune exécution précédente!")
            print("→ Vous devez d'abord exécuter les clics au moins une fois (option 3)")
            return

        if not self.last_params['coordinates']:
            print("\n⚠️ Aucun paramètre précédent disponible!")
            print("→ Capturez d'abord des positions (option 1)")
            print("→ Puis exécutez les clics (option 3)")
            return
            
        self.coordinates = self.last_params['coordinates'].copy()
        self.delay = self.last_params['delay']
        print("\n🔄 Utilisation des derniers paramètres :")
        print(f"Délai : {self.delay * 1000} millisecondes")
        self.show_coordinates()
        self.execute_clicks()

def main():
    print("🎯 Auto-Clicker")
    print("Un outil pour automatiser vos clics")
    print("--------------------------------")
    
    clicker = AutoClicker()
    
    while True:
        print("\n📋 Menu Principal")
        print("-------------")
        print("1. Capturer de nouvelles positions")
        print("2. Afficher/Modifier les positions")
        print("3. Exécuter les clics")
        print("4. Réexécuter avec les derniers paramètres")
        print("5. Quitter")
        
        choix = input("\nVotre choix : ")
        
        if choix == '1':
            clicker.coordinates = []
            print("\n📌 Mode Capture")
            print("→ Placez votre curseur aux positions souhaitées")
            print("→ Appuyez sur F2 pour capturer chaque position")
            print("→ Appuyez sur F3 quand vous avez terminé")
            clicker.get_coordinates_interactive()
        
        elif choix == '2':
            if not clicker.coordinates:
                print("\n⚠️ Aucune position n'est enregistrée!")
                print("→ Utilisez d'abord l'option 1 pour capturer des positions")
                continue
            clicker.modify_coordinates()
            
        elif choix == '3':
            if not clicker.coordinates:
                print("\n⚠️ Impossible d'exécuter les clics!")
                print("→ Aucune position n'a été capturée")
                print("→ Utilisez d'abord l'option 1 pour capturer les positions souhaitées")
                continue
            clicker.get_delay()
            clicker.execute_clicks()
            
        elif choix == '4':
            clicker.execute_last_params()
            
        elif choix == '5':
            print("\n👋 Merci d'avoir utilisé Auto-Clicker!")
            break
            
        else:
            print("\n❌ Option invalide!")
            print("→ Veuillez choisir une option entre 1 et 5")

if __name__ == "__main__":
    main()