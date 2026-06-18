from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOADED_SUCCESS = "File uploaded success"
    FILE_UPLOADED_FAILED = "File upload failure"
    PROCESSING_SUCCESS = "Processing success"
    PROCESSING_FAILED = "Processing failed"
    NO_FILES_ERROR = "No files found"
    FILE_ID_ERROR= "No file found with this id"
    PROJECT_NOT_FOUND_ERROR = "Project not found"
    INSERT_INTO_VECTORDB_ERROR = "Insert_into_vector_database_error"
    INSERT_INTO_VECTORDB_SUCCESS = "Insert_into_vector_database_success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    RAG_ANSWER_ERROR = "Rag_answer_error"
    RAG_ANSWER_SUCCESS = "Rag_answer_success"