#!/usr/bin/env python
# coding: utf-8

from uuid import uuid4
import requests

from .exceptions import BadResponse
from .utils import check_status_code


def is_json_has_path(json, path):
    current_element = json
    for path_element in path:
        if not current_element.get(path_element):
            return False
        else:
            current_element = current_element[path_element]
    return True


def generate_client_id():
    return "mybee%3B{}%3Bandroid_22%3B4.26.1_965".format(uuid4())


def get_balance(number, password):
    session = requests.Session()
    token_response = session.get(
        "http://api.beeline.ru/mw/auth/1/auth",
        params={
            "client_id": generate_client_id(),
            "login": number,
            "password": password,
        },
    )
    check_status_code(token_response, 200)
    if not token_response.json().get("token"):
        raise BadResponse("Token not found", token_response)
    token = token_response.json()["token"]

    balance_response = session.get(
        "https://api.beeline.ru/mobile/api/v1/dynamic/data",
        params={"blocks": "Profile_Balance"},
        headers={"X-Auth-Token": token, "X-Login": number, "X-CTN": number},
    )
    check_status_code(balance_response, 200)
    if not is_json_has_path(
        balance_response.json(), ["data", "profile_Balance", "balance", "value"]
    ):
        raise BadResponse("Incorrect balance response", balance_response)
    return balance_response.json()["data"]["profile_Balance"]["balance"]["value"]
