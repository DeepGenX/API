### Code generation:
To generate output for a given input, send a post request to http://ADDRESS:PORT/generate and specify these `json` parameters (NOTE: Don't set defaults in the extensions themselves because if we want to change a default value, we'd have to change it in the extension for every IDE instead of just once on the VPS):
- token: The token to authenticate the request
- input: The code that the user has written so far (from the start of the document to the line that the cursor is on, including that line)
- formatter (optional): The formatter to use to format the input and output code, black will be used by default
- max_length (optional): The max amount of tokens to generate
- temperature (optional): I have no clue what this does, it's used for generating output with GPT-J, unless you know what it does, just leave it out and it'll be defaulted to whatever it is in api.py as default
- top_p (optional): Same thing as temperature, no clue, if left empty, it's set to the default in api.py

### Response format:
The response format is a json string containing these values:
- success: Success contains a boolean that specifies whether the processing of the request went well or failed, if it's true, it means that everything is fine and you should be able to read the output, if not, take a look at the error value
- error (only present when success is false): When success is false the error value will be set to a json object containing a code and a string giving a basic description of what went wrong
- message (only present when success is true): When success is true the message value will be set to whatever GPT-J outputted after it has been parsed
Examples:
{"success": true, "message": ["abjiwjiodaoijdw"]}
{"success", false, "error": {"code": "MISSING_PARAMETER", "message": "Missing input parameter."}}

### Errors and their meanings (not all errors are listed here, just a few, the errors.py file contains all errors and they shouldn't be too hard to understand):
When something goes wrong the error value will be set, here is a list of what some errors mean:
- TOKEN_INVALID: The token specified in the request is invalid, maybe someone made a typo or maybe the user did not generate a token yet
- TOKEN_DISABLED: The token specified in the request has been disabled because it has been used in a way that is not permitted

### Misc:
- Token format: {Hash function used}.{64 Random characters}.{Hashed email}
- The path to the token file should be stored in an environment variable called `CODEGENX_TOKEN_FILE` and the email and password used to verify users should be in an environment variable called `CODEGENX_EMAIL_ADDRESS` and `CODEGENX_EMAIL_PASSWORD`
