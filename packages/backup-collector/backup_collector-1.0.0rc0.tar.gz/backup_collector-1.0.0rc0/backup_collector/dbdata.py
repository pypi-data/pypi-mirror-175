from pydantic.dataclasses import dataclass
from networktools.ip import validURL, validPORT
from pydantic import ValidationError, validator
from dataclasses import dataclass as std_dataclass, asdict

@dataclass
class DBData:
    host: str
    port: int
    dbname: str

    @validator("host")
    def check_host_is_url(cls, value):
        assert validURL(value), "It's not a valid host url"
        return value
    
    @validator("port")
    def check_port_is_valid(cls, value):
        assert validPORT(value), "It's not a valid port value 0 to 65534"
        return value

    def dict(self):
        return asdict(self)
