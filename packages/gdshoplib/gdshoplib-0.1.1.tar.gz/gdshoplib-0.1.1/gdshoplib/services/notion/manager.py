# Менеджер управления Notion
import json
from core.manager.basemanager import BaseManager
from services.notion.models import (
    Product, ProductProperties, ProductSettings,
    properties_type_parse_map, properties_keys_map
)
from services.notion.models import User
from .settings import Settings


class NotionManager(BaseManager):
    SETTINGS = Settings
    OBJECTS_CACHE = None
    BASE_URL = "https://api.notion.com/v1/"

    def get_headers(self):
        return {
            **self.auth_headers(),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Accept": "application/json"
        }

    def auth(self):
        return True

    def auth_headers(self):
        return {"Authorization": "Bearer " + self.settings.NOTION_SECRET_TOKEN}

    def get_user(self, user_id):
        data = self.make_request(f'users/{user_id}', method='get').json()
        return User.parse_obj({**data, **{'email': data['person']["email"]}})

    def is_settings_block(self, block):
        return block['type'] == 'code' and \
            block['code'].get('caption', [{}])[0].get('plain_text') == '[base_settings]'

    def get_settings(self, product_id):
        # Поиск блока с настройками и загрузка
        for block_response in self.pagination(f'blocks/{product_id}/children/', method='get'):
            for raw_block in block_response.json()['results']:
                if self.is_settings_block(raw_block):
                    raw_settings = json.loads(
                        properties_type_parse_map['rich_text'](raw_block['code'])
                    )
                    return ProductSettings.parse_obj(raw_settings)

    def get_products(self):
        products = []
        for page in self.pagination(
            f'databases/{self.settings.PRODUCT_DB}/query', method='post', params=None
        ):
            for raw_product in page.json()['results']:
                product = self.parse_product(raw_product)
                product.settings = self.get_settings(product.id)
                products.append(product.dict())

        return products

    def get_product(self, sku):
        data = self.make_request(
            f'databases/{self.settings.PRODUCT_DB}/query',
            method='post',
            params={
                "filter": {
                    "property": "Наш SKU",
                    "rich_text": {
                        "contains": sku
                    }
                }
            }).json()['results'][0]

        return self.parse_product(data)

    def generate_sku(self, product):
        # Сгенерировать SKU на основе продукта
        return ""

    def set_sku(self):
        # Найти товары без SKU и проставить
        products = []
        for page in self.pagination(
            f'databases/{self.settings.PRODUCT_DB}/query', method='post', params={
                "filter": {
                    "property": "Наш SKU",
                    "rich_text": {
                        "is_empty": True
                    }
                }
            }
        ):
            for raw_product in page.json()['results']:
                product = self.parse_product(raw_product)
                product.settings = self.get_settings(product.id)
                products.append(product.dict())

        return products

    def update_product(self, data):
        ...

    def parse_properties(self, properties):
        result = {}
        for k, v in properties.items():
            key = properties_keys_map.get(v['id'], {}).get('key')
            if not key:
                continue
            value_parser = properties_type_parse_map.get(v['type'], lambda data: str(data))
            result.append(
                ProductProperties(name=k, value=value_parser(v), key=key)
            )

        return result

    def parse_product(self, product):
        _product = Product.parse_obj({
            **product,
            **{
                'created_by': self.get_user(product['created_by']['id']).email,
                'last_edited_by': self.get_user(product['last_edited_by']['id']).email,
                'properties': self.parse_properties(product['properties'])
            }}
        )
        return _product

    def pagination(self, url, *, params=None, **kwargs):
        _params = params or {}
        response = None
        while True:
            response = self.make_request(url, params=_params, **kwargs)
            next_cursor = self.pagination_next(response)

            match next_cursor:
                case None:
                    yield response
                case False:
                    yield response
                    return
                case _:
                    _params = {**_params, **dict(start_cursor=next_cursor)}

    def pagination_next(self, response):
        """Выдаем данные для следующего"""
        if not response:
            return None

        if not response.json().get('has_more'):
            return False

        return response.json()['next_cursor']
