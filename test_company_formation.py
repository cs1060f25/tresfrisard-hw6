import pytest
import re
from app import CompanyFormation, generate_delaware_articles, generate_california_articles, generate_california_llc_certificate, generate_new_york_articles, generate_new_york_llc_certificate
from pydantic import ValidationError
from PyPDF2 import PdfReader
import io

# Test data
VALID_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
    'DC', 'PR', 'GU', 'VI', 'AS', 'MP'
]

def normalize_text(text):
    """Normalize PDF-extracted text by collapsing whitespace and uppercasing."""
    return re.sub(r'\s+', ' ', text.strip()).upper()

def test_state_validation():
    # Test all valid states
    for state in VALID_STATES:
        data = {
            "company_name": "Test Company",
            "state_of_formation": state,
            "company_type": "corporation",
            "incorporator_name": "Test User"
        }
        company = CompanyFormation(**data)
        assert company.state_of_formation == state.upper()

    # Test invalid state
    with pytest.raises(ValidationError):
        data = {
            "company_name": "Test Company",
            "state_of_formation": "XX",
            "company_type": "corporation",
            "incorporator_name": "Test User"
        }
        CompanyFormation(**data)

def test_pdf_generation():
    test_data = {
        "company_name": "Basic Test Company",
        "state_of_formation": "DE",
        "company_type": "corporation",
        "incorporator_name": "Testy McTestface"
    }
    
    pdf_buffer = generate_delaware_articles(CompanyFormation(**test_data))
    pdf_buffer.seek(0)
    
    reader = PdfReader(pdf_buffer)
    text = "\n".join(page.extract_text() for page in reader.pages)
    
    assert "Basic Test Company" in text
    assert "Testy McTestface" in text
    assert "CERTIFICATE OF INCORPORATION" in text
    assert "FIRST: The name of this corporation is:" in text
    assert "SECOND: Its registered office in the State of Delaware" in text
    assert "THIRD: The purpose of the corporation is to engage" in text
    assert "FOURTH: The total number of shares of stock" in text
    assert "IN WITNESS WHEREOF, the undersigned" in text

def test_california_corporation_pdf():
    test_data = {
        "company_name": "California Test Corp",
        "state_of_formation": "CA",
        "company_type": "corporation",
        "incorporator_name": "Testy McTestface"
    }
    
    pdf_buffer = generate_california_articles(CompanyFormation(**test_data))
    pdf_buffer.seek(0)
    
    reader = PdfReader(pdf_buffer)
    text = "\n".join(page.extract_text() for page in reader.pages)
    
    assert "California Test Corp" in text
    assert "ARTICLES OF INCORPORATION" in text
    assert "ARTICLE I: The name of this corporation is:" in text
    assert "ARTICLE II: The purpose of the corporation" in text
    assert "ARTICLE III: The name and address in California" in text

def test_california_llc_pdf():
    test_data = {
        "company_name": "California Test LLC",
        "state_of_formation": "CA",
        "company_type": "LLC",
        "incorporator_name": "Testy McTestface"
    }
    
    pdf_buffer = generate_california_llc_certificate(CompanyFormation(**test_data))
    pdf_buffer.seek(0)
    
    reader = PdfReader(pdf_buffer)
    text = "\n".join(page.extract_text() for page in reader.pages)
    
    assert "California Test LLC" in text
    assert "ARTICLES OF ORGANIZATION" in text
    assert "ARTICLE I: The name of the limited liability company is:" in text
    assert "ARTICLE II: The purpose of the limited liability company" in text
    assert "ARTICLE III: The name and address in California" in text

