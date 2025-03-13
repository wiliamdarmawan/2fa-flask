from app import errors

def validate_json_api_params(params):
    if not params.get("data"):
        raise errors.InvalidParamsError("Missing `data` field")
    if not params.get("data").get("attributes"):
        raise errors.InvalidParamsError("Missing `data.attributes` field")
    return params.get("data").get("attributes")