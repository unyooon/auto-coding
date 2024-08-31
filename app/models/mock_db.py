from app.schemas.db_schema import DesignDocument

mock_data = {
    "design_documents": []
}


def get_doc():
    return mock_data["items"]


def add_doc(doc: DesignDocument):
    mock_data["items"].append(doc)
