from typing import TypedDict, Dict


class T_Enquiry_Json(TypedDict):
    index: str


# Response from the server to the view.
class T_Response_Json(TypedDict):
    db_index: str  # What is the current DB index
    message_count: str  # How many messages this response contains
    container: str  # Container ID that processed this request
    records: Dict[str, str]  # Dictionary of records


class T_Message_Json(TypedDict):
    username: str  # Client username
    message: str  # Client message


class T_Yell_Json(T_Message_Json):
    index: str  # Local user message index
    time: str  # Time of the request
    app_node: str  # Container ID that processed this request
    # (Though, this gets sent to the logger, hence it's called app_node)






