import uuid
import string
import requests
import time
import sys

from pydantic import BaseModel, validator, root_validator
from dataclasses import dataclass
from datetime import datetime




from splunk_contentctl.objects.security_content_object import SecurityContentObject
from splunk_contentctl.objects.enums import AnalyticsType
from splunk_contentctl.objects.enums import DataModel
from splunk_contentctl.objects.detection_tags import DetectionTags
from splunk_contentctl.objects.deployment import Deployment
from splunk_contentctl.objects.unit_test import UnitTest
from splunk_contentctl.objects.macro import Macro
from splunk_contentctl.objects.lookup import Lookup
from splunk_contentctl.objects.baseline import Baseline
from splunk_contentctl.objects.playbook import Playbook
from splunk_contentctl.helper.link_validator import LinkValidator





class Detection(BaseModel, SecurityContentObject):
    # detection spec
    name: str
    id: str
    version: int
    date: str
    author: str
    type: str
    datamodel: list
    description: str
    search: str
    how_to_implement: str
    known_false_positives: str
    check_references: bool = False #Validation is done in order, this field must be defined first
    references: list
    tags: DetectionTags
    

    # enrichments
    deprecated: bool = None
    experimental: bool = None
    deployment: Deployment = None
    annotations: dict = None
    risk: list = None
    playbooks: list[Playbook] = None
    baselines: list[Baseline] = None
    mappings: dict = None
    test: UnitTest = None
    macros: list[Macro] = None
    lookups: list[Lookup] = None
    cve_enrichment: list = None
    splunk_app_enrichment: list = None
    file_path: str = None
    source: str = None
    nes_fields: str = None
    providing_technologies: list = None


    # @validator('name')
    # def name_max_length(cls, v, values):      
    #     if len(v) > 67:
    #         raise ValueError('name is longer then 67 chars: ' + v)
    #     return v

    @validator('name')
    def name_invalid_chars(cls, v):
        invalidChars = set(string.punctuation.replace("-", ""))
        if any(char in invalidChars for char in v):
            raise ValueError('invalid chars used in name: ' + v)
        return v

    @validator('id')
    def id_check(cls, v, values):
        try:
            uuid.UUID(str(v))
        except:
            raise ValueError('uuid is not valid: ' + values["name"])
        return v

    @validator('date')
    def date_valid(cls, v, values):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except:
            raise ValueError('date is not in format YYYY-MM-DD: ' + values["name"])
        return v

    @validator('type')
    def type_valid(cls, v, values):
        if v.lower() not in [el.name.lower() for el in AnalyticsType]:
            raise ValueError('not valid analytics type: ' + values["name"])
        return v

    @validator('datamodel')
    def datamodel_valid(cls, v, values):
        for datamodel in v:
            if datamodel not in [el.name for el in DataModel]:
                raise ValueError('not valid data model: ' + values["name"])
        return v

    @validator('description', 'how_to_implement')
    def encode_error(cls, v, values, field):
        try:
            v.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('encoding error in ' + field.name + ': ' + values["name"])
        return v

    @root_validator
    def search_validation(cls, values):
        if 'ssa_' not in values['file_path']:
            if not '_filter' in values['search']:
                raise ValueError('filter macro missing in: ' + values["name"])
            if any(x in values['search'] for x in ['eventtype=', 'sourcetype=', ' source=', 'index=']):
                if not 'index=_internal' in values['search']:
                    raise ValueError('Use source macro instead of eventtype, sourcetype, source or index in detection: ' + values["name"])
        return values

    @root_validator
    def name_max_length(cls, values):
        # Check max length only for ESCU searches, SSA does not have that constraint
        if 'ssa_' not in values['file_path']:
            if len(values["name"]) > 67:
                raise ValueError('name is longer then 67 chars: ' + values["name"])
        return values

# disable it because of performance reasons
    # @validator('references')
    # def references_check(cls, v, values):
    #     LinkValidator.check_references(v, values["name"])
    #     return v

    @validator('search')
    def search_validate(cls, v, values):
        # write search validator
        return v

 