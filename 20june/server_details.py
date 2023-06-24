def details():
    endpoint = "ws://nimblewebstream.lisuns.com:4575"
    port = "4575"
    api_key = "40e5c1ea-15a5-495f-9cd5-79b4ab1fa347"
    auth_message = {
        "function": "Authenticate",
        "apikey": api_key
    }

    return endpoint, port, auth_message, api_key
