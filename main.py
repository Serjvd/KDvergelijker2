"""
Hoofdscript voor het vergelijken van twee kwalificatiedossiers.
"""
import os
import argparse
import sys
from typing import Dict, Any

from pdf_extractor import PDFExtractor
from comparator import DossierComparator
from exporter import ExcelExporter


def extract_data_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Extraheert alle relevante data uit een PDF-bestand.
    
    Args:
        pdf_path: Pad naar het PDF-bestand
        
    Returns:
        Dictionary met geëxtraheerde data
    """
    print(f"Bezig met extraheren van data uit: {os.path.basename(pdf_path)}")
    
    extractor = PDFExtractor(pdf_path)
    
    # Extraheer tekst
    extractor.extract_text()
    
    # Extraheer metadata
    metadata = extractor.extract_metadata()
    
    # Extraheer kerntaken
    kerntaken = extractor.extract_kerntaken()
    
    # Extraheer werkprocessen
    werkprocessen = extractor.extract_werkprocessen()
    
    # Extraheer beroepshouding
    beroepshouding = extractor.extract_beroepshouding()
    
    # Extraheer context
    context = extractor.extract_context()
    
    # Extraheer resultaat
    resultaat = extractor.extract_resultaat()
    
    # Extraheer vakkennis en vaardigheden
    vakkennis_vaardigheden = extractor.extract_vakkennis_vaardigheden()
    
    return {
        "metadata": metadata,
        "kerntaken": kerntaken,
        "werkprocessen": werkprocessen,
        "beroepshouding": beroepshouding,
        "context": context,
        "resultaat": resultaat,
        "vakkennis_vaardigheden": vakkennis_vaardigheden
    }


def compare_dossiers(oud_data: Dict[str, Any], nieuw_data: Dict[str, Any]) -> list:
    """
    Vergelijkt twee kwalificatiedossiers.
    
    Args:
        oud_data: Dictionary met geëxtraheerde data uit het oude dossier
        nieuw_data: Dictionary met geëxtraheerde data uit het nieuwe dossier
        
    Returns:
        Lijst van dictionaries met vergelijkingsresultaten
    """
    print("Bezig met vergelijken van de dossiers...")
    
    comparator = DossierComparator(oud_data, nieuw_data)
    results = comparator.compare_all()
    
    return results


def export_results(results: list, output_dir: str, filename_prefix: str) -> str:
    """
    Exporteert de vergelijkingsresultaten naar Excel.
    
    Args:
        results: Lijst van dictionaries met vergelijkingsresultaten
        output_dir: Directory waar de Excel-bestanden worden opgeslagen
        filename_prefix: Prefix voor de bestandsnaam
        
    Returns:
        Pad naar het aangemaakte Excel-bestand
    """
    print("Bezig met exporteren van resultaten naar Excel...")
    
    exporter = ExcelExporter(output_dir)
    filename = f"{filename_prefix}_vergelijking.xlsx"
    excel_path = exporter.export_to_excel(results, filename)
    
    # Voeg opmaak toe aan het Excel-bestand
    exporter.format_excel(excel_path)
    
    return excel_path


def main():
    """Hoofdfunctie voor het uitvoeren van de vergelijkingsanalyse."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Vergelijk twee kwalificatiedossiers.')
    parser.add_argument('oud_pdf', help='Pad naar het oude kwalificatiedossier (PDF)')
    parser.add_argument('nieuw_pdf', help='Pad naar het nieuwe kwalificatiedossier (PDF)')
    parser.add_argument('--output-dir', '-o', default='output', help='Directory voor output bestanden')
    parser.add_argument('--prefix', '-p', default='kwalificatiedossier', help='Prefix voor de bestandsnaam')
    
    args = parser.parse_args()
    
    # Controleer of de PDF-bestanden bestaan
    if not os.path.isfile(args.oud_pdf):
        print(f"Fout: Het oude PDF-bestand bestaat niet: {args.oud_pdf}")
        return 1
    
    if not os.path.isfile(args.nieuw_pdf):
        print(f"Fout: Het nieuwe PDF-bestand bestaat niet: {args.nieuw_pdf}")
        return 1
    
    # Maak de output directory aan als deze nog niet bestaat
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Extraheer data uit de PDF-bestanden
        oud_data = extract_data_from_pdf(args.oud_pdf)
        nieuw_data = extract_data_from_pdf(args.nieuw_pdf)
        
        # Vergelijk de dossiers
        results = compare_dossiers(oud_data, nieuw_data)
        
        # Exporteer de resultaten naar Excel
        excel_path = export_results(results, args.output_dir, args.prefix)
        
        print(f"\nVergelijkingsanalyse voltooid!")
        print(f"Resultaten zijn opgeslagen in:")
        print(f"- Excel: {excel_path}")
        print(f"- CSV: {excel_path.replace('.xlsx', '.csv')}")
        
        return 0
    
    except Exception as e:
        print(f"Er is een fout opgetreden: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
