from typing import Dict, Optional


class DNSDatabase(object):
    def __init__(self, source_file: str = "/etc/myhosts") -> None:
        self._source_file: str = source_file

        self._data: Dict[str, str] = self._load_data(source_file)

    def _load_data(self, source_file: str):
        data: Dict[str, str] = {}
        with open(source_file, "r") as data_file:
            for record in data_file.readlines():
                ip, host = record.split()
                data[host.lower()] = ip

        return data

    def get_ip_of_domain(self, domain: str) -> Optional[str]:
        return self._data.get(domain, None)


dns_database = DNSDatabase(source_file="/etc/myhosts")
