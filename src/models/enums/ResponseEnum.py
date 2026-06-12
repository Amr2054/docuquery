from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOADED_SUCCESS = "File uploaded success"
    FILE_UPLOADED_FAILED = "File upload failure"
    PROCESSING_SUCCESS = "Processing success"
    PROCESSING_FAILED = "Processing failed"