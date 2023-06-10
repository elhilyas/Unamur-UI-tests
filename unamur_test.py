from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import os

PATH = "WEB DRIVER PATH"
UNAMUR = "https://unamur.be/"
PATH_SCREENSHOT = "PATH SCREENSHOT"

# Donne les droits de lecture, écriture au dossier voulu 
os.chmod(PATH_SCREENSHOT, 0o777)


def test_unamur_translation(initial_language) :
    """
    Parcours l'ensemble des ongles de la barre de navigation et traduis le site afin de voir si le site est traduit ou s'il renvoie a la page d'acceuil

    Args:
        initial_language (str): La langue initiale du site de l'unamur 
                "fr" ou "en"

    Returns:
        str: "Le site est uniquement disponible en français (fr) ou en anglais (en)" 
            -> Si le parametre "initial_language" n'est ni "fr" ou "en"

    Raises:
        StaleElementReferenceException: L'élément a été modifié ou n'est plus présent
        NoSuchElementException: L'élément n'a pas été trouvé
    """

    # Preparation du webdriver
    service = Service(PATH)
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")  # Résolution de la page en 1920x1080
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    link = UNAMUR

    # Préparation de certaines variables au bon fonctionnement du programme
    if initial_language == "fr":
        driver.get(link)
        translate_button = "siteaction-english"
        test_language = "en"
    elif initial_language == "en":
        link = link + "en"
        driver.get(link)
        translate_button = "siteaction-french"
        test_language = "fr"
    else:
        return "Le site est uniquement disponible en français (fr) ou en anglais (en)"

    
    try:
        # Recherche du conteneur parent
        navbar = driver.find_element(By.ID, "portal-shortcuts")

        # Recherche de tous les éléments <dl> dans le conteneur
        dl_elements = navbar.find_elements(By.TAG_NAME, "dl")

        # Parcourir les éléments <dl> et récupérer les IDs
        for dl_index in range(len(dl_elements)):

            # Raffraichir la liste d'elements
            navbar = driver.find_element(By.ID, "portal-shortcuts")
            dl_elements = navbar.find_elements(By.TAG_NAME, "dl")

            dl_id = dl_elements[dl_index].get_attribute("id")
            print(dl_id)

            # Clique sur le lien pour ouvrir le dropdown
            dropdown_link = dl_elements[dl_index].find_element(By.TAG_NAME, "a")
            dropdown_link.click()

            # Attente explicite jusqu'à ce que les éléments du dropdown soient visibles
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, dl_id)))

            # Recherche du dropdown par son ID après l'attente explicite
            dropdown = driver.find_element(By.ID, dl_id)

            # Récupérer à nouveau les éléments du dropdown
            dropdown_items = dropdown.find_elements(By.TAG_NAME, "li")

            for li_index in range(len(dropdown_items)):
                try:
                    dropdown_item = dropdown_items[li_index]
                    dropdown_item_a = None

                    # Tentative de récupération de l'élément <a> dans l'élément <li>
                    try:
                        dropdown_item_a = dropdown_item.find_element(By.TAG_NAME, 'a')

                    except NoSuchElementException:
                        dropdown_link.click()

                        dropdown_class = dropdown.get_attribute("class")

                        # Vérifier si la classe est "actionMenu deactivated"
                        if "actionMenu deactivated" in dropdown_class:
                            dropdown_link.click()
                        
                        continue

                    if dropdown_item_a is not None:
                        dropdown_class = dropdown.get_attribute("class")

                        # Vérifier si la classe est "actionMenu deactivated"
                        if "actionMenu deactivated" in dropdown_class:
                            dropdown_link.click()

                        # Récupérer l'attribut href du lien
                        href = dropdown_item_a.get_attribute("href")

                        # Vérifier si le lien est une ancre vers une autre partie du même site
                        if "https://www.unamur.be/" in href:

                            # Clique sur l'élément correspondant à l'index actuel
                            dropdown_item_a.click()

                            # Obtenir l'url de la page actuelle
                            current_url = driver.current_url
                            
                            if "https://www.unamur.be/" in current_url:
                                file_name = current_url.replace('/', '-')
                                file_name = file_name.replace(":", "-")
                                file_name1 = file_name + "--(1)-" + initial_language

                                # Premier screenshot en français
                                driver.save_screenshot("%s\\%s.png" % (PATH_SCREENSHOT, file_name1))
                                en_button = driver.find_element(By.ID,translate_button)

                                en_button.click()

                                # Deuxième screenshot en anglais
                                file_name2 =  file_name + "--(2)-" + initial_language + "-" + test_language 
                                driver.save_screenshot("%s\\%s.png" % (PATH_SCREENSHOT, file_name2))
                                
                            else:
                                print("Le lien pointe vers un autre domaine. %s" % current_url)


                            # Attendre que la page se mette à jour
                            WebDriverWait(driver, 10).until(EC.staleness_of(dropdown))

                            # Retour a la page d'acceuil
                            driver.get(link)

                            # Rechercher à nouveau le bouton pour ouvrir le dropdown
                            dropdown = driver.find_element(By.ID, dl_id)
                            dropdown_link = dropdown.find_element(By.TAG_NAME, "a")
                            dropdown_link.click()

                            # Attendre que le dropdown soit visible
                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, dl_id)))
                            
                            # Récupérer à nouveau les éléments du dropdown
                            dropdown_items = dropdown.find_elements(By.TAG_NAME, "li")
                        
                        # Vérifier si le lien pointe vers un autre domaine
                        else:
                            print("Le lien pointe vers un autre domaine. %s" % dropdown_item_a.text)
                            continue

                except StaleElementReferenceException:
                    # L'élément a été modifié ou n'est plus présent, passer à l'élément suivant
                    pass

                except Exception as e:
                    print("Une exception s'est produite:", e)
                    
                    
    except NoSuchElementException as e:
        print("L'élément dropdown n'a pas été trouvé:", e)

    except Exception as e:
        print("Une exception s'est produite:", e)

    finally:   
        # Fermeture du navigateur
        driver.quit()

        return "Fin de l'executuion des cas de tests" 
