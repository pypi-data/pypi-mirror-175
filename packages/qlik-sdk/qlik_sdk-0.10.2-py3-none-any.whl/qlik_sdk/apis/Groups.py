# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.478.8

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Group:
    """
    represents a Group document

    Attributes
    ----------
    assignedRoles: list[GroupAssignedRoles]
    createdAt: str
      The timestamp for when the group record was created.
    id: str
      The unique identifier for the group
    idpId: str
      The unique identifier for the source IDP.
    lastUpdatedAt: str
      The timestamp for when the group record was last updated.
    links: GroupLinks
      Contains Links for current document
    name: str
      The name of the group.
    status: str
      The state of the group.
    tenantId: str
      The tenant identifier associated with the given group
    """

    assignedRoles: list[GroupAssignedRoles] = None
    createdAt: str = None
    id: str = None
    idpId: str = None
    lastUpdatedAt: str = None
    links: GroupLinks = None
    name: str = None
    status: str = None
    tenantId: str = None

    def __init__(self_, **kvargs):

        if "assignedRoles" in kvargs:
            if (
                type(kvargs["assignedRoles"]).__name__
                == self_.__annotations__["assignedRoles"]
            ):
                self_.assignedRoles = kvargs["assignedRoles"]
            else:
                self_.assignedRoles = [
                    GroupAssignedRoles(**e) for e in kvargs["assignedRoles"]
                ]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ == self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "idpId" in kvargs:
            if type(kvargs["idpId"]).__name__ == self_.__annotations__["idpId"]:
                self_.idpId = kvargs["idpId"]
            else:
                self_.idpId = kvargs["idpId"]
        if "lastUpdatedAt" in kvargs:
            if (
                type(kvargs["lastUpdatedAt"]).__name__
                == self_.__annotations__["lastUpdatedAt"]
            ):
                self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
            else:
                self_.lastUpdatedAt = kvargs["lastUpdatedAt"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GroupLinks(**kvargs["links"])
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ == self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def delete(self) -> None:
        """
        Delete group by id

        Parameters
        ----------
        """
        self.auth.rest(
            path="/groups/{groupId}".replace("{groupId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )


@dataclass
class Filter:
    """
    An advanced query filter to be used for complex user querying in the tenant.

    Attributes
    ----------
    filter: str
      The advanced filtering to be applied the query. All conditional statements within this query parameter are case insensitive.
    """

    filter: str = None

    def __init__(self_, **kvargs):

        if "filter" in kvargs:
            if type(kvargs["filter"]).__name__ == self_.__annotations__["filter"]:
                self_.filter = kvargs["filter"]
            else:
                self_.filter = kvargs["filter"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupAssignedRoles:
    """
    represents a role entity to be stored on a Group entity, either default or custom role

    Attributes
    ----------
    id: str
    level: str
    name: str
    permissions: list[str]
    type: str
    """

    id: str = None
    level: str = None
    name: str = None
    permissions: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "level" in kvargs:
            if type(kvargs["level"]).__name__ == self_.__annotations__["level"]:
                self_.level = kvargs["level"]
            else:
                self_.level = kvargs["level"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "permissions" in kvargs:
            if (
                type(kvargs["permissions"]).__name__
                == self_.__annotations__["permissions"]
            ):
                self_.permissions = kvargs["permissions"]
            else:
                self_.permissions = kvargs["permissions"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupLinks:
    """
    Contains Links for current document

    Attributes
    ----------
    self: GroupLinksSelf
    """

    self: GroupLinksSelf = None

    def __init__(self_, **kvargs):

        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = GroupLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current group document
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettings:
    """
    represents a GroupSetting document

    Attributes
    ----------
    autoCreateGroups: bool
      Determines if groups should be created on login.
    links: GroupSettingsLinks
      Contains Links for current document
    syncIdpGroups: bool
      Determines if groups should be created on login.
    tenantId: str
      The unique tenant identifier.
    """

    autoCreateGroups: bool = None
    links: GroupSettingsLinks = None
    syncIdpGroups: bool = None
    tenantId: str = None

    def __init__(self_, **kvargs):

        if "autoCreateGroups" in kvargs:
            if (
                type(kvargs["autoCreateGroups"]).__name__
                == self_.__annotations__["autoCreateGroups"]
            ):
                self_.autoCreateGroups = kvargs["autoCreateGroups"]
            else:
                self_.autoCreateGroups = kvargs["autoCreateGroups"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GroupSettingsLinks(**kvargs["links"])
        if "syncIdpGroups" in kvargs:
            if (
                type(kvargs["syncIdpGroups"]).__name__
                == self_.__annotations__["syncIdpGroups"]
            ):
                self_.syncIdpGroups = kvargs["syncIdpGroups"]
            else:
                self_.syncIdpGroups = kvargs["syncIdpGroups"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ == self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettingsLinks:
    """
    Contains Links for current document

    Attributes
    ----------
    self: GroupSettingsLinksSelf
    """

    self: GroupSettingsLinksSelf = None

    def __init__(self_, **kvargs):

        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = GroupSettingsLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupSettingsLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current group settings document
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsClass:
    """
    A result object when listing groups.

    Attributes
    ----------
    data: list[Group]
      An array of groups.
    links: GroupsLinks
    totalResults: int
      Indicates the total number of matching documents. Will only be returned if the query parameter "totalResults" is true.
    """

    data: list[Group] = None
    links: GroupsLinks = None
    totalResults: int = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Group(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = GroupsLinks(**kvargs["links"])
        if "totalResults" in kvargs:
            if (
                type(kvargs["totalResults"]).__name__
                == self_.__annotations__["totalResults"]
            ):
                self_.totalResults = kvargs["totalResults"]
            else:
                self_.totalResults = kvargs["totalResults"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsLinks:
    """

    Attributes
    ----------
    next: GroupsLinksNext
    prev: GroupsLinksPrev
    self: GroupsLinksSelf
    """

    next: GroupsLinksNext = None
    prev: GroupsLinksPrev = None
    self: GroupsLinksSelf = None

    def __init__(self_, **kvargs):

        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = GroupsLinksNext(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = GroupsLinksPrev(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = GroupsLinksSelf(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsLinksNext:
    """

    Attributes
    ----------
    href: str
      Link to the next page of items
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsLinksPrev:
    """

    Attributes
    ----------
    href: str
      Link to the previous page of items
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class GroupsLinksSelf:
    """

    Attributes
    ----------
    href: str
      Link to the current page of items
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SettingsPatchSchema:
    """
    An array of JSON Patches for the groups settings.

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Groups:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def filter(
        self,
        data: Filter = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = "+name",
        max_items: int = 20,
    ) -> ListableResource[Group]:
        """
        Filter groups
        Retrieves a list of groups matching the filter using advanced query string.

        Parameters
        ----------
        limit: float = 20
          The number of user entries to retrieve.
        next: str = None
          Get users with IDs that are higher than the target user ID. Cannot be used in conjunction with prev.
        prev: str = None
          Get users with IDs that are lower than the target user ID. Cannot be used in conjunction with next.
        sort: str = "+name"
          The field to sort by, with +/- prefix indicating sort order
        data: Filter = None
          Will contain the query filter to apply. It shall not contain more than 50 ids.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/groups/actions/filter",
            method="POST",
            params=query_params,
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=Group,
            auth=self.auth,
            path="/groups/actions/filter",
            max_items=max_items,
            query_params=query_params,
        )

    def get_settings(self) -> GroupSettings:
        """
        Get group settings
        Returns the active tenant's group settings.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/groups/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = GroupSettings(**response.json())
        obj.auth = self.auth
        return obj

    def patch_settings(self, data: SettingsPatchSchema) -> None:
        """
        Update group settings

        Parameters
        ----------
        data: SettingsPatchSchema

        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        self.auth.rest(
            path="/groups/settings",
            method="PATCH",
            params={},
            data=data,
        )

    def get(self, groupId: str) -> Group:
        """
        Get group by id
        Returns the requested group.

        Parameters
        ----------
        groupId: str
          The group's unique identifier
        """
        response = self.auth.rest(
            path="/groups/{groupId}".replace("{groupId}", groupId),
            method="GET",
            params={},
            data=None,
        )
        obj = Group(**response.json())
        obj.auth = self.auth
        return obj

    def get_groups(
        self,
        filter: str = None,
        limit: float = 20,
        next: str = None,
        prev: str = None,
        sort: str = None,
        totalResults: bool = None,
        max_items: int = 20,
    ) -> ListableResource[Group]:
        """
        List groups.
        Returns a list of groups with cursor-based pagination.

        Parameters
        ----------
        filter: str = None
          The advanced filtering to use for the query. Refer to RFC 7644 https://datatracker.ietf.org/doc/rfc7644/ for the syntax. Cannot be combined with any of the fields marked as deprecated. All conditional statements within this query parameter are case insensitive.
        limit: float = 20
          The number of groups to retrieve.
        next: str = None
          The next page cursor.
        prev: str = None
          The previous page cursor.
        sort: str = None
          Optional resource field name to sort on, eg. name. Can be prefixed with +/- to determine order, defaults to (+) ascending.
        totalResults: bool = None
          Whether to return a total match count in the result. Defaults to false.
        """
        query_params = {}
        if filter is not None:
            query_params["filter"] = filter
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if totalResults is not None:
            query_params["totalResults"] = totalResults
        response = self.auth.rest(
            path="/groups",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Group,
            auth=self.auth,
            path="/groups",
            max_items=max_items,
            query_params=query_params,
        )
