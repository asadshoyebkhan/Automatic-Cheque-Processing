# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
from difflib import SequenceMatcher
from indiancurrencyconvertor import num2words


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



def analyze_custom_documents(custom_model_id,image):

    # from dotenv import load_dotenv
    # load_dotenv()

    # path_to_sample_documents = os.path.abspath(
    #     os.path.join(
    #         os.path.abspath(__file__), "..", "./Test/Cheque 309061.jpg"
    #     )
    # )
    # [START analyze_custom_documents]
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
    key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
    model_id = os.getenv("CUSTOM_BUILT_MODEL_ID", custom_model_id)

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Make sure your document's type is included in the list of document types the custom model can analyze
    # with open(path_to_sample_documents, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
            model_id=model_id, document=image)
    result = poller.result()

    cheque_data={}
    for idx, document in enumerate(result.documents):
        # print("--------Analyzing document #{}--------".format(idx + 1))
        # print("Document has type {}".format(document.doc_type))
        # print("Document has confidence {}".format(document.confidence))
        # print("Document was analyzed by model with ID {}".format(result.model_id))
        for field_name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            cheque_data[field_name]=field_value
            # print("......found field Name '{}' with value '{}' and with confidence {}".format(field_name, field_value, field.confidence))

    cheque_data['Amount']=int(cheque_data['Amount'])
    cheque_data['Account No.']=int(cheque_data['Account No.'])
    cheque_data['Cheque No.']=int(''.join(filter(str.isdigit, cheque_data['Cheque No.'])))
    cheque_data['Amount in words']=cheque_data['Amount in words'].lower()
    amount_in_words=num2words(cheque_data['Amount'])

    # getting similarity ratio of amount in words and amount in number
    amount_similarity_ratio=similar(amount_in_words,cheque_data["Amount in words"])

    if amount_similarity_ratio>0.8:
        cheque_data['Amount in words']=amount_in_words
    else:
        return 'Amount in words is not matching with the specified amount' 
    return(cheque_data)

    # # iterate over tables, lines, and selection marks on each page
    # for page in result.pages:
    #     print("\nLines found on page {}".format(page.page_number))
    #     for line in page.lines:
    #         print("...Line '{}'".format(line.content))
    #     for word in page.words:
    #         print(
    #             "...Word '{}' has a confidence of {}".format(
    #                 word.content, word.confidence
    #             )
    #         )
    #     for selection_mark in page.selection_marks:
    #         print(
    #             "...Selection mark is '{}' and has a confidence of {}".format(
    #                 selection_mark.state, selection_mark.confidence
    #             )
    #         )

    # for i, table in enumerate(result.tables):
    #     print("\nTable {} can be found on page:".format(i + 1))
    #     for region in table.bounding_regions:
    #         print("...{}".format(i + 1, region.page_number))
    #     for cell in table.cells:
    #         print(
    #             "...Cell[{}][{}] has content '{}'".format(
    #                 cell.row_index, cell.column_index, cell.content
    #             )
    #         )
    # print("-----------------------------------")
    # [END analyze_custom_documents]



model_id = None
if os.getenv("CONTAINER_SAS_URL") and not os.getenv("CUSTOM_BUILT_MODEL_ID"):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentModelAdministrationClient, ModelBuildMode

    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

    if not endpoint or not key:
        raise ValueError("Please provide endpoint and API key to run the samples.")

    document_model_admin_client = DocumentModelAdministrationClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    model = document_model_admin_client.begin_build_document_model(
        ModelBuildMode.TEMPLATE, blob_container_url=os.getenv("CONTAINER_SAS_URL")
    ).result()
    model_id = model.model_id

    # cheque_data=analyze_custom_documents(model_id)

    # print(cheque_data)
   