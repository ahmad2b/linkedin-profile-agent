import os
import re
from typing import Any, Dict
import requests

class LinkedinTool:
    def __init__(self, api_key: str):
        if not api_key or len(api_key) == 0:
            raise ValueError(
                "Missing ProxyCurl API key. Please add PROXYCURL_API_KEY in your environment variables."
            )
        self.api_key = api_key

    def search_profile(self, profile_url: str) -> Dict[str, Any]:
        if not self.is_valid_linkedin_url(profile_url):
            raise ValueError("Invalid LinkedIn profile URL")

        url = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {'url': profile_url}

        response = self.fetch_data(url, params)

        return self.format_data(response)

    def search_company(self, company_url: str) -> Dict[str, Any]:
        if not self.is_valid_linkedin_url(company_url):
            raise ValueError("Invalid LinkedIn company URL")

        api_endpoint = "https://nubela.co/proxycurl/api/linkedin/company"
        params = {
            'url': company_url,
            'categories': 'include',
            'funding_data': 'include',
            'exit_data': 'include',
            'acquisitions': 'include',
            'extra': 'include',
            'use_cache': 'if-present',
            'fallback_to_cache': 'on-error'
        }

        response = self.fetch_data(api_endpoint, params)

        return self.format_data(response)

    def fetch_data(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers, params=params)

        if not response.ok:
            raise RuntimeError(
                f'Failed to fetch data from LinkedIn API. Status: {response.status_code}'
            )

        return response.json()

    def format_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        def clean_empty_keys(obj: Dict[str, Any]):
            keys_to_delete = []
            for key, value in obj.items():
                if (
                    value is None or value == '' or
                    (isinstance(value, dict) and not value) or
                    (isinstance(value, list) and not value)
                ):
                    keys_to_delete.append(key)
                elif isinstance(value, dict):
                    clean_empty_keys(value)
                    if not value:
                        keys_to_delete.append(key)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            clean_empty_keys(item)
                    if not value:
                        keys_to_delete.append(key)

            for key in keys_to_delete:
                del obj[key]

        clean_empty_keys(data)

        data.pop('people_also_viewed', None)
        data.pop('similarly_named_profiles', None)
        data.pop('activities', None)

        return data

    def is_valid_linkedin_url(self, url: str) -> bool:
        linkedin_url_regex = r'^https:\/\/www\.linkedin\.com\/(in|company)\/[a-zA-Z0-9-]+\/?$'
        return bool(re.match(linkedin_url_regex, str(url)))
