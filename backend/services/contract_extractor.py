"""
Service d'extraction de texte depuis des contrats (PDF ou images).
Utilise PyPDF2 pour les PDF et pytesseract pour l'OCR sur images.
"""

from pathlib import Path
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image


class ContractExtractor:
    def __init__(self):
        """
        Initialise le service d'extraction de contrat.
        """
        print("🔧 Initialisation du ContractExtractor...")
        # Tesseract path (Windows uniquement, à ajuster si installé)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        print("✅ ContractExtractor prêt")

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extrait le texte d'un fichier PDF.

        Args:
            pdf_path: Chemin vers le fichier PDF

        Returns:
            Texte extrait du PDF
        """
        try:
            reader = PdfReader(str(pdf_path))
            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            return text.strip()
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction PDF: {e}")
            raise e

    def extract_text_from_image(self, image_path: Path) -> str:
        """
        Extrait le texte d'une image via OCR (Tesseract).

        Args:
            image_path: Chemin vers l'image

        Returns:
            Texte extrait de l'image
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang="fra")
            return text.strip()
        except Exception as e:
            print(f"❌ Erreur lors de l'OCR: {e}")
            # Si Tesseract n'est pas installé, retourner un message d'erreur explicite
            if "tesseract is not installed" in str(e).lower():
                raise Exception(
                    "Tesseract OCR n'est pas installé. Veuillez utiliser un PDF ou installer Tesseract."
                )
            raise e

    def extract_text(self, file_path: Path) -> dict:
        """
        Extrait le texte d'un fichier (PDF ou image).
        Détecte automatiquement le type de fichier.

        Args:
            file_path: Chemin vers le fichier

        Returns:
            dict contenant le texte extrait et des métadonnées
        """
        file_extension = file_path.suffix.lower()

        if file_extension == ".pdf":
            print(f"📄 Extraction de texte depuis PDF: {file_path.name}")
            text = self.extract_text_from_pdf(file_path)
            method = "PDF"
        elif file_extension in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
            print(f"🖼️ Extraction de texte depuis image (OCR): {file_path.name}")
            text = self.extract_text_from_image(file_path)
            method = "OCR"
        else:
            raise ValueError(f"Type de fichier non supporté: {file_extension}")

        # Statistiques
        word_count = len(text.split())
        char_count = len(text)

        return {
            "text": text,
            "method": method,
            "stats": {
                "word_count": word_count,
                "char_count": char_count,
                "file_type": file_extension,
            },
        }


# Instance globale
_contract_extractor = None


def get_contract_extractor() -> ContractExtractor:
    """Retourne l'instance singleton du ContractExtractor"""
    global _contract_extractor
    if _contract_extractor is None:
        _contract_extractor = ContractExtractor()
    return _contract_extractor
