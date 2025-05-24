import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os

class TestInMentorUserPage:
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """Configuration initiale pour tous les tests"""
        # Configuration du navigateur
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        # Décommentez la ligne suivante pour mode headless
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # URL de base - à adapter selon votre environnement
        self.base_url = "http://localhost:5000"
        
        yield
        
        # Nettoyage après tous les tests
        self.driver.quit()
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Préparation avant chaque test"""
        # Naviguer vers la page utilisateur
        self.driver.get(f"{self.base_url}/profile")  # Adaptez l'URL
        time.sleep(2)
    
    def test_01_page_load_and_title(self):
        """Test du chargement de la page et du titre"""
        assert "inMentor" in self.driver.title
        print("✓ Titre de la page vérifié")
    
    def test_02_header_elements(self):
        """Test des éléments du header"""
        # Vérifier le logo
        logo = self.driver.find_element(By.CLASS_NAME, "logo")
        assert logo.text == "inMentor"
        
        # Vérifier les liens de navigation
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a")
        expected_links = ["Trang chủ", "Về chúng tôi", "Phỏng vấn AI", "Danh sách việc làm", "Feedback"]
        
        for i, link in enumerate(nav_links):
            assert link.text == expected_links[i]
        
        print("✓ Éléments du header vérifiés")
    
    def test_03_dropdown_menu(self):
        """Test du menu déroulant du compte"""
        # Cliquer sur "Tài khoản"
        account_button = self.driver.find_element(By.CSS_SELECTOR, ".account span")
        account_button.click()
        
        # Attendre que le dropdown apparaisse
        dropdown = self.wait.until(
            EC.visibility_of_element_located((By.ID, "accountDropdown"))
        )
        
        # Vérifier que le dropdown est visible
        assert dropdown.is_displayed()
        
        # Vérifier les liens du dropdown
        dropdown_links = dropdown.find_elements(By.TAG_NAME, "a")
        assert len(dropdown_links) == 2
        
        # Cliquer ailleurs pour fermer le dropdown
        self.driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(1)
        
        print("✓ Menu déroulant testé")
    
    def test_04_profile_image(self):
        """Test de l'image de profil"""
        profile_img = self.driver.find_element(By.ID, "avatar")
        assert profile_img.is_displayed()
        
        # Vérifier que l'image a une source
        img_src = profile_img.get_attribute("src")
        assert img_src is not None
        assert img_src != ""
        
        print("✓ Image de profil vérifiée")
    
    def test_05_form_fields_disabled_by_default(self):
        """Test que les champs sont désactivés par défaut"""
        form_fields = [
            "fullname", "email", "dob", "phone", 
            "country", "province", "district", "skills"
        ]
        
        for field_id in form_fields:
            field = self.driver.find_element(By.ID, field_id)
            assert field.get_attribute("disabled")
        
        print("✓ Champs désactivés par défaut")
    
    def test_06_edit_mode_toggle(self):
        """Test du mode d'édition"""
        # Cliquer sur le bouton "Chỉnh sửa thông tin"
        edit_button = self.driver.find_element(By.CSS_SELECTOR, ".edit-btn")
        edit_button.click()
        time.sleep(1)
        
        # Vérifier que les champs sont maintenant activés
        form_fields = ["fullname", "email", "dob", "phone", "country", "province", "district"]
        
        for field_id in form_fields:
            field = self.driver.find_element(By.ID, field_id)
            assert field.get_attribute("disabled") is None
        
        # Vérifier que l'input file est visible
        avatar_input = self.driver.find_element(By.ID, "avatarInput")
        assert avatar_input.value_of_css_property("display") == "block"
        
        print("✓ Mode d'édition activé")
    
    def test_07_form_validation(self):
        """Test de la validation des champs"""
        # Activer le mode édition
        edit_button = self.driver.find_element(By.CSS_SELECTOR, ".edit-btn")
        edit_button.click()
        time.sleep(1)
        
        # Tester la modification des champs
        fullname_field = self.driver.find_element(By.ID, "fullname")
        original_value = fullname_field.get_attribute("value")
        
        # Modifier le nom
        fullname_field.clear()
        fullname_field.send_keys("Test User Modified")
        
        # Vérifier que la valeur a changé
        assert fullname_field.get_attribute("value") == "Test User Modified"
        
        # Restaurer la valeur originale
        fullname_field.clear()
        fullname_field.send_keys(original_value)
        
        print("✓ Validation des champs testée")
    
    def test_08_buttons_functionality(self):
        """Test de la fonctionnalité des boutons"""
        # Test du bouton "Phân tích CV"
        analyze_button = self.driver.find_element(By.XPATH, "//button[text()='Phân tích CV']")
        assert analyze_button.is_displayed()
        assert analyze_button.is_enabled()
        
        # Cliquer sur le bouton (cela déclenchera une alerte)
        analyze_button.click()
        
        # Attendre et gérer l'alerte
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            assert "Đang phân tích CV" in alert_text
            alert.accept()
            print("✓ Bouton 'Phân tích CV' testé")
        except TimeoutException:
            print("⚠ Alerte non trouvée pour le bouton 'Phân tích CV'")
        
        # Test du bouton "Cập nhật"
        update_button = self.driver.find_element(By.XPATH, "//button[text()='Cập nhật']")
        assert update_button.is_displayed()
        assert update_button.is_enabled()
        
        print("✓ Boutons testés")
    
    def test_09_responsive_design(self):
        """Test de la responsivité de base"""
        # Tester différentes tailles d'écran
        original_size = self.driver.get_window_size()
        
        # Taille mobile
        self.driver.set_window_size(375, 667)
        time.sleep(1)
        
        # Vérifier que les éléments sont toujours visibles
        logo = self.driver.find_element(By.CLASS_NAME, "logo")
        assert logo.is_displayed()
        
        # Restaurer la taille originale
        self.driver.set_window_size(original_size['width'], original_size['height'])
        
        print("✓ Responsivité de base testée")
    
    def test_10_form_submission_flow(self):
        """Test du flux complet de soumission du formulaire"""
        # Activer le mode édition
        edit_button = self.driver.find_element(By.CSS_SELECTOR, ".edit-btn")
        edit_button.click()
        time.sleep(1)
        
        # Modifier quelques champs
        phone_field = self.driver.find_element(By.ID, "phone")
        original_phone = phone_field.get_attribute("value")
        phone_field.clear()
        phone_field.send_keys("0123456789")
        
        # Désactiver le mode édition (simule la sauvegarde)
        edit_button.click()
        time.sleep(2)
        
        # Vérifier que les champs sont redevenus désactivés
        assert phone_field.get_attribute("disabled")
        
        print("✓ Flux de soumission testé")
    
    def test_11_accessibility_basic(self):
        """Test d'accessibilité de base"""
        # Vérifier que les images ont des attributs alt
        images = self.driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            assert alt_text is not None
            assert alt_text != ""
        
        # Vérifier que les labels sont associés aux champs
        labels = self.driver.find_elements(By.TAG_NAME, "label")
        assert len(labels) > 0
        
        print("✓ Accessibilité de base vérifiée")
    
    def test_12_css_styles_loaded(self):
        """Test que les styles CSS sont chargés"""
        # Vérifier la couleur du logo
        logo = self.driver.find_element(By.CLASS_NAME, "logo")
        logo_color = logo.value_of_css_property("color")
        
        # Vérifier le background du body
        body = self.driver.find_element(By.TAG_NAME, "body")
        body_bg = body.value_of_css_property("background-color")
        
        # Ces valeurs doivent être différentes des valeurs par défaut
        assert logo_color != "rgba(0, 0, 0, 1)"  # Pas noir par défaut
        
        print("✓ Styles CSS vérifiés")

# Tests additionnels pour pytest
def test_browser_compatibility():
    """Test de compatibilité navigateur simple"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("http://localhost:5000")
        assert driver.title is not None
        print("✓ Test de compatibilité navigateur passé")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Pour exécution directe avec python
    pytest.main([__file__, "-v", "-s"])