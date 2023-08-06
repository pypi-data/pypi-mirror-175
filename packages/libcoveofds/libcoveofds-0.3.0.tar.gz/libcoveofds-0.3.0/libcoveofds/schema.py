import jsonref
import requests

from libcove2.common import schema_dict_fields_generator


class OFDSSchema:

    # The latest commit hash from https://github.com/Open-Telecoms-Data/open-fibre-data-standard/commits/0.1-dev
    package_schema_url: str = "https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/b4dbea4705039610d893c12e688fd2a1f9b877ca/schema/network-package-schema.json"
    data_schema_url: str = "https://raw.githubusercontent.com/Open-Telecoms-Data/open-fibre-data-standard/b4dbea4705039610d893c12e688fd2a1f9b877ca/schema/network-schema.json"

    def get_package_schema(self):
        r = requests.get(self.package_schema_url)
        return r.json()

    def get_package_schema_dereferenced(self):
        r = requests.get(self.package_schema_url)
        return jsonref.loads(r.text)

    def get_data_schema(self):
        r = requests.get(self.data_schema_url)
        return r.json()

    def get_link_rels_for_external_nodes(self) -> list:
        return [
            "tag:opentelecomdata.net,2022:nodesAPI",
            "tag:opentelecomdata.net,2022:nodesFile",
        ]

    def get_link_rels_for_external_spans(self) -> list:
        return [
            "tag:opentelecomdata.net,2022:spansAPI",
            "tag:opentelecomdata.net,2022:spansFile",
        ]

    def get_package_schema_fields(self) -> set:
        return set(schema_dict_fields_generator(self.get_package_schema_dereferenced()))

    def extract_data_ids_from_data_and_path(self, data: dict, path: list) -> dict:
        out: dict = {}
        # network_id
        if len(path) >= 2 and path[0] == "networks":
            network_id = data["networks"][path[1]].get("id")
            if network_id:
                out["network_id"] = network_id
        # other ids
        for field in ["node", "span"]:
            if len(path) >= 4 and path[0] == "networks" and path[2] == field + "s":
                id = data["networks"][path[1]][field + "s"][path[3]].get("id")
                if id:
                    out[field + "_id"] = id
        # return
        return out
