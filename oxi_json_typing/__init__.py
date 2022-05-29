from typing import TypedDict, Dict, Union


class T_Enquiry_Json(TypedDict):
    index: str
    max_load: str


# Response from the server to the view.
class T_Response_Json(TypedDict):
    db_index: str  # What is the current DB index
    message_count: str  # How many messages this response contains
    container: str  # Container ID that processed this request
    records: Dict[str, str]  # Dictionary of records


class T_Message_Json(TypedDict):
    username: Union[str, bytes]  # Client username
    message: Union[str, bytes]  # Client message


class T_Yell_Json(T_Message_Json):
    index: Union[str, bytes]
    time: Union[str, bytes]  # Time of the request
    app_node: Union[str, bytes]  # Container ID that processed this request
    # (Though, this gets sent to the logger, hence it's called app_node)






