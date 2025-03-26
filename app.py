
import streamlit as st
import tempfile
import os

from pdf_extractor import PDFExtractor
from comparator import DossierComparator
from exporter import ExcelExporter

def extract_data(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name

    extractor = PDFExtractor(tmp_path)
    extractor.extract_text()

    data = {
        "metadata": extractor.extract_metadata(),
        "kerntaken": extractor.extract_kerntaken(),
        "werkprocessen": extractor.extract_werkprocessen(),
        "beroepshouding": extractor.extract_beroepshouding(),
        "context": extractor.extract_context(),
        "resultaat": extractor.extract_resultaat(),
        "vakkennis_vaardigheden": extractor.extract_vakkennis_vaardigheden(),
    }

    os.unlink(tmp_path)  # Verwijder tijdelijk bestand
    return data

def main():
    st.set_page_config(page_title="Kwalificatiedossier Vergelijker", layout="wide")
    st.title("📄 Vergelijk kwalificatiedossiers")
    st.markdown("""Upload hieronder twee kwalificatiedossiers in PDF-formaat (oud en nieuw). 
Na verwerking kun je het verschil downloaden als Excel-bestand.""")

    col1, col2 = st.columns(2)
    with col1:
        oud_pdf = st.file_uploader("⬅️ Oud dossier (PDF)", type="pdf", key="oud")
    with col2:
        nieuw_pdf = st.file_uploader("➡️ Nieuw dossier (PDF)", type="pdf", key="nieuw")

    if oud_pdf and nieuw_pdf:
        with st.spinner("Bezig met verwerken en vergelijken..."):
            try:
                oud_data = extract_data(oud_pdf)
                nieuw_data = extract_data(nieuw_pdf)

                comparator = DossierComparator(oud_data, nieuw_data)
                results = comparator.compare_all()

                exporter = ExcelExporter(output_dir=".")
                output_file = exporter.export_to_excel(results, filename="vergelijking.xlsx")
                exporter.format_excel(output_file)

                st.success("✅ Vergelijking voltooid!")

                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📥 Download Excel-bestand",
                        data=f,
                        file_name="vergelijking.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ Er is een fout opgetreden tijdens verwerking: {e}")
    else:
        st.info("📂 Wacht op beide uploads...")

if __name__ == "__main__":
    main()
