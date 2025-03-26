"""
Module voor het exporteren van vergelijkingsresultaten naar Excel en CSV.
"""
import os
import pandas as pd
from typing import List, Dict, Any

class ExcelExporter:
    """Klasse voor het exporteren van vergelijkingsresultaten naar Excel en CSV."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialiseert de ExcelExporter met een output directory.
        
        Args:
            output_dir: Directory waar de output bestanden worden opgeslagen
        """
        self.output_dir = output_dir
        
        # Maak output directory als deze nog niet bestaat
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def export_to_excel(self, comparison_results: List[Dict[str, Any]], prefix: str = "kwalificatiedossier") -> Dict[str, str]:
        """
        Exporteert vergelijkingsresultaten naar Excel en CSV.
        
        Args:
            comparison_results: Lijst van dictionaries met vergelijkingsresultaten
            prefix: Prefix voor de bestandsnaam
            
        Returns:
            Dictionary met paden naar de gegenereerde bestanden
        """
        # Sorteer de resultaten alfabetisch op codering_nieuw
        sorted_results = sorted(comparison_results, key=lambda x: x.get("codering_nieuw", ""))
        
        # Maak een DataFrame van de resultaten
        df = pd.DataFrame(sorted_results)
        
        # Hernoem de kolommen voor betere leesbaarheid
        df = df.rename(columns={
            "codering_oud": "Codering OUD",
            "naam_oud": "Naam OUD",
            "codering_nieuw": "Codering NIEUW",
            "naam_nieuw": "Naam NIEUW",
            "impact": "Impact op inhoud",
            "pagina": "Pagina"
        })
        
        # Bepaal de bestandspaden
        excel_path = os.path.join(self.output_dir, f"{prefix}_vergelijking.xlsx")
        csv_path = os.path.join(self.output_dir, f"{prefix}_vergelijking.csv")
        
        try:
            # Poging 1: Gebruik ExcelWriter met engine specificatie
            try:
                with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Vergelijking')
            except Exception as e1:
                print(f"Eerste poging mislukt: {str(e1)}")
                
                # Poging 2: Directe export met engine specificatie
                try:
                    df.to_excel(excel_path, index=False, engine='openpyxl')
                except Exception as e2:
                    print(f"Tweede poging mislukt: {str(e2)}")
                    
                    # Poging 3: Gebruik xlsxwriter engine
                    try:
                        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
                            df.to_excel(writer, index=False)
                    except Exception as e3:
                        print(f"Derde poging mislukt: {str(e3)}")
                        
                        # Fallback: Sla alleen op als CSV
                        print("Excel export mislukt, alleen CSV wordt opgeslagen")
        except Exception as e:
            print(f"Excel export mislukt: {str(e)}")
            print("Alleen CSV wordt opgeslagen")
        
        # Exporteer naar CSV (dit zou altijd moeten werken)
        df.to_csv(csv_path, index=False, sep=';')
        
        return {
            "excel": excel_path if os.path.exists(excel_path) else None,
            "csv": csv_path
        }
