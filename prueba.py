import requests

API_URL = "https://api-inference.huggingface.co/models/villefrancisco/finetuned_modelLegal"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
text = "Summarize this legal document: UNITED NATIONS EDUCATIONAL, SCIENTIFIC AND CULTURAL ORGANIZATIONCONVENTION CONCERNING THE PROTECTION OF THEWORLD CULTURAL AND NATURAL HERITAGEFINANCIAL REGULATIONS FOR THE WORLD HERITAGE FUND Article  15  of  the  Convention  concerning  the  Protection  of  the  World  Cultural  and  Natural Heritage (hereinafter referred to as \"the Convention\"), establishes a Fund, called \"the World Heritage Fund\" hereinafter referred to as \"the Fund\" which is to constitute a trust fund, in conformity with the provisions of the Financial Regulations of UNESCO. Consequently,  in  accordance  with  Regulation  6.7  of  the  Financial  Regulations  of  the  Organization,  the  Director-General  has  established  the  following  special  financial  regulations to govern the operations of this Fund.1. Purpose of the Fund1.1.The  purpose  of  this  Fund  shall  be  to  receive  contributions  from  the  sources  indicated  in  3.1  below  and  to  make  payments  there  from  to  assist  in  the  protection of properties forming part of the World Cultural and Natural Heritage of Outstanding Universal Value in accordance with the terms of the Convention and of the present Regulations. 2. Financial period of the Fund 2.1.The financial period shall be two consecutive calendar years coinciding with the financial period of the Regular Budget of UNESCO.3. Provision of funds3.1.The resources of the Fund shall consist of :(a)contributions   made   by   the   States   Parties   to   the   Convention,   in   accordance with its Article 16 ;(b)contributions, gifts or bequests which may be made by :i)  other States ;"

response = requests.post(API_URL, headers=headers, json={"inputs": text})

# Print the raw response and status code
print("Status Code:", response.status_code)
print("Response Text:", response.text)