def test_new_york_corporation_pdf():
    test_data = {
        "company_name": "Test Company",
        "state_of_formation": "NY",
        "company_type": "corporation",
        "incorporator_name": "Testy McTestface"
    }
    
    pdf_buffer = generate_new_york_articles(CompanyFormation(**test_data))
    pdf_buffer.seek(0)
    
    reader = PdfReader(pdf_buffer)
    text = normalize_text("\n".join(page.extract_text() for page in reader.pages))
    
    # Verify full key content matching the image
    assert "CERTIFICATE OF INCORPORATION OF TEST COMPANY" in text
    assert "UNDER SECTION 402 OF THE BUSINESS CORPORATION LAW" in text
    assert "FIRST: THE NAME OF THIS CORPORATION IS: TEST COMPANY" in text
    assert "SECOND: THE PURPOSE OF THE CORPORATION IS TO ENGAGE IN ANY LAWFUL ACT OR ACTIVITY FOR WHICH A CORPORATION MAY BE ORGANIZED UNDER THE BUSINESS CORPORATION LAW. THE CORPORATION IS NOT FORMED TO ENGAGE IN ANY ACT OR ACTIVITY REQUIRING THE CONSENT OR APPROVAL OF ANY STATE OFFICIAL, DEPARTMENT, BOARD, AGENCY OR OTHER BODY WITHOUT SUCH CONSENT OR APPROVAL FIRST BEING OBTAINED." in text
    assert "THIRD: THE COUNTY, WITHIN THIS STATE, IN WHICH THE OFFICE OF THE CORPORATION IS TO BE LOCATED IS: ALBANY COUNTY." in text
    assert "FOURTH: THE CORPORATION SHALL HAVE AUTHORITY TO ISSUE ONE CLASS OF SHARES CONSISTING OF 1,000 COMMON SHARES WITH $0.01 PAR VALUE PER SHARE." in text
    assert "FIFTH: THE SECRETARY OF STATE IS DESIGNATED AS AGENT OF THE CORPORATION UPON WHOM PROCESS AGAINST THE CORPORATION MAY BE SERVED. THE POST OFFICE ADDRESS TO WHICH THE SECRETARY OF STATE SHALL MAIL A COPY OF ANY PROCESS AGAINST THE CORPORATION SERVED UPON THE SECRETARY OF STATE BY PERSONAL DELIVERY IS: 418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207" in text
    assert "INCORPORATOR: /S/ TESTY MCTESTFACE 418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207" in text
    assert "FILER'S NAME AND ADDRESS: /S/ TESTY MCTESTFACE 418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207" in text

def test_new_york_llc_pdf():
    test_data = {
        "company_name": "Test Company",
        "state_of_formation": "NY",
        "company_type": "LLC",
        "incorporator_name": "Testy McTestface"
    }
    
    pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**test_data))
    pdf_buffer.seek(0)
    
    reader = PdfReader(pdf_buffer)
    text = normalize_text("\n".join(page.extract_text() for page in reader.pages))
    
    # Verify full key content matching the image
    assert "ARTICLES OF ORGANIZATION OF TEST COMPANY" in text
    assert "UNDER SECTION 203 OF THE LIMITED LIABILITY COMPANY LAW" in text
    assert "FIRST: THE NAME OF THE LIMITED LIABILITY COMPANY IS: TEST COMPANY" in text
    assert "SECOND: THE COUNTY, WITHIN THIS STATE, IN WHICH THE OFFICE OF THE LIMITED LIABILITY COMPANY IS TO BE LOCATED IS: ALBANY COUNTY." in text
    assert "THIRD: THE SECRETARY OF STATE IS DESIGNATED AS AGENT OF THE LIMITED LIABILITY COMPANY UPON WHOM PROCESS AGAINST THE LIMITED LIABILITY COMPANY MAY BE SERVED. THE POST OFFICE ADDRESS TO WHICH THE SECRETARY OF STATE SHALL MAIL A COPY OF ANY PROCESS AGAINST THE LIMITED LIABILITY COMPANY SERVED UPON THE SECRETARY OF STATE BY PERSONAL DELIVERY IS: 418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207" in text
    assert "ORGANIZER: /S/ TESTY MCTESTFACE 418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207" in text
    assert "FILER'S NAME AND ADDRESS: /S/ TESTY MCTESTFACE 418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207" in text