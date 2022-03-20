from enum import Enum


class Permissions(str, Enum):
    AdminAnyOrganization = "org:a:a"
    ReadAnyOrganization = "org:r:a"
    CreateSelfOrganization = "org:c:s"
    UpdateSelfOrganization = "org:u:s"
    DeleteSelfOrganization = "org:d:s"
    AdminAnyAidCenter = "aidcenter:a:a"
    ReadAnyAidCenter = "aidcenter:r:a"
    CreateSelfAidCenter = "aidcenter:c:s"
    UpdateSelfAidCenter = "aidcenter:u:s"
    DeleteSelfAidCenter = "aidcenter:d:s"
    AdminAnyAssetRequest = "asset-request:a:a"
    ReadAnyAssetRequest = "asset-request:r:a"
    CreateSelfAssetRequest = "asset-request:c:s"
    UpdateSelfAssetRequest = "asset-request:u:s"
    DeleteSelfAssetRequest = "asset-request:d:s"